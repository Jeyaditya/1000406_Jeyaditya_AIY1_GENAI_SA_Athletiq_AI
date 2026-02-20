import streamlit as st
import google.generativeai as genai
from PIL import Image

# ================= PAGE CONFIG =================
try:
    icon = Image.open("Athletiq_AI mascot/Fitness_logo.png")
    st.set_page_config(page_title="ATHLETIQ AI", page_icon=icon, layout="wide")
except:
    st.set_page_config(page_title="ATHLETIQ AI", layout="wide")

# ================= CUSTOM CSS (UPDATED) =================
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    
    /* Container for the logo and title to keep them inline */
    .header-container {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 10px;
    }
    
    .app-title { 
        font-size: 3.5rem; 
        font-weight: 800; 
        color: #4ade80; 
        margin: 0;
        line-height: 1;
    }
    .subtitle { 
        font-size: 1.2rem; 
        color: #cbd5e1; 
        margin-left: 5px;
    }
    /* Rest of your existing CSS... */
    .card { background: rgba(255,255,255,0.05); padding: 25px; border-radius: 18px; border: 1px solid rgba(74, 222, 128, 0.2); margin-bottom: 20px; }
    .coach-bubble { background-color: #1e293b; padding: 25px; border-radius: 20px; border-bottom-right-radius: 5px; border: 2px solid #4ade80; color: #f1f5f9; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

# ================= HEADER SECTION (FIXED) =================
# We use columns to ensure the image and text are side-by-side without "ghost" gaps
header_col1, header_col2 = st.columns([1, 5])

with header_col1:
    try:
        # Check your path: Ensure 'Athletiq_AI mascot' is exactly correct (caps/spaces)
        st.image("Athletiq_AI mascot/Fitness_logo.png", width=150)
    except:
        st.write("🏋️") # Fallback icon if path is broken

with header_col2:
    st.markdown("<div class='app-title'>ATHLETIQ AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Smart Training • Safe Recovery • Peak Performance</div>", unsafe_allow_html=True)

st.divider() # Clean line to separate header from inputs

# ================= API CONFIG =================
# Replace with your renewed key in st.secrets
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

@st.cache_resource
def load_model():
    # max_output_tokens=800 prevents the "2000-word essay"
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config={
            "max_output_tokens": 800,
            "temperature": 0.8,
        }
    )

model = load_model()

# ================= SIDEBAR (BMI & MASCOT) =================
with st.sidebar:
    try:
        st.image("Athletiq_AI mascot/Kangaroo_mascot.png", width="stretch")
    except:
        st.write("🦘 [Mascot Image]")
    
    st.markdown("### 🦘 Coach's Corner")
    st.info("“Let’s hop to it, Champ! Time to build that elite performance!”")
    
    st.divider()
    st.markdown("#### 📊 Athlete Vitals")
    sb_height = st.number_input("Height (cm)", 120, 220, 160)
    sb_weight = st.number_input("Weight (kg)", 25, 150, 50)
    
    bmi = round(sb_weight / ((sb_height/100) ** 2), 1)
    
    if bmi < 18.5: status, col = "Underweight", "normal"
    elif 18.5 <= bmi < 24.9: status, col = "Healthy Range", "normal"
    else: status, col = "Review Build", "inverse"
    
    st.metric(label="Current BMI", value=bmi, delta=status, delta_color=col)
    st.caption("Youth BMI is a guide—focus on growth and energy!")
    
    

# ================= MAIN HEADER =================
header_col1, header_col2 = st.columns([1, 6])
with header_col2:
    st.markdown("<div class='app-title'>ATHLETIQ AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Smart Training • Safe Recovery • Peak Performance</div>", unsafe_allow_html=True)

# ================= INPUT SECTION =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    sport = st.selectbox("Sport", ["Football", "Cricket", "Basketball", "Athletics", "Badminton", "Hockey"])
    position = st.text_input("Playing Position", placeholder="e.g. Striker, Bowler")
    age = st.slider("Age", 10, 20, 15)

with c2:
    goal = st.selectbox("Primary Goal", ["Build stamina", "Increase strength", "Post-injury recovery", "Improve agility", "Match performance"])
    diet = st.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    injury = st.text_input("Injury History", placeholder="e.g. None, slight ankle pain")
st.markdown("</div>", unsafe_allow_html=True)

# ================= GENERATION LOGIC =================
def build_prompt():
    return f"""
    You are the ATHLETIQ AI Mascot, a high-energy, elite Kangaroo Sports Coach.
    Voice: Energetic, uses athletic slang (e.g., 'Ace it', 'Full throttle', 'Hopping mad gains').
    
    Context: {age}yo {sport} player ({position}). Goal: {goal}. Diet: {diet}. Injury: {injury if injury else 'None'}.
    
    STRICT OUTPUT FORMAT:
    1. Start with a 1-sentence high-energy greeting.
    2. Provide a 'Game Plan' Table (Exercise | Sets/Reps | Coach's Tip).
    3. 3 Bullet points for 'Pro-Level Fueling' and 'Injury Shield'.
    4. Keep it under 350 words total. No long paragraphs!
    """

if st.button("🚀 GENERATE ELITE TRAINING PLAN"):
    with st.spinner("Coach is drawing up the play..."):
        try:
            response = model.generate_content(build_prompt())
            
            # Displaying the Mascot's Speech
            st.markdown(f"""
            <div class='coach-bubble'>
                <h3 style='color: #4ade80; margin-top:0;'>🦘 COACH SAYS:</h3>
                {response.text}
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
            
            st.download_button(
                label="📥 Save Training Plan",
                data=response.text,
                file_name=f"Athletiq_{sport}_Plan.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"Ouch! The coach took a tumble. Try again! Error: {e}")

st.markdown("---")
st.caption("ATHLETIQ AI 2026 | Train Smart. Recover Strong.")

