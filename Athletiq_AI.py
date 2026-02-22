import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# ================= PAGE CONFIG =================
st.set_page_config(page_title="ATHLETIQ AI", layout="wide")

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    
    /* Extra top padding so heading is NEVER cut off */
    .block-container { padding-top: 5rem !important; }

    .app-title { 
        font-size: clamp(2rem, 5vw, 3.5rem); 
        font-weight: 800; 
        color: #4ade80; 
        margin: 0;
        line-height: 1.1;
    }
    .subtitle { 
        font-size: 1.1rem; 
        color: #cbd5e1; 
        margin-bottom: 20px;
    }
    .coach-bubble {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #4ade80;
        color: #f1f5f9;
    }
</style>
""", unsafe_allow_html=True)

# ================= API CONFIG (THE QUOTA FIX) =================
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

@st.cache_resource
def load_model():
    # 1.5-flash-8b is the 'Secret Weapon' for Free Tier Quota
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash-8b", 
        generation_config={"max_output_tokens": 500, "temperature": 0.7}
    )

model = load_model()

# ================= SIDEBAR =================
with st.sidebar:
    # Path logic to ensure images show up
    mascot_path = os.path.join("Athletiq_AI mascot", "Kangaroo_mascot.png")
    if os.path.exists(mascot_path):
        st.image(mascot_path, width="stretch")
    else:
        st.title("You better not slack cause I am not here!!!")
    
    st.markdown("### Coach's Corner")
    st.divider()
    
    # BMI Section
    st.markdown("#### Vitals")
    h = st.number_input("Height (cm)", 120, 220, 160)
    w = st.number_input("Weight (kg)", 25, 150, 50)
    bmi_val = round(w / ((h/100)**2), 1)
    st.metric("BMI", bmi_val)

# ================= HEADER =================
col_img, col_txt = st.columns([1, 5])
with col_img:
    logo_path = os.path.join("Athletiq_AI mascot", "Fitness_logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=120)
    else:
        st.write("🏋️ Even when I am not here, I am watching you")
with col_txt:
    st.markdown("<div class='app-title'>ATHLETIQ AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Smart Training • Safe Recovery • Peak Performance</div>", unsafe_allow_html=True)

st.divider()

# ================= INPUTS =================
c1, c2 = st.columns(2)
with c1:
    sport = st.selectbox("Sport", ["Football", "Cricket", "Basketball", "Athletics", "Badminton", "Hockey"])
    age = st.slider("Age", 10, 20, 15)
with c2:
    goal = st.selectbox("Goal", ["Build stamina", "Increase strength", "Agility"])
    injury = st.text_input("Injuries?", value="None")

# ================= GENERATION =================
if st.button("GET AN ELITE WORKOUT PLAN"):
    with st.spinner("Kangaroo Coach is hopping to work..."):
        try:
            prompt = f"Act as a high-energy Kangaroo coach. Create a short workout table and 2 tips for a {age}yo {sport} player aiming for {goal}. Injury: {injury}. Stay under 200 words."
            response = model.generate_content(prompt)
            
            st.markdown(f"""
            <div class='coach-bubble'>
                <h3 style='color:#4ade80;'>Coach's Game Plan:</h3>
                {response.text}
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error("The locker room is full! (Quota Exceeded). Wait 60 seconds and try again.")
