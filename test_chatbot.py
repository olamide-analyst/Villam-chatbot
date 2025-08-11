import streamlit as st
from vchat import generate_response  

# --- Initialize session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hi there! I'm V-Chat. How can I help you today?"}
    ]

# Title and instructions
st.title("🌿 V-Chat – Villam Hub Assistant")
st.write("Ask about urban farming, tree planting, or anything Villam Hub-related!")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
user_input = st.chat_input("Ask a question...")
if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Generate response from Vchat
    with st.spinner("Thinking..."):
        response = generate_response(user_input, history=st.session_state.chat_history)

    # Show assistant reply
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})
