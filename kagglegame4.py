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
        'B1': 20,
        'B2': 30,
        'C1': 40,
        'C2': 50
    }
    
    points = level_points.get(level, 0)
    return points, level

def journey_progress(distance, target=517):
    progress_percentage = min(distance / target * 100, 100)
    return f"""
    <div style="width: 100%; background: lightgray; position: relative; height: 60px; border-radius: 10px; overflow: hidden;">
        <div style="position: absolute; width: {progress_percentage}%; height: 100%; background: linear-gradient(to right, #0000FF, #FFFFFF, #FF0000); transition: width 0.5s;">
            <img src="https://img.icons8.com/doodle/48/000000/car--v1.png" style="position: absolute; right: 0; transform: translateX(50%); height: 48px; width: 48px; animation: drive 1s infinite alternate;">
        </div>
        <img src="https://img.icons8.com/ios-filled/50/000000/eiffel-tower.png" style="position: absolute; right: 0; transform: translateX(-50%); height: 48px; width: 48px;">
    </div>
    <style>
        @keyframes drive {{
            0% {{ transform: translateX(50%) translateY(0); }}
            100% {{ transform: translateX(50%) translateY(-5px); }}
        }}
    </style>
    """

# CSS for Background
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background: url(https://www.canva.com/design/DAGF9e6tdVs/pbXKXsMvuCtlsTmHfRVfzA/view?embed) no-repeat center center fixed;
background-size: cover;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page", ["Welcome", "Game", "Review and Learn"])

# Welcome Page
if page == "Welcome":
    st.title('Welcome to EPFL to Paris Journey')
    st.write('''
    Welcome to the EPFL to Paris journey! As an international student at EPFL, your goal is to improve your French skills to make it to the Eiffel Tower in Paris. 
    Write as complex sentences as possible in French within 90 seconds to move your car closer to the Eiffel Tower. The total distance is 517 kilometers.
    Are you ready for the challenge? Let's start the game and see how far you can go!
    ''')
    
    # Embed the image using HTML iframe
    st.markdown('''
    <div style="position: relative; width: 100%; height: 0; padding-top: 56.2500%;
    padding-bottom: 0; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden;
    border-radius: 8px; will-change: transform;">
      <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0;margin: 0;"
        src="https://www.canva.com/design/DAGF9e6tdVs/pbXKXsMvuCtlsTmHfRVfzA/view?embed" allowfullscreen="allowfullscreen" allow="fullscreen">
      </iframe>
    </div>
    <a href="https://www.canva.com/design/DAGF9e6tdVs/pbXKXsMvuCtlsTmHfRVfzA/view?utm_content=DAGF9e6tdVs&utm_campaign=designshare&utm_medium=embeds&utm_source=link" target="_blank" rel="noopener">
    ''', unsafe_allow_html=True)

# Game Page
elif page == "Game":
    st.title('EPFL to Paris Journey')

    st.write('''
    Welcome to the EPFL to Paris journey! As an international student at EPFL, your goal is to improve your French skills to make it to the Eiffel Tower in Paris. 
    Write as complex sentences as possible in French within 90 seconds to move your car closer to the Eiffel Tower. The total distance is 517 kilometers.
    ''')

    if 'timer_started' not in st.session_state:
        st.session_state['timer_started'] = False
        st.session_state['total_points'] = 0
        st.session_state['distance'] = 0
        st.session_state['time_left'] = 90
        st.session_state['sentences'] = []
        st.session_state['first_submission'] = False

    if st.button('Start the game!') and not st.session_state['timer_started']:
        st.session_state['timer_started'] = True
        st.session_state['start_time'] = time.time()

    if st.session_state['timer_started']:
        elapsed_time = time.time() - st.session_state['start_time']
        st.session_state['time_left'] = max(90 - elapsed_time, 0)
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
            st.markdown(journey_progress(st.session_state['distance'], 517), unsafe_allow_html=True)
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

# Review and Learn Page
elif page == "Review and Learn":
    st.title("Review and Learn")

    if 'sentences' in st.session_state and st.session_state['sentences']:
        st.write("### Sentence History")
        for sentence, points, level in st.session_state['sentences']:
            st.write(f"Sentence: {sentence} | Points: {points} | Level: {level}")

    st.write("### 10 Most Used Sentences in Paris")
    most_used_sentences = [
        "Bonjour, comment ça va ?",
        "Je voudrais un café, s'il vous plaît.",
        "Où est la station de métro la plus proche ?",
        "Combien ça coûte ?",
        "Pouvez-vous m'aider, s'il vous plaît ?",
        "Je suis perdu.",
        "Quelle heure est-il ?",
        "Parlez-vous anglais ?",
        "Merci beaucoup.",
        "Au revoir et bonne journée."
    ]

    for sentence in most_used_sentences:
        st.write(f"- {sentence}")

# Continuously update the timer
while st.session_state.get('timer_started', False):
    elapsed_time = time.time() - st.session_state['start_time']
    st.session_state['time_left'] = max(90 - elapsed_time, 0)
    if st.session_state['time_left'] <= 0:
        st.session_state['timer_started'] = False
        st.write("Time is up! Submit your last sentence or restart the game.")
        break
    timer_placeholder.write(f'Time Left: {int(st.session_state["time_left"])} seconds')
    time.sleep(1)
