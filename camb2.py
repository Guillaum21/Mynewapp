import streamlit as st

def determine_french_level(sentence):
    words = sentence.split()
    num_words = len(words)
    unique_words = len(set(words))
    average_word_length = sum(len(word) for word in words) / num_words if num_words else 0
    lexical_diversity = unique_words / num_words if num_words else 0

    level = "Débutant (A1)"  # Default to beginner if no other criteria met
    if num_words < 5:
        points = 5
    elif 5 <= num_words < 10:
        points = 10
        level = "Élémentaire (A2)"
    elif 10 <= num_words < 15:
        points = 15
        level = "Intermédiaire (B1)"
    elif 15 <= num_words < 20:
        points = 20
        level = "Intermédiaire Avancé (B2)"
    elif 20 <= num_words < 25:
        points = 25
        level = "Avancé (C1)"
    else:
        points = 30
        level = "Expérimenté (C2)"

    additional_points = (average_word_length * 1.5) + (lexical_diversity * 10)
    total_points = points + additional_points
    return total_points, level

st.set_page_config(page_title='Jeu de Complexité des Phrases Françaises', layout='wide')
st.title('Jeu de Complexité des Phrases Françaises')

st.write('''
Écrivez la phrase la plus complexe possible en français.
Plus la phrase est complexe, plus vous gagnez de points.
Plus vous avez de points, plus la voiture a d'électricité.
Plus la voiture a d'électricité, plus elle peut continuer à rouler.
Quand vous n'avez plus d'électricité, la voiture s'arrête et le jeu vous donne votre score final.
''')

if 'total_points' not in st.session_state:
    st.session_state['total_points'] = 0
    st.session_state['distance'] = 0

user_input = st.text_input('Écrivez une phrase ici', '')

if st.button('Soumettre la phrase'):
    if user_input:
        points, level = determine_french_level(user_input)
        st.session_state['total_points'] += points
        st.session_state['distance'] += points * 10  # Each point adds 10 meters to the car's travel
        st.write(f'Points for this sentence: {points}')
        st.write(f'French Level: {level}')
        st.write(f'Total Points: {st.session_state["total_points"]}')
        st.write(f'Distance: {st.session_state["distance"]} meters')
    else:
        st.error('Veuillez entrer une phrase avant de soumettre.')

if st.button('Arrêter le jeu et afficher le score final'):
    st.write(f'Final Score: {st.session_state["total_points"]} Points')
    st.write(f'Total Distance: {st.session_state["distance"]} meters')
    st.session_state['total_points'] = 0
    st.session_state['distance'] = 0  # Reset the game
