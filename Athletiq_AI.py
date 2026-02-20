import streamlit as st
import google.generativeai as genai
from PIL import Image

# ================= PAGE CONFIG =================
try:
    icon = Image.open("Athletiq_AI mascot/Fitness_logo.png")
    st.set_page_config(page_title="ATHLETIQ AI", page_icon=icon, layout="wide")
except:
    st.set_page_config(page_title="ATHLETIQ AI", layout="wide")

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .block-container { padding-top: 1.5rem; }
    
    .app-title { 
        font-size: 3.5rem; 
        font-weight: 800; 
        color: #4ade80; 
        margin: 0;
        line-height: 1.1;
    }
    .subtitle { 
        font-size: 1.2rem; 
        color: #cbd5e1; 
        margin-top: 0px;
    }
    .card {
        background: rgba(255,255,255,0.05);
        padding: 20px;
        border-radius: 18px;
        border: 1px solid rgba(74, 222, 128, 0.2);
        margin-bottom: 15px;
    }
    .coach-bubble {
        background-color: #1e293b;
        padding: 25px;
        border-radius: 20px;
        border-bottom-right-radius: 5px;
        border: 2px solid #4ade80;
        color: #f1f5f9;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ================= API CONFIG =================
# Ensure GEMINI_API_KEY is correctly set in your Streamlit Secrets
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

@st.cache_resource
def load_model():
    # Switching to 1.5-flash to help with Quota limits on Free Tier
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "max_output_tokens": 600,
            "temperature": 0.7,
        }
    )

model = load_model()

# ================= SIDEBAR (BMI & MASCOT) =================
with st.sidebar:
    try:
        # 2026 Syntax: width="stretch" replaces use_container_width=True
        st.image("Athletiq_AI mascot/Kangaroo_mascot.png", width="stretch")
    except:
        st.title("🦘")
    
    st.markdown("### 🦘 Coach's Corner")
    st.info("“Let’s hop to it, Champ! Time to build that elite performance!”")
    
    st.divider()
    st.markdown("#### 📊 Athlete Vitals")
    sb_height = st.number_input("Height (cm)", 120, 220, 160)
    sb_weight = st.number_input("Weight (kg)", 25, 150, 50)
    
    # Simple BMI Logic
    bmi_calc = round(sb_weight / ((sb_height/100) ** 2), 1)
    
    if bmi_calc < 18.5: 
        status, col = "Underweight", "normal"
    elif 18.5 <= bmi_calc < 24.9: 
        status, col = "Healthy Range", "normal"
    else: 
        status, col = "Review Build", "inverse"
    
    st.metric(label="Current BMI", value=bmi_calc, delta=status, delta_color=col)
    st.caption("Youth BMI varies by growth spurt—keep training hard!")

# ================= MAIN HEADER =================
# Fixed the "Ghost Box" by ensuring no empty markdown is rendered
header_col1, header_col2 = st.columns([1, 5])

with header_col1:
    try:
        st.image("Athletiq_AI mascot/Fitness_logo.png", width=120)
    except:
        st.header("🏋️")

with header_col2:
    st.markdown(f"<div class='app-title'>ATHLETIQ AI</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>Smart Training • Safe Recovery • Peak Performance</div>", unsafe_allow_html=True)

st.divider()

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
    Voice: Energetic, athletic slang, use phrases like 'Ace it', 'Full throttle', 'Hopping mad gains'.
    
    Context: {age}yo {sport} player ({position}). Goal: {goal}. Diet: {diet}. Injury: {injury if injury else 'None'}.
    
    STRICT OUTPUT FORMAT:
    1. 1-sentence catchy greeting as the Mascot.
    2. 'Game Plan' Table (Exercise | Sets/Reps | Coach's Tip).
    3. 3 Bullet points for 'Fueling' and 'Safety'.
    4. NO long paragraphs. Keep it under 300 words.
    """

if st.button("🚀 GENERATE ELITE TRAINING PLAN"):
    if not GEMINI_API_KEY:
        st.error("Please add your API Key to Streamlit Secrets!")
    else:
        with st.spinner("Coach is drawing up the play..."):
            try:
                response = model.generate_content(build_prompt())
                
                # The Mascot Speech Bubble
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
                st.error("The API quota is full or the key is expired. Please try again in a few minutes!")
                st.info("Tip: Free tier has a limit of 15 requests per minute.")

st.markdown("---")
st.caption("ATHLETIQ AI 2026 | Train Smart. Recover Strong.")
