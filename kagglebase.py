import streamlit as st
import joblib
import requests
from io import BytesIO
from sklearn.linear_model import LogisticRegressionCV  # Ensure this import is here
from sklearn.feature_extraction.text import TfidfVectorizer  # If you use it in other parts


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
st.title("Sentence Difficulty Predictor")

sentence = st.text_area("Enter a sentence to predict its difficulty:")

if st.button("Predict"):
    if sentence:
        # Transform the input sentence
        sentence_transformed = vectorizer.transform([sentence])
        
        # Predict the difficulty
        prediction = model.predict(sentence_transformed)
        
        # Display the prediction
        st.write(f"Predicted Difficulty: {prediction[0]}")
    else:
        st.write("Please enter a sentence.")

  
