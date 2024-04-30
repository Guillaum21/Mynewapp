import streamlit as st

def determine_french_level(sentence):
    words = sentence.split()
    num_words = len(words)
    unique_words = len(set(words))
    average_word_length = sum(len(word) for word in words) / num_words if num_words else 0
    lexical_diversity = unique_words / num_words if num_words else 0

    # Determine initial level based on the number of words
    if num_words < 5:
        level = "Débutant (A1)"
    elif 5 <= num_words < 10:
        level = "Élémentaire (A2)"
    elif 10 <= num_words < 15:
        level = "Intermédiaire (B1)"
    elif 15 <= num_words < 20:
        level = "Intermédiaire Avancé (B2)"
    elif 20 <= num_words < 25:
        level = "Avancé (C1)"
    else:
        level = "Expérimenté (C2)"

    # Adjust the level based on average word length
    if average_word_length > 6:
        if "Débutant" in level or "Élémentaire" in level:
            level = "Intermédiaire (B1)"
        elif "Intermédiaire" in level:
            level = "Intermédiaire Avancé (B2)"
        elif "Intermédiaire Avancé" in level:
            level = "Avancé (C1)"
        elif "Avancé" in level:
            level = "Expérimenté (C2)"
    
    # Adjust the level based on lexical diversity
    if lexical_diversity > 0.5:
        if "Débutant" in level:
            level = "Élémentaire (A2)"
        elif "Élémentaire" in level:
            level = "Intermédiaire (B1)"
        elif "Intermédiaire" in level:
            level = "Intermédiaire Avancé (B2)"
        elif "Intermédiaire Avancé" in level:
            level = "Avancé (C1)"
        elif "Avancé" in level:
            level = "Expérimenté (C2)"

    return level

# Streamlit page configuration
st.set_page_config(page_title='Détecteur de Niveau de Français', layout='wide')

# Title of the app
st.title('Détecteur de Niveau de Français')

# App description
st.write('Veuillez écrire une courte phrase en français dans la zone de texte ci-dessous et cliquer sur le bouton pour évaluer votre niveau de français.')

# User input field
user_input = st.text_input('Écrivez une courte phrase ici', '')

# Button to process input and display results
if st.button('Évaluer'):
    if user_input:
        # Call the function that processes the input to determine the French level
        french_level = determine_french_level(user_input)
        # Display the user's input and the calculated French level
        st.write(f'Votre phrase était: "{user_input}"')
        st.success(f'Votre niveau de français automatique est: {french_level}')
    else:
        st.error('Veuillez entrer une phrase avant de cliquer sur le bouton évaluer.')
