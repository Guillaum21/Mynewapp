import random
import streamlit as st

def get_computer_choice():
    return random.choice(['Rock', 'Paper', 'Scissors'])

def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "It's a tie!"
    elif (player_choice == 'Rock' and computer_choice == 'Scissors') or \
         (player_choice == 'Paper' and computer_choice == 'Rock') or \
         (player_choice == 'Scissors' and computer_choice == 'Paper'):
        return "You win!"
    else:
        return "You lose!"

def play_game():
    st.title("Rock, Paper, Scissors Game")
    
    if 'computer_choice' not in st.session_state:
        st.session_state.computer_choice = ''
        st.session_state.result = ''
    
    st.write("Choose Rock, Paper, or Scissors:")
    player_choice = st.selectbox("Your choice:", ['Rock', 'Paper', 'Scissors'])
    
    if st.button("Play"):
        st.session_state.computer_choice = get_computer_choice()
        st.session_state.result = determine_winner(player_choice, st.session_state.computer_choice)
    
    if st.session_state.computer_choice:
        st.write(f"Computer chose: {st.session_state.computer_choice}")
        st.write(st.session_state.result)

if __name__ == "__main__":
    play_game()
