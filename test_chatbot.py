from villambot_rag import generate_response
import streamlit as st

# Simulate Streamlit session state (chat history)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "user", "content": "Hi, what services does Villam Hub offer?"},
        {"role": "assistant", "content": "Villam Hub offers farming kits, a tree planting service, and farming-as-a-service."}
    ]

# User asks a new question
question = "Tell me more about the tree planting service."

# Get AI-generated response
response = generate_response(question)

# Print the chatbot’s answer
print("\nVillamBot says:\n")
print(response)

