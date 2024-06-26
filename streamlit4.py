import streamlit as st
import time

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

def boat_progress(distance, target=2000):
    progress_percentage = min(distance / target * 100, 100)
    return f"""
    <div style="width: 100%; background: lightblue; position: relative; height: 50px; border-radius: 10px;">
        <div style="position: absolute; width: {progress_percentage}%; height: 100%; background: linear-gradient(to right, #0078D7, #83C5BE);">
            <span style="position: absolute; right: 0; transform: translateX(50%); font-size: 24px;">⛵</span> <!-- Increased size for the boat -->
        </div>
        <span style="position: absolute; right: 0; transform: translateX(-100%); color: black; font-size: 24px;">🏁</span> <!-- Increased size for the flag -->
    </div>
    """

st.set_page_config(page_title='Jeu de Complexité des Phrases Françaises', layout='wide')
st.title('Jeu de Complexité des Phrases Françaises')

st.write('''
Write as complex sentences as possible in French within 60 seconds to push the boat as far as possible.
The goal is to reach 2000 meters.
''')

if 'timer_started' not in st.session_state:
    st.session_state['timer_started'] = False
    st.session_state['total_points'] = 0
    st.session_state['distance'] = 0
    st.session_state['time_left'] = 60

if st.button('Start') and not st.session_state['timer_started']:
    st.session_state['timer_started'] = True
    st.session_state['start_time'] = time.time()

if st.session_state['timer_started']:
    elapsed_time = time.time() - st.session_state['start_time']
    st.session_state['time_left'] = max(60 - elapsed_time, 0)
    if st.session_state['time_left'] <= 0:
        st.session_state['timer_started'] = False
        st.write(f'Final Score: {st.session_state["total_points"]} Points')
        st.write(f'Total Distance: {st.session_state["distance"]} meters')
        st.session_state['total_points'] = 0
        st.session_state['distance'] = 0  # Reset game

user_input = st.text_input('Write a short sentence here', '')
sentence_level = st.empty()

if st.session_state['timer_started'] and st.button('Submit Sentence'):
    if user_input:
        points, level = determine_french_level(user_input)
        st.session_state['total_points'] += points
        st.session_state['distance'] += points * 10  # Each point adds 10 meters to the boat's travel
        st.write(f'Points for this sentence: {points}')
        sentence_level.text(f'French Level: {level}')
        st.write(f'Total Points: {st.session_state["total_points"]}')
        st.write(f'Distance: {st.session_state["distance"]} meters')
        st.markdown(boat_progress(st.session_state['distance'], 5000), unsafe_allow_html=True)
    else:
        st.error('Please enter a sentence before submitting.')

if st.session_state['time_left'] > 0:
    st.write(f'Time Left: {int(st.session_state["time_left"])} seconds')
else:
    st.write("Time is up! Submit your last sentence or restart the game.")
