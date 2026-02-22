import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

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
    
    .block-container { padding-top: 5rem !important; }

    .app-title { 
        font-size: 3.5rem; 
        font-weight: 800; 
        color: #4ade80; 
        margin: 0;
        line-height: 1.1;
    }
    .subtitle { 
        font-size: 1.3rem; 
        color: #cbd5e1; 
        margin-top: 5px;
    }
    .card {
        background: rgba(255,255,255,0.05);
        padding: 25px;
        border-radius: 18px;
        border: 1px solid rgba(74, 222, 128, 0.2);
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 1.2rem;
        color: #a7f3d0;
        font-weight: 600;
        margin-bottom: 15px;
    }
    .coach-bubble {
        background-color: #1e293b;
        padding: 25px;
        border-radius: 20px;
        border-bottom-right-radius: 5px;
        border: 2px solid #4ade80;
        color: #f1f5f9;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ================= API CONFIG =================
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

@st.cache_resource
def load_model():
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash-8b",
        generation_config={
            "max_output_tokens": 800,
            "temperature": 0.7,
        }
    )

model = load_model()

# ================= SIDEBAR =================
with st.sidebar:
    mascot_path = os.path.join("Athletiq_AI mascot", "Kangaroo_mascot.png")
    if os.path.exists(mascot_path):
        st.image(mascot_path, width="stretch")
    else:
        st.title("🦘 Better be sweating before I come back!!!")
    
    st.markdown("### Coach's Corner")
    st.info("“Let’s hop to it, Champ! Ready for some hopping mad gains?”")
    
    st.divider()
    st.markdown("####  Athlete Vitals")
    sb_height = st.number_input("Height (cm)", 120, 220, 160)
    sb_weight = st.number_input("Weight (kg)", 25, 150, 50)
    
    bmi = round(sb_weight / ((sb_height/100) ** 2), 1)
    
    if bmi < 18.5: status, col = "Underweight", "normal"
    elif 18.5 <= bmi < 24.9: status, col = "Healthy Range", "normal"
    else: status, col = "Monitor Build", "inverse"
    
    st.metric(label="Current BMI", value=bmi, delta=status, delta_color=col)
    
    

# ================= SINGLE HEADER SECTION =================
header_col1, header_col2 = st.columns([1, 5])

with header_col1:
    logo_path = os.path.join("Athletiq_AI mascot", "Fitness_logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=140)
    else:
        st.header("🏋️ Don't slack just cause I am not here!!")

with header_col2:
    st.markdown("<div class='app-title'>ATHLETIQ AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Smart Training • Safe Recovery • Peak Performance</div>", unsafe_allow_html=True)

st.divider()

# ================= MAIN INPUT LAYOUT  =================
col1, col2 = st.columns(2)

# -------- ATHLETE PROFILE --------
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'> Athlete Profile</div>", unsafe_allow_html=True)
    sport = st.selectbox("Sport", ["Football", "Cricket", "Basketball", "Athletics", "Badminton", "Hockey"])
    position = st.text_input("Playing Position", placeholder="e.g. Striker, Fast Bowler")
    age = st.slider("Age", 10, 20, 15)
    st.markdown("</div>", unsafe_allow_html=True)

# -------- TRAINING PREFERENCES --------
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'> Training Goals</div>", unsafe_allow_html=True)
    goal = st.selectbox("Primary Goal", ["Build stamina", "Increase strength", "Post-injury recovery", "Improve agility", "Match performance", "Overall fitness"])
    diet = st.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    injury = st.text_area("Injury / Risk Factors", placeholder="e.g., knee strain, ankle sprain", height=68)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= GENERATION LOGIC =================
def build_prompt():
    return f"""
    You are the ATHLETIQ AI Mascot, a high-energy, elite Kangaroo Sports Coach.
    Voice: Energetic, athletic slang (e.g., 'Ace it', 'Full throttle', 'Hopping mad gains').
    
    Context: {age}yo {sport} player ({position}). Goal: {goal}. Diet: {diet}. Injury: {injury if injury else 'None'}.
    
    STRICT OUTPUT FORMAT:
    1. 1-sentence catchy greeting as the Mascot.
    2. 'Game Plan' Table (Exercise | Sets/Reps | Coach's Tip).
    3. Bullet points for 'Pro-Level Fueling' and 'Injury Shield'.
    4. Keep it under 350 words total.
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
            st.error("The locker room is full! (Quota Exceeded). Wait 60 seconds and try again.")

st.markdown("---")
st.caption("ATHLETIQ AI 2026 | Train Smart. Recover Strong.")
