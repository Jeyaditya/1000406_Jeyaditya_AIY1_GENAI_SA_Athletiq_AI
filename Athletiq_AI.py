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
    
    /* Increased top padding to ensure the header is never cut off */
    .block-container { padding-top: 5.5rem !important; }

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
        model_name="gemini-1.5-flash", # Using the most stable 2026 free-tier model name
        generation_config={
            "max_output_tokens": 1000,
            "temperature": 0.6,
        }
    )

model = load_model()

# ================= SESSION STATE (Prevents cut-offs and handles sidebar download) =================
if "training_plan" not in st.session_state:
    st.session_state.training_plan = ""

# ================= SIDEBAR =================
with st.sidebar:
    mascot_path = os.path.join("Athletiq_AI mascot", "Kangaroo_mascot.png")
    if os.path.exists(mascot_path):
        st.image(mascot_path, width="stretch")
    else:
        st.title("Better be sweating before I come back!!!")
    
    st.markdown("### Coach's Corner")
    st.info("“Let’s hop to it, Champ! Ready for some hopping mad gains?”")
    
    st.divider()
    st.markdown("#### Athlete Vitals")
    sb_height = st.number_input("Height (cm)", 120, 220, 160)
    sb_weight = st.number_input("Weight (kg)", 25, 150, 50)
    
    bmi = round(sb_weight / ((sb_height/100) ** 2), 1)
    
    if bmi < 18.5: status, col = "Underweight", "normal"
    elif 18.5 <= bmi < 24.9: status, col = "Healthy Range", "normal"
    else: status, col = "Monitor Build", "inverse"
    
    st.metric(label="Current BMI", value=bmi, delta=status, delta_color=col)

    # Sidebar Download Button (Only shows after generation)
    if st.session_state.training_plan:
        st.divider()
        st.download_button(
            label="📥 Save Training Plan",
            data=st.session_state.training_plan,
            file_name=f"Athletiq_Training_Plan.txt",
            mime="text/plain",
            use_container_width=True
        )

# ================= SINGLE HEADER SECTION =================
header_col1, header_col2 = st.columns([1, 5])

with header_col1:
    logo_path = os.path.join("Athletiq_AI mascot", "Fitness_logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=140)
    else:
        st.header("Don't slack just cause I am not here!!")

with header_col2:
    st.markdown("<div class='app-title'>ATHLETIQ AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Smart Training • Safe Recovery • Peak Performance</div>", unsafe_allow_html=True)

st.divider()

# ================= MAIN INPUT LAYOUT =================
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Athlete Profile</div>", unsafe_allow_html=True)
    sport = st.selectbox("Sport", ["Football", "Cricket", "Basketball", "Athletics", "Badminton", "Hockey"])
    position = st.text_input("Playing Position", placeholder="e.g. Striker, Fast Bowler")
    age = st.slider("Age", 10, 20, 15)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Training Goals</div>", unsafe_allow_html=True)
    goal = st.selectbox("Primary Goal", ["Build stamina", "Increase strength", "Post-injury recovery", "Improve agility", "Match performance", "Overall fitness"])
    diet = st.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    injury = st.text_area("Injury / Risk Factors", placeholder="e.g., knee strain, ankle sprain", height=68)
    st.markdown("</div>", unsafe_allow_html=True)

# ================= GENERATION LOGIC =================
def build_prompt():
    return f"""
    You are the ATHLETIQ AI Mascot who is very energetic and loves dad jokes (Kangaroo Coach). 
    TASK: Create a TIGHT training plan for a {age}yo {sport} player ({position}).
    Goal: {goal}. Diet: {diet}. Injury: {injury if injury else 'None'}.

    STRICT RULES:
    1. Limit the greeting to 5 WORDS MAX.
    2. Provide separate short paragraphs for Exercise, Reps, and Coach Tip.
    3. Use 3 short bullet points for fueling/safety.
    4. NO long paragraphs. Finish the response entirely and clearly.
    """

if st.button("🚀 GENERATE ELITE TRAINING PLAN"):
    with st.spinner("Coach is breaking down a game plan! ..."):
        try:
            response = model.generate_content(build_prompt())
            st.session_state.training_plan = response.text
            st.balloons()
        except Exception as e:
            st.error(f"Coach is out of breath! Error: {str(e)}")

# Display the result (locked in via session state)
if st.session_state.training_plan:
    st.markdown(f"""
    <div class='coach-bubble'>
        <h3 style='color: #4ade80; margin-top:0;'>COACH SAYS:</h3>
        {st.session_state.training_plan}
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("ATHLETIQ AI 2026 | Train Smart. Recover Strong.")
