import streamlit as st

# Function to simulate a response from an AI (placeholder)
def get_ai_response(message):
    # You would integrate with an actual AI model here
    return "This is a simulated response to: " + message

# Main function to run the Streamlit app
def main():
    st.title('Chat with AI')

    # Session state to store chat history
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # Text input for user message
    user_message = st.text_input("You:", key="input")

    # On 'Enter', append the message and get a response
    if st.session_state.input:
        st.session_state.history.append(("You", user_message))
        # Simulate an AI response
        ai_response = get_ai_response(user_message)
        st.session_state.history.append(("AI", ai_response))
        # Clear the input box
        st.session_state.input = ""

    # Display chat history
    for role, message in st.session_state.history:
        if role == "You":
            st.text_area("", value=message, height=25, key=message[:10])
        else:
            st.text_area("", value=message, height=25, key=message[:10], style={"text-align": "right"})

# Run the main function
if __name__ == '__main__':
    main()
