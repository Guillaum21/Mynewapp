import streamlit as st
import joblib
import requests
from io import BytesIO
from sklearn.linear_model import LogisticRegressionCV
from sklearn.feature_extraction.text import TfidfVectorizer
import time
import base64

# Ensure set_page_config is the first Streamlit command
st.set_page_config(page_title='EPFL to Paris Journey', layout='wide')

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

def journey_progress(distance, target=500):
    progress_percentage = min(distance / target * 100, 100)
    return f"""
    <div style="width: 100%; background: lightgray; position: relative; height: 60px; border-radius: 10px; overflow: hidden;">
        <div style="position: absolute; width: {progress_percentage}%; height: 100%; background: linear-gradient(to right, #FF5733, #FFC300); transition: width 0.5s;">
            <img src="https://img.icons8.com/doodle/48/000000/car--v1.png" style="position: absolute; right: 0; transform: translateX(50%); height: 48px; width: 48px; animation: drive 1s infinite alternate;">
        </div>
        <img src="https://img.icons8.com/doodle/48/000000/eiffel-tower.png" style="position: absolute; right: 0; transform: translateX(-50%); height: 48px; width: 48px;">
    </div>
    <style>
        @keyframes drive {{
            0% {{ transform: translateX(50%) translateY(0); }}
            100% {{ transform: translateX(50%) translateY(-5px); }}
        }}
    </style>
    """

# Function to convert an uploaded image to base64
def get_base64_image(uploaded_file):
    img_data = uploaded_file.read()
    return base64.b64encode(img_data).decode()

# Path to the uploaded background image file
background_image_path = "/mnt/data/file-ZTHeXSTs6D0AabwBRgsylbJq"

with open(background_image_path, "rb") as image_file:
    background_image_base64 = base64.b64encode(image_file.read()).decode()

# CSS for Background
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
background: url(data:image/png;base64,{background_image_base64}) no-repeat center center fixed;
background-size: cover;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.title('EPFL to Paris Journey')

st.write('''
Welcome to the EPFL to Paris journey! As an international student at EPFL, your goal is to improve your French skills to make it to the Eiffel Tower in Paris. 
Write as complex sentences as possible in French within 60 seconds to move your car closer to the Eiffel Tower. The total distance is 500 kilometers.
''')

if 'timer_started' not in st.session_state:
    st.session_state['timer_started'] = False
    st.session_state['total_points'] = 0
    st.session_state['distance'] = 0
    st.session_state['time_left'] = 60
    st.session_state['sentences'] = []
    st.session_state['first_submission'] = False

if st.button('Start the game!') and not st.session_state['timer_started']:
    st.session_state['timer_started'] = True
    st.session_state['start_time'] = time.time()

if st.session_state['timer_started']:
    elapsed_time = time.time() - st.session_state['start_time']
    st.session_state['time_left'] = max(60 - elapsed_time, 0)
    if st.session_state['time_left'] <= 0:
        st.session_state['timer_started'] = False
        st.write(f'Final Score: {st.session_state["total_points"]} Points')
        st.write(f'Total Distance: {st.session_state["distance"]} kilometers')
        st.session_state['total_points'] = 0
        st.session_state['distance'] = 0  # Reset game
        st.session_state['sentences'] = []
        st.session_state['first_submission'] = False

user_input = st.text_input('Write your best sentences', '')
sentence_level = st.empty()

if st.session_state['timer_started'] and st.button('Submit Sentence'):
    if user_input:
        points, level = determine_french_level(user_input)
        st.session_state['total_points'] += points
        st.session_state['distance'] += points  # Each point adds 1 kilometer to the car's travel
        st.session_state['sentences'].append((user_input, points, level))
        st.session_state['first_submission'] = True
        st.write(f'French Level: {level}')
        st.write(f'Points for this sentence: {points}')
        st.write(f'Total Distance: {st.session_state["distance"]} kilometers')
        st.markdown(journey_progress(st.session_state['distance'], 500), unsafe_allow_html=True)
    else:
        st.error('Please enter a sentence before submitting.')

# Live timer
timer_placeholder = st.empty()
if st.session_state['time_left'] > 0:
    with timer_placeholder:
        st.write(f'Time Left: {int(st.session_state["time_left"])} seconds')
else:
    timer_placeholder.write("Time is up! Submit your last sentence or restart the game.")

# Encouragement messages
if st.session_state['first_submission']:
    if st.session_state['distance'] < 100:
        st.write("**Keep going! You can do it!**")
    elif st.session_state['distance'] < 250:
        st.write("Great job! You're halfway there!")
    elif st.session_state['distance'] < 400:
        st.write("You're making great progress! Almost there!")
    else:
        st.write("Just a little more! The Eiffel Tower is in sight!")

# Display sentence history
if st.session_state['sentences']:
    st.write("### Sentence History")
    for sentence, points, level in st.session_state['sentences']:
        st.write(f"Sentence: {sentence} | Points: {points} | Level: {level}")

# Continuously update the timer
while st.session_state['timer_started']:
    elapsed_time = time.time() - st.session_state['start_time']
    st.session_state['time_left'] = max(60 - elapsed_time, 0)
    if st.session_state['time_left'] <= 0:
        st.session_state['timer_started'] = False
        st.write("Time is up! Submit your last sentence or restart the game.")
        break
    timer_placeholder.write(f'Time Left: {int(st.session_state["time_left"])} seconds')
    time.sleep(1)
