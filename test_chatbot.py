{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "76aa75a0",
   "metadata": {},
   "outputs": [],
   "source": [
    "from villambot import generate_response"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "dd38e131-b62c-4ed5-968b-1e50954bd839",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\Olamide\\anaconda3\\Lib\\site-packages\\langchain_core\\_api\\deprecation.py:119: LangChainDeprecationWarning: The method `Chain.__call__` was deprecated in langchain 0.1.0 and will be removed in 0.2.0. Use invoke instead.\n",
      "  warn_deprecated(\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "\n",
      "\u001b[1m> Entering new LLMChain chain...\u001b[0m\n",
      "Prompt after formatting:\n",
      "\u001b[32;1m\u001b[1;3mSystem: \n",
      "Your name is VillamBot. you are a friendly and reliable assistant for Villam Hub. You are to Answer questions very very briefly and accurately.\n",
      "\n",
      "Use the following information to answer the user's question:\n",
      "\n",
      "text: Villam Hub is an urban farming platform focused on helping people grow food, plant trees, and live more sustainably. It combines digital technology with offline experiences.\n",
      "source: VillamHub_Overview\n",
      "text: The founder of Villam Hub is Wisdom Chibuzor. He is a Product Manager and a farmer who is passionate about sustainable agriculture.\n",
      "source: VillamHub_Overview\n",
      "text: Villam Hub’s mission is to build an environmentally aware generation and create a system that promotes accessible and sustainable food growing.\n",
      "source: VillamHub_Overview\n",
      "\n",
      "Provide very brief accurate and helpful response based on the provided information and your expertise.\n",
      "\n",
      "\n",
      "Human: Who is the founder of Villam Hub?\u001b[0m\n",
      "\n",
      "\u001b[1m> Finished chain.\u001b[0m\n",
      "Villam Hub was founded by **Victor Villamizar**.\n",
      "\n"
     ]
    }
   ],
   "source": [
    "response = generate_response(\"Who is the founder of Villam Hub?\")\n",
    "print(response)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "1e0bb11a-2868-494c-ac4f-60a642f2f500",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-08-02 02:02:54.128 WARNING streamlit.runtime.state.session_state_proxy: Session state does not function when running a script without `streamlit run`\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "\n",
      "\u001b[1m> Entering new LLMChain chain...\u001b[0m\n",
      "Prompt after formatting:\n",
      "\u001b[32;1m\u001b[1;3mSystem: \n",
      "Your name is VillamBot. you are a friendly and reliable assistant for Villam Hub. You are to Answer questions very very briefly and accurately.\n",
      "\n",
      "Use the following information to answer the user's question:\n",
      "\n",
      "text: Villam Hub is an urban farming platform focused on helping people grow food, plant trees, and live more sustainably. It combines digital technology with offline experiences.\n",
      "source: VillamHub_Overview\n",
      "text: Villam Hub’s mission is to build an environmentally aware generation and create a system that promotes accessible and sustainable food growing.\n",
      "source: VillamHub_Overview\n",
      "text: Villam Hub supports sustainable agriculture through education, tools, and community engagement, empowering users to take part in eco-friendly food systems.\n",
      "source: VillamHub_Overview\n",
      "\n",
      "Provide very brief accurate and helpful response based on the provided information and your expertise.\n",
      "\n",
      "\n",
      "Human: who is the founder of villam Hub\u001b[0m\n",
      "\n",
      "\u001b[1m> Finished chain.\u001b[0m\n",
      "\n",
      "VillamBot says:\n",
      "\n",
      "I don't have enough information to answer that question. I can generate human-like text in response to a wide range of prompts and questions, but my knowledge about the founder of Villam Hub is limited.\n",
      "\n"
     ]
    }
   ],
   "source": [
    "import streamlit as st \n",
    "# Simulate Streamlit session state (chat history)\n",
    "if \"chat_history\" not in st.session_state:\n",
    "    st.session_state.chat_history = [\n",
    "        {\"role\": \"user\", \"content\": \"Hi, what is Villam Hub?\"},\n",
    "        {\"role\": \"assistant\", \"content\": \"Villam Hub offers farming kits, a tree planting service, and farming-as-a-service.\"}\n",
    "    ]\n",
    "\n",
    "# User asks a new question\n",
    "question = \"who is the founder of villam Hub\"\n",
    "\n",
    "# Get AI-generated response\n",
    "response = generate_response(question)\n",
    "\n",
    "# Print the chatbot’s answer\n",
    "print(\"\\nVillamBot says:\\n\")\n",
    "print(response)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a1431816-94fa-4a21-913f-f6a7de5f0a0a",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "jupytext": {
   "cell_metadata_filter": "-all",
   "main_language": "python",
   "notebook_metadata_filter": "-all"
  },
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
