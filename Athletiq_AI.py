import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# ================= PAGE CONFIG =================
# Try-except for the favicon
icon_path = "Athletiq_AI mascot/Fitness_logo.png"
try:
    icon = Image.open(icon_path)
    st.set_page_config(page_title="ATHLETIQ AI", page_icon=icon, layout="wide")
except:
    st.set_page_config(page_title="ATHLETIQ AI", layout="wide")

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    
    /* Increased top padding so heading isn't cut off */
    .block-container { 
        padding-top: 4rem !important; 
        padding-bottom: 2rem;
    }

    .app-title { 
        font-size: 3.8rem; 
        font-weight: 800; 
        color: #4ade80; 
        margin: 0;
        line-height: 1.2; /* Increased to prevent clipping */
        letter-spacing: -1px;
    }
    .subtitle { 
        font-size: 1.3rem; 
        color: #cbd5e1; 
        margin-top: 0px;
        font-weight: 400;
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
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

@st.cache_resource
def load_model():
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={"max_output_tokens": 600, "temperature": 0.7}
    )

model = load_model()

# ================= SIDEBAR =================
with st.sidebar:
    mascot_path = "Athletiq_AI mascot/Kangaroo_mascot.png"
    if os.path.exists(mascot_path):
        st.image(mascot_path, width="stretch")
    else:
        st.error(f"Image not found at: {mascot_path}")
        st.title("🦘")
    
    st.markdown("### 🦘 Coach's Corner")
    st.info("“Let’s hop to it, Champ!”")
    
    st.divider()
    st.markdown("#### 📊 Athlete Vitals")
    sb_height = st.number_input("Height (cm)", 120, 220, 160)
    sb_weight = st.number_input("Weight (kg)", 25, 150, 50)
    
    bmi_calc = round(sb_weight / ((sb_height/100) ** 2), 1)
    
    if bmi_calc < 18.5: status, col = "Underweight", "normal"
    elif 18.5 <= bmi_calc < 24.9: status, col = "Healthy Range", "normal"
    else: status, col = "Review Build", "inverse"
    
    st.metric(label="Current BMI", value=bmi_calc, delta=status, delta_color=col)
    
    

# ================= MAIN HEADER =================
header_col1, header_col2 = st.columns([1, 4])

with header_col1:
    if os.path.exists(icon_path):
        st.image(icon_path, width=150)
    else:
        st.markdown("<h1 style='font-size: 80px;'>🏋️</h1>", unsafe_allow_html=True)

with header_col2:
    st.markdown("<div class='app-title'>ATHLETIQ AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Smart Training • Safe Recovery • Peak Performance</div>", unsafe_allow_html=True)

st.divider()

# ================= INPUTS & GENERATION =================
st.markdown("<div class='card'>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    sport = st.selectbox("Sport", ["Football", "Cricket", "Basketball", "Athletics", "Badminton", "Hockey"])
    position = st.text_input("Playing Position", placeholder="e.g. Striker")
    age = st.slider("Age", 10, 20, 15)
with c2:
    goal = st.selectbox("Primary Goal", ["Build stamina", "Increase strength", "Improve agility"])
    diet = st.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    injury = st.text_input("Injury History", placeholder="e.g. None")
st.markdown("</div>", unsafe_allow_html=True)

if st.button("GENERATE ELITE TRAINING PLAN"):
    with st.spinner("Coach is drawing up the play..."):
        try:
            prompt = f"Role: High-energy Kangaroo Coach. Athlete: {age}yo {sport} {position}. Goal: {goal}. Brief Workout Table + 3 tips."
            response = model.generate_content(prompt)
            
            st.markdown(f"""
            <div class='coach-bubble'>
                <h3 style='color: #4ade80; margin-top:0;'> COACH SAYS:</h3>
                {response.text}
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
        except Exception as e:
            st.error("Quota full! Try again in 60 seconds.")

st.markdown("---")
st.caption("ATHLETIQ AI")

