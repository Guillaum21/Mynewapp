import random
import streamlit as st

def choose_word():
    words = ['python', 'streamlit', 'hangman', 'challenge', 'repository']
    return random.choice(words)

def display_word(word, guessed_letters):
    return ' '.join([letter if letter in guessed_letters else '_' for letter in word])

def hangman_game():
    st.title("Hangman Game")
    
    if 'word' not in st.session_state:
        st.session_state.word = choose_word()
        st.session_state.guessed_letters = []
        st.session_state.wrong_attempts = 0
        st.session_state.max_attempts = 6
        st.session_state.game_over = False

    st.write("Guess the word:")
    st.write(display_word(st.session_state.word, st.session_state.guessed_letters))
    
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
        st.session_state.word = choose_word()
        st.session_state.guessed_letters = []
        st.session_state.wrong_attempts = 0
        st.session_state.game_over = False

if __name__ == "__main__":
    hangman_game()
