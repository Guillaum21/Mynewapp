import streamlit as st
import joblib
import requests
from io import BytesIO
import time
from sklearn.linear_model import LogisticRegressionCV  # Ensure this import is here
from sklearn.feature_extraction.text import TfidfVectorizer  # If you use it in other parts

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

# Function to determine French level based on sentence complexity
def determine_french_level(sentence):
    words = sentence.split()
    num_words = len(words)
    unique_words = len(set(words))
    average_word_length = sum(len(word) for word in words) / num_words if num_words else 0
    lexical_diversity = unique_words / num_words if num_words else 0

    level = "Débutant (A1)"  # Default to beginner if no other criteria met
    if num_words < 5:
        points = 5
    elif 5 <= num_words < 10:
        points = 10
        level = "Élémentaire (A2)"
    elif 10 <= num_words < 15:
        points = 15
        level = "Intermédiaire (B1)"
    elif 15 <= num_words < 20:
        points = 20
        level = "Intermédiaire Avancé (B2)"
    elif 20 <= num_words < 25:
        points = 25
        level = "Avancé (C1)"
    else:
        points = 30
        level = "Expérimenté (C2)"

    additional_points = (average_word_length * 1.5) + (lexical_diversity * 10)
    total_points = points + additional_points
    return total_points, level

# Function to display the boat progress
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

st.set_page_config(page_title='Jeu de Complexité des Phrases Françaises', layout='wide')
st.title('Jeu de Complexité des Phrases Françaises')

st.write('''
Write as complex sentences as possible in French within 60 seconds to pilot the boat as far as possible.
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
        st.session_state['total_points'] += points
        st.session_state['distance'] += points * 10  # Each point adds 10 meters to the boat's travel

        # Transform the input sentence using the loaded vectorizer and model
        sentence_transformed = vectorizer.transform([user_input])
        model_prediction = model.predict(sentence_transformed)
        model_difficulty = model_prediction[0]

        st.write(f'Points for this sentence: {points}')
        st.write(f'Predicted Difficulty by Model: {model_difficulty}')
        sentence_level.text(f'French Level: {level}')
        st.write(f'Total Points: {st.session_state["total_points"]}')
        st.write(f'Distance: {st.session_state["distance"]} meters')
        st.markdown(boat_progress(st.session_state['distance'], 5000), unsafe_allow_html=True)
    else:
        st.error('Please enter a sentence before submitting.')
