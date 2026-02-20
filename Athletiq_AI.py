import streamlit as st
import google.generativeai as genai
from PIL import Image

# ================= PAGE CONFIG =================
icon = Image.open("Athletiq_AI mascot/Fitness_logo.png")

st.set_page_config(
    page_title="ATHLETIQ AI",
    page_icon=icon,
    layout="wide"
)

# ================= SESSION STATE (ADDED) =================
if "athletiq_chats" not in st.session_state:
    st.session_state.athletiq_chats = []

# ================= CUSTOM CSS =================
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
}
.app-title {
    font-size: 3rem;
    font-weight: 800;
    color: #4ade80;
}
.subtitle {
    font-size: 1.3rem;
    color: #cbd5e1;
}
.card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}
.section-title {
    font-size: 1.2rem;
    color: #a7f3d0;
    font-weight: 600;
}
.mascot-box {
    background: rgba(255,255,255,0.04);
    padding: 20px;
    border-radius: 20px;
    text-align: center;

.mascot-row {
    display: flex;
    gap: 16px;
    align-items: flex-start;
}

.mascot-img {
    width: 90px;
}

.mascot-bubble {
    background: rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 18px;
    position: relative;
}

.mascot-bubble::before {
    content: "";
    position: absolute;
    left: -12px;
    top: 24px;
    border-width: 8px;
    border-style: solid;
    border-color: transparent rgba(255,255,255,0.08) transparent transparent;
}
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
header_col1, header_col2 = st.columns([1, 6])

with header_col1:
    st.image("Athletiq_AI mascot/Fitness_logo.png", width=180)

with header_col2:
    st.markdown("<div class='app-title'>ATHLETIQ AI</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='subtitle'>Smart Training • Safe Recovery • Peak Performance</div>",
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ================= CHAT HISTORY TABS (ADDED) =================
if st.session_state.athletiq_chats:
    tabs = st.tabs([chat["title"] for chat in st.session_state.athletiq_chats])

    for tab, chat in zip(tabs, st.session_state.athletiq_chats):
        with tab:
            st.markdown(chat["content"], unsafe_allow_html=True)

# ================= API CONFIG =================
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

@st.cache_resource
def load_model():
    return genai.GenerativeModel("gemini-2.5-flash")

model = load_model()

# ================= MAIN LAYOUT =================
left_col, right_col = st.columns([3, 1])

# ================= LEFT COLUMN =================
with left_col:

    col1, col2 = st.columns(2)

    # -------- ATHLETE PROFILE --------
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🏅 Athlete Profile</div>", unsafe_allow_html=True)

        sport = st.selectbox(
            "Sport",
            ["Football", "Cricket", "Basketball", "Athletics", "Badminton", "Hockey"]
        )
        position = st.text_input("Playing Position")
        age = st.slider("Age", 10, 20, 15)

        height = st.number_input("Height (cm)", min_value=120, max_value=220, value=160)
        weight = st.number_input("Weight (kg)", min_value=25, max_value=150, value=50)

        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 1)

        if bmi < 18.5:
            bmi_status = "Underweight"
        elif 18.5 <= bmi < 24.9:
            bmi_status = "Normal"
        elif 25 <= bmi < 29.9:
            bmi_status = "Overweight"
        else:
            bmi_status = "Obese"

        st.markdown(
            f"""
            **BMI:** {bmi}  
            **Category:** {bmi_status}  
            🛈 *BMI is a general health indicator. For youth athletes, performance and growth patterns matter more than numbers.*
            """
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # -------- TRAINING PREFERENCES --------
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🎯 Training Preferences</div>", unsafe_allow_html=True)

        goal = st.selectbox(
            "Primary Goal",
            [
                "Build stamina",
                "Increase strength",
                "Post-injury recovery",
                "Improve agility",
                "Match performance",
                "Overall fitness"
            ]
        )

        injury = st.text_area(
            "Injury / Risk Factors",
            placeholder="e.g., knee strain, ankle sprain"
        )

        diet = st.selectbox(
            "Diet Preference",
            ["Vegetarian", "Non-Vegetarian", "Vegan"]
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # -------- PROMPT --------
    def build_prompt():
        return f"""
You are ATHLETIQ AI, an expert youth sports coach.

Athlete Details:
Sport: {sport}
Position: {position}
Age: {age}
BMI: {bmi} ({bmi_status})
Goal: {goal}
Injury history: {injury}
Diet preference: {diet}

Provide:
1. Warm-up
2. Main workout
3. Injury precautions
4. Skill/tactical advice
5. Nutrition tips
6. Cool-down routine

Keep advice safe, motivating, and youth-appropriate.
"""

    if st.button("Generate Elite Training Plan"):
        with st.spinner("ATHLETIQ AI is designing your plan (Scroll up to see the recommendations!)... "):
            response = model.generate_content(build_prompt())

        formatted_response = f"""
        <div class='card'>
        <div class='section-title'>📋 Personalized Coaching Blueprint</div><br>
        {response.text}
        </div>
        """

        # ================= SAVE TO CHAT HISTORY (ADDED) =================
        st.session_state.athletiq_chats.insert(0, {
            "title": f"{sport} • {goal}",
            "content": formatted_response
        })
        st.session_state.athletiq_chats = st.session_state.athletiq_chats[:5]

        st.rerun()

# ================= RIGHT COLUMN =================
with right_col:
    st.markdown("<div class='mascot-box'>", unsafe_allow_html=True)
    st.markdown("### Your Fitness Coach")

    st.image(
        "Athletiq_AI mascot/Kangaroo_mascot.png",
        caption="ATHLETIQ AI Coach",
        use_container_width=True
    )

    st.markdown("💬 *Train smart. Recover strong.*")
    st.markdown("</div>", unsafe_allow_html=True)
