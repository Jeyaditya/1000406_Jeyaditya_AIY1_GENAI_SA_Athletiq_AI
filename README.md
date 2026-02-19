# 1000406_Jeyaditya_AIY1_GENAI_SA_Athletiq_AI
# PROJECT REPORT: ATHLETIQ AI 
**Subject:** Artificial Intelligence & Web Development Project Submission
**Student Name:** Jeyaditya
**Registration number:** 1000406

---

## 1. Project Overview
**ATHLETIQ AI** is an intelligent sports science application designed to bridge the gap between elite coaching and youth athletes. Recognizing that young athletes have unique physiological needs, this application uses Large Language Models (LLMs) to generate safe, age-appropriate, and sport-specific training regimens.

The core objective of this project is to demonstrate the integration of Generative AI (Gemini 1.5 Flash) with a modern web framework (Streamlit) to provide actionable, personalized data for physical education and athletic development.

## 2. Key Features & Functionality
* **Dynamic Athlete Profiling:** The system captures essential metrics including sport type, playing position, age, and physical dimensions.
* **Automated BMI Logic:** Includes a built-in calculator to categorize the athlete's physical status, which informs the AI’s intensity recommendations.
* **Multi-Faceted Plan Generation:** Each AI-generated response is structured into six critical pillars:
    1.  Dynamic Warm-ups
    2.  Sport-Specific Main Workouts
    3.  Injury Prevention & Risk Management
    4.  Skill-based Tactical Advice
    5.  Dietary Recommendations (Veg/Non-Veg/Vegan)
    6.  Regulated Cool-down Routines
* **Session State Management:** Implements a "Recent History" feature using Streamlit session states, allowing the user to compare the last five generated plans without losing data during the session.

## 3. Technical Architecture
* **Frontend UI:** Developed using Streamlit with custom CSS injection for a high-contrast "Elite Athlete" dark-mode theme.
* **Backend Logic:** Python-based processing for BMI calculation and data handling.
* **AI Integration:** Utilizes the `google-generativeai` library to communicate with the Gemini 1.5 Flash model.
* **Prompt Engineering:** Features a structured prompt template that ensures the AI maintains a "Youth-Appropriate" and "Motivating" persona while prioritizing safety.

## 4. How to Execute the Project
1.  **Install Dependencies:**
    ```bash
    pip install streamlit google-generativeai Pillow
    ```
2.  **API Configuration:**
    Ensure a `.streamlit/secrets.toml` file exists with a valid `GEMINI_API_KEY`.
3.  **Directory Structure:**
    Place the main code in `Athletiq_AI.py` and ensure the `Athletiq_AI mascot/` folder contains the required image assets (`Fitness_logo.png` and `Kangaroo_mascot.png`).
4.  **Launch:**
    ```bash
    streamlit run Athletiq_AI.py
    ```

## 5. Conclusion
This project demonstrates how AI can be democratized for youth sports, providing high-quality coaching advice that was previously only accessible to professional athletes. It emphasizes safety, user experience, and the practical application of prompt engineering in a real-world scenario.

---

**Credits**
* Student name: Jeyaditya
* CRS Facilitator: Mrs. Arul Jyoti
