import streamlit as st
import time
import joblib
import requests
from io import BytesIO
from sklearn.linear_model import LogisticRegressionCV  # Ensure this import is here
from sklearn.feature_extraction.text import TfidfVectorizer  # If you use it in other parts
from datetime import datetime

# Set the page configuration
st.set_page_config(page_title='Jeu de Complexité des Phrases Françaises', layout='wide')

# Load the vectorizer and model from GitHub
@st.cache_resource
def load_vectorizer_model():
    vectorizer_url = "https://github.com/tcastrom/CEFR-French/raw/main/Models/Basic%20Models/Streamlit/vectorizer.joblib"
    model_url = "https://github.com/tcastrom/CEFR-French/raw/main/Models/Basic%20Models/Streamlit/logistic_regression_model.joblib"
    
    vectorizer_response = requests.get(vectorizer_url)
    model_response = requests.get(model_url)
    
    vectorizer = joblib.load(BytesIO(vectorizer_response.content))
    model = joblib.load(BytesIO(model_response.content))
    
    return vectorizer, model

vectorizer, model = load_vectorizer_model()

# Function to determine points based on model prediction
def determine_points_from_model(prediction):
    # Map the model prediction to points
    difficulty_to_points = {
        "A1": 5,
        "A2": 10,
        "B1": 15,
        "B2": 20,
        "C1": 25,
        "C2": 30
    }
    return difficulty_to_points.get(prediction, 0), prediction

def boat_progress(distance, target=2000):
    progress_percentage = min(distance / target * 100, 100)
    return f"""
    <div style="width: 100%; background: lightblue; position: relative; height: 50px; border-radius: 10px;">
        <div style="position: absolute; width: {progress_percentage}%; height: 100%; background: linear-gradient(to right, #0078D7, #83C5BE);">
            <span style="position: absolute; right: 0; transform: translateX(50%); font-size: 24px;">⛵</span> <!-- Increased size for the boat -->
        </div>
        <span style="position: absolute; right: 0; transform: translateX(-100%); color: black; font-size: 24px;">🏁</span> <!-- Increased size for the flag -->
    </div>
    """

st.title('Jeu de Complexité des Phrases Françaises')

st.write('''
Write as complex sentences as possible in French within 60 seconds to push the boat as far as possible.
The goal is to reach 200 meters.
''')

if 'timer_started' not in st.session_state:
    st.session_state['timer_started'] = False
    st.session_state['total_points'] = 0
    st.session_state['distance'] = 0
    st.session_state['time_left'] = 1000

clock_placeholder = st.empty()  # Placeholder for the clock

if st.button('Start') and not st.session_state['timer_started']:
    st.session_state['timer_started'] = True
    st.session_state['start_time'] = time.time()

if st.session_state['timer_started']:
    start_time = st.session_state['start_time']
    while time.time() - start_time < 1000:
        elapsed_time = time.time() - st.session_state['start_time']
        st.session_state['time_left'] = max(1000 - elapsed_time, 0)
        clock_placeholder.text(f"Time Left: {int(st.session_state['time_left'])} seconds")
        time.sleep(1)
    st.session_state['timer_started'] = False
    st.write(f'Final Score: {round(st.session_state["total_points"], 2)} Points')
    st.write(f'Total Distance: {round(st.session_state["distance"], 2)} meters')
    st.session_state['total_points'] = 0
    st.session_state['distance'] = 0  # Reset game

user_input = st.text_input('Write your best sentence', '')
sentence_level = st.empty()

if st.session_state['timer_started'] and st.button('Submit Sentence'):
    if user_input:
        # Transform the input sentence using the loaded vectorizer and model
        sentence_transformed = vectorizer.transform([user_input])
        model_prediction = model.predict(sentence_transformed)
        model_difficulty = model_prediction[0]
        
        # Determine points based on model prediction
        points, level = determine_points_from_model(model_difficulty)
        st.session_state['total_points'] += points
        st.session_state['distance'] += points * 10  # Each point adds 10 meters to the boat's travel

        st.write(f'Points for this sentence: {round(points, 2)}')
        st.write(f'Predicted Difficulty by Model: {model_difficulty}')
        sentence_level.text(f'French Level: {model_difficulty}')
        st.write(f'Total Points: {round(st.session_state["total_points"], 2)}')
        st.write(f'Distance: {round(st.session_state["distance"], 2)} meters')
        st.markdown(boat_progress(st.session_state['distance'], 2000), unsafe_allow_html=True)
    else:
        st.error('Please enter a sentence before submitting.')

if st.session_state['time_left'] > 0:
    st.write(f'Time Left: {int(st.session_state["time_left"])} seconds')
else:
    st.write("Time is up! Submit your last sentence or restart the game.")
