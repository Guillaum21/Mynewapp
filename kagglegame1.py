import streamlit as st
import joblib
import requests
from io import BytesIO
from sklearn.linear_model import LogisticRegressionCV
from sklearn.feature_extraction.text import TfidfVectorizer
import random

# Load the vectorizer and model from GitHub
@st.cache(allow_output_mutation=True)
def load_vectorizer_model():
    vectorizer_url = "https://github.com/tcastrom/CEFR-French/raw/main/Models/Basic%20Models/Streamlit/vectorizer.joblib"
    model_url = "https://github.com/tcastrom/CEFR-French/raw/main/Models/Basic%20Models/Streamlit/logistic_regression_model.joblib"
    
    vectorizer_response = requests.get(vectorizer_url)
    model_response = requests.get(model_url)
    
    vectorizer = joblib.load(BytesIO(vectorizer_response.content))
    model = joblib.load(BytesIO(model_response.content))
    
    return vectorizer, model

vectorizer, model = load_vectorizer_model()

# Streamlit app
st.title("Sentence Difficulty Prediction Game")

# Initialize session state for scores and game state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'round' not in st.session_state:
    st.session_state.round = 1

# Display the score and round
st.write(f"Round: {st.session_state.round}")
st.write(f"Score: {st.session_state.score}")

# Game rules
st.write("""
## How to Play:
1. Enter a French sentence.
2. Guess the difficulty level (A1, A2, B1, B2, C1, C2).
3. Click 'Predict' to see if you guessed correctly.
4. Score points for correct guesses. 
""")

sentence = st.text_area("Enter a sentence to predict its difficulty:")

difficulty_options = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
user_guess = st.selectbox("Guess the difficulty level:", difficulty_options)

if st.button("Predict"):
    if sentence:
        # Transform the input sentence
        sentence_transformed = vectorizer.transform([sentence])
        
        # Predict the difficulty
        prediction = model.predict(sentence_transformed)[0]
        
        # Check the user's guess
        if user_guess == prediction:
            st.session_state.score += 1
            st.write(f"Correct! The difficulty level is {prediction}.")
        else:
            st.write(f"Incorrect. The difficulty level is {prediction}.")
        
        # Update round
        st.session_state.round += 1
    else:
        st.write("Please enter a sentence.")
