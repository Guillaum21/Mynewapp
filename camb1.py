import streamlit as st

def determine_cambridge_level(sentence):
    words = sentence.split()
    num_words = len(words)
    unique_words = len(set(words))
    average_word_length = sum(len(word) for word in words) / num_words if num_words else 0
    lexical_diversity = unique_words / num_words if num_words else 0
    
  
    # Adjust the level based on the number of words
    if num_words < 5:
        level = "Beginner (A1)"
    elif 5 <= num_words < 10:
        level = "Elementary (A2)"
    elif 10 <= num_words < 15:
        level = "Intermediate (B1)"
    elif 15 <= num_words < 20:
        level = "Upper Intermediate (B2)"
    elif 20 <= num_words < 25:
        level = "Advanced (C1)"
    else:
        level = "Proficient (C2)"

    # Refine the level based on average word length and lexical diversity
    if average_word_length > 6:
        if "Beginner" in level or "Elementary" in level:
            level = "Intermediate (B1)"
        elif "Intermediate" in level:
            level = "Upper Intermediate (B2)"
        elif "Upper Intermediate" in level:
            level = "Advanced (C1)"
        elif "Advanced" in level:
            level = "Proficient (C2)"
    
    if lexical_diversity > 0.5:
        if "Beginner" in level:
            level = "Elementary (A2)"
        elif "Elementary" in level:
            level = "Intermediate (B1)"
        elif "Intermediate" in level:
            level = "Upper Intermediate (B2)"
        elif "Upper Intermediate" in level:
            level = "Advanced (C1)"
        elif "Advanced" in level:
            level = "Proficient (C2)"

return level

# Set page configuration for Streamlit
st.set_page_config(page_title='Cambridge Level Detector', layout='wide')

# Title for the app
st.title('Cambridge Level Detector')

# Instructions or description
st.write('Please write a short sentence in the text box below and click the button to evaluate your Cambridge level.')

# Text input field
user_input = st.text_input('Write a short sentence here', '')

# Button to process input
if st.button('Evaluate'):
    if user_input:
        # Call the function that processes the input to determine the Cambridge level
        cambridge_level = determine_cambridge_level(user_input)
        st.write(f'Your input was: "{user_input}"')
        # Display the determined Cambridge level
        st.success(f'Your automatic Cambridge level is: {cambridge_level}')
    else:
        st.error('Please enter a sentence before clicking the evaluate button.')

# Optionally, you can use st.empty() to reserve space for output that will change based on user interaction
placeholder = st.empty()
