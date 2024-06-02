import random
import streamlit as st

# Define themes and words
themes = {
    'Animals': ['elephant', 'giraffe', 'tiger', 'zebra', 'lion', 'cheetah', 'monkey', 'kangaroo', 'panda', 'koala'],
    'Fruits': ['apple', 'banana', 'orange', 'grape', 'watermelon', 'pineapple', 'strawberry', 'blueberry', 'mango', 'papaya'],
    'Countries': ['canada', 'brazil', 'france', 'germany', 'india', 'japan', 'nigeria', 'russia', 'spain', 'turkey']
}

def choose_word(theme):
    return random.choice(themes[theme])

def display_word(word, guessed_letters):
    return ' '.join([letter if letter in guessed_letters else '_' for letter in word])

def draw_hangman(wrong_attempts):
    stages = [
        """
           ------
           |    |
                |
                |
                |
                |
        --------
        """,
        """
           ------
           |    |
           O    |
                |
                |
                |
        --------
        """,
        """
           ------
           |    |
           O    |
           |    |
                |
                |
        --------
        """,
        """
           ------
           |    |
           O    |
          /|    |
                |
                |
        --------
        """,
        """
           ------
           |    |
           O    |
          /|\\   |
                |
                |
        --------
        """,
        """
           ------
           |    |
           O    |
          /|\\   |
          /     |
                |
        --------
        """,
        """
           ------
           |    |
           O    |
          /|\\   |
          / \\   |
                |
        --------
        """
    ]
    return stages[wrong_attempts]

def hangman_game():
    st.title("Hangman Game")
    
    if 'theme' not in st.session_state:
        st.session_state.theme = None
        st.session_state.word = None
        st.session_state.guessed_letters = []
        st.session_state.wrong_attempts = 0
