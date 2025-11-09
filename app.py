import streamlit as st
import numpy as np
import pickle

# Load trained model

@st.cache_resource
def load_model():
    with open("Retrained_Model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

# Streamlit Setup
st.set_page_config(
    page_title="Sleep Disorder Predictor",
    page_icon="😴",
    layout="centered"
)

st.title("😴 Sleep Disorder Prediction")
st.write("Predict if you are likely to have a sleep disorder based on your health and lifestyle data.")

# Input Fields
st.header("👤 Personal Information")
gender = st.selectbox("Gender", ["Male", "Female"])
age = st.number_input("Age", min_value=10, max_value=100, value=25)
occupation = st.selectbox(
    "Occupation",
    [
        "Software Engineer", "Doctor", "Nurse", "Teacher", "Salesperson", 
        "Lawyer", "Engineer", "Student", "Scientist", "Driver", "Other"
    ]
)

st.header("💤 Sleep & Activity")
sleep_duration = st.slider("Sleep Duration (hours)", 0.0, 12.0, 7.0, 0.5)
quality_of_sleep = st.slider("Quality of Sleep (1–10)", 1, 10, 6)
physical_activity = st.slider("Physical Activity (minutes/day)", 0, 180, 30)
daily_steps = st.number_input("Daily Steps", min_value=0, max_value=30000, value=5000, step=500)

st.header("❤️ Health Metrics")
stress_level = st.slider("Stress Level (1–10)", 1, 10, 5)
bmi_category = st.selectbox("BMI Category", ["Normal", "Obese", "Overweight", "Underweight"])
heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=180, value=70)
upper_bp = st.number_input("Upper BP (Systolic)", min_value=90, max_value=180, value=120)
lower_bp = st.number_input("Lower BP (Diastolic)", min_value=60, max_value=120, value=80)

# Encoding Inputs (from LabelEncoder)
gender_map = {"Male": 1, "Female": 0}
bmi_map = {"Normal": 0, "Obese": 1, "Overweight": 2, "Underweight": 3}

# Occupation encoding (as per your LabelEncoder order)
occupation_map = {
    "Software Engineer": 9,
    "Doctor": 1,
    "Nurse": 6,
    "Teacher": 10,
    "Salesperson": 5,
    "Lawyer": 2,
    "Engineer": 0,
    "Student": 8,
    "Scientist": 3,
    "Driver": 7,
    "Other": 4
}

# Prepare model input
input_data = np.array([[
    gender_map[gender],
    age,
    occupation_map[occupation],
    sleep_duration,
    quality_of_sleep,
    physical_activity,
    stress_level,
    bmi_map[bmi_category],
    heart_rate,
    daily_steps,
    upper_bp,
    lower_bp
]])

# Prediction
if st.button("🔍 Predict Sleep Disorder"):
    prediction = model.predict(input_data)[0]

    label_map = {0: "No Disorder", 1: "Sleep Apnea", 2: "Insomnia"}

    st.subheader("📊 Prediction Result:")
    disorder = label_map.get(prediction, "Unknown")

    if disorder == "No Disorder":
        st.success("✅ You are unlikely to have a sleep disorder.")
    elif disorder == "Sleep Apnea":
        st.warning("⚠️ Possible Sleep Apnea detected. Consider medical consultation.")
    else:
        st.error("😴 Possible Insomnia detected. Try improving sleep hygiene.")

st.markdown("---")

