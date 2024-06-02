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
        st.session_state.max_attempts = 6
        st.session_state.game_over = False

    if st.session_state.theme is None:
        theme = st.selectbox("Select a theme:", list(themes.keys()))
        if st.button("Start Game"):
            st.session_state.theme = theme
            st.session_state.word = choose_word(theme)
            st.session_state.guessed_letters = []
            st.session_state.wrong_attempts = 0
            st.session_state.game_over = False
    
    if st.session_state.theme is not None:
        st.write(f"Theme: {st.session_state.theme}")
        st.write("Guess the word:")
        st.write(display_word(st.session_state.word, st.session_state.guessed_letters))
        st.text(draw_hangman(st.session_state.wrong_attempts))
        
        if st.session_state.wrong_attempts >= st.session_state.max_attempts:
            st.write(f"You lost! The word was {st.session_state.word}.")
            st.session_state.game_over = True
        
        if not st.session_state.game_over:
            letter = st.text_input("Enter a letter:").lower()
            
            if st.button("Guess"):
                if letter in st.session_state.guessed_letters:
                    st.write("You already guessed that letter.")
                elif letter in st.session_state.word:
                    st.session_state.guessed_letters.append(letter)
                    st.write("Good guess!")
                else:
                    st.session_state.guessed_letters.append(letter)
                    st.session_state.wrong_attempts += 1
                    st.write("Wrong guess!")

                if all([letter in st.session_state.guessed_letters for letter in st.session_state.word]):
                    st.write(f"Congratulations! You guessed the word: {st.session_state.word}")
                    st.session_state.game_over = True
        
        st.write(f"Wrong attempts: {st.session_state.wrong_attempts}/{st.session_state.max_attempts}")

        if st.button("Reset Game"):
            st.session_state.theme = None
            st.session_state.word = None
            st.session_state.guessed_letters = []
            st.session_state.wrong_attempts = 0
            st.session_state.game_over = False

if __name__ == "__main__":
    hangman_game()
