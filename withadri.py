import random
import streamlit as st

def guess_the_number():
    st.title("Guess the Number Game")
    
    # Initialize session state variables
    if 'number_to_guess' not in st.session_state:
        st.session_state.number_to_guess = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.guess = 0
        st.session_state.feedback = ''
    
    st.write("Guess a number between 1 and 100")
    
    guess = st.number_input("Enter your guess", min_value=1, max_value=100, step=1)
    
    if st.button("Submit Guess"):
        st.session_state.attempts += 1
        st.session_state.guess = guess
        
        if guess < st.session_state.number_to_guess:
            st.session_state.feedback = "Too low! Try again."
        elif guess > st.session_state.number_to_guess:
            st.session_state.feedback = "Too high! Try again."
        else:
            st.session_state.feedback = f"Congratulations! You've guessed the number {st.session_state.number_to_guess} in {st.session_state.attempts} attempts."
            # Reset the game
            st.session_state.number_to_guess = random.randint(1, 100)
            st.session_state.attempts = 0
    
    st.write(st.session_state.feedback)

if __name__ == "__main__":
    guess_the_number()
