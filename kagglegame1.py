import streamlit as st
import joblib
import requests
from io import BytesIO
from sklearn.linear_model import LogisticRegressionCV
from sklearn.feature_extraction.text import TfidfVectorizer
import time

# Ensure set_page_config is the first Streamlit command
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

# Function to determine points based on predicted level
def determine_french_level(sentence):
    sentence_transformed = vectorizer.transform([sentence])
    prediction = model.predict(sentence_transformed)[0]
    
    st.write(f"Debug: Prediction is {prediction}")

    # Map numerical predictions to CEFR levels
    prediction_to_level = {
        0: 'A1',
        1: 'A2',
        2: 'B1',
        3: 'B2',
        4: 'C1',
        5: 'C2'
    }

    level = prediction_to_level.get(prediction, 'Unknown')
    level_points = {
        'A1': 5,
        'A2': 10,
        'B1': 15,
        'B2': 20,
        'C1': 25,
        'C2': 30
    }
    
    points = level_points.get(level, 0)
    return points, level

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
The goal is to reach 2000 meters.
''')

if 'timer_started' not in st.session_state:
    st.session_state['timer_started'] = False
    st.session_state['total_points'] = 0
    st.session_state['distance'] = 0
    st.session_state['time_left'] = 60

if st.button('Start') and not st.session_state['timer_started']:
    st.session_state['timer_started'] = True
    st.session_state['start_time'] = time.time()

if st.session_state['timer_started']:
    elapsed_time = time.time() - st.session_state['start_time']
    st.session_state['time_left'] = max(60 - elapsed_time, 0)
    if st.session_state['time_left'] <= 0:
        st.session_state['timer_started'] = False
        st.write(f'Final Score: {st.session_state["total_points"]} Points')
        st.write(f'Total Distance: {st.session_state["distance"]} meters')
        st.session_state['total_points'] = 0
        st.session_state['distance'] = 0  # Reset game

user_input = st.text_input('Write a short sentence here', '')
sentence_level = st.empty()

if st.session_state['timer_started'] and st.button('Submit Sentence'):
    if user_input:
        points, level = determine_french_level(user_input)
        st.write(f"Debug: Points = {points}, Level = {level}")
        st.session_state['total_points'] += points
        st.session_state['distance'] += points * 10  # Each point adds 10 meters to the boat's travel
        st.write(f'Points for this sentence: {points}')
        sentence_level.text(f'French Level: {level}')
        st.write(f'Total Points: {st.session_state["total_points"]}')
        st.write(f'Distance: {st.session_state["distance"]} meters')
        st.markdown(boat_progress(st.session_state['distance'], 2000), unsafe_allow_html=True)
    else:
        st.error('Please enter a sentence before submitting.')

if st.session_state['time_left'] > 0:
    st.write(f'Time Left: {int(st.session_state["time_left"])} seconds')
else:
    st.write("Time is up! Submit your last sentence or restart the game.")
