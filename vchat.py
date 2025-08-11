import os
import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from pinecone import Pinecone

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize services
embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
pc = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pc.Index("vchat")  

# Prompt template
system_prompt_template = """
You are V-Chat, the AI assistant for Villam Hub, a platform focused on sustainable agriculture, urban farming, and tree planting.

Goals:
- Answer in 1-3 concise sentences (max ~60 words).
- Ground every answer strictly in the Context. Do not invent facts.
- If the Context is insufficient, say so briefly and ask one clarifying question if helpful.

Context:
{doc_content}

Response rules:
- Start with the direct answer in plain language.
- If suggesting actions, list up to three short bullet points.
- Keep tone helpful, neutral, and professional.
- If the Context contains 'No relevant information found.', reply: "I don't have enough info from the documents to answer that." Optionally add one next step.
"""

# Get top 3 relevant chunks from Pinecone
def retrieve_relevant_chunks(question: str) -> str:
    query_vector = embed_model.embed_query(question)
    query_vector = [float(x) for x in query_vector]

    results = pinecone_index.query(
        vector=query_vector,
        top_k=3,
        include_metadata=True
    )

    top_chunks = [match["metadata"].get("text", "") for match in results.get("matches", [])]

    if not top_chunks:
        return "No relevant information found." # referenced in system prompt


    clean_chunk = [f"- {chunk.strip()}" for chunk in top_chunks]
    return "\n".join(clean_chunk).replace("{", "{{").replace("}", "}}")


# Main function to generate response
def generate_response(user_question, history=[]):
    """Generate a response using Pinecone + Gemini 2.0 with optional memory."""
    # Retrieve the most relevant chunks from Pinecone
    context = retrieve_relevant_chunks(user_question)
    
    # Format the system prompt using the retrieved content
    system_prompt = system_prompt_template.format(doc_content=context)
     
    # Convert the passed chat history to LangChain format
    chat_history = ChatMessageHistory()
    for msg in history:
        if msg["role"] == "user":
            chat_history.add_user_message(msg["content"])
        elif msg["role"] == "assistant":
            chat_history.add_ai_message(msg["content"])

    # Initialize memory for the chain
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=chat_history,
        return_messages=True
    )
    # Define the full chat prompt
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(system_prompt),   # gives VillamBot its role + retrieved info
            MessagesPlaceholder(variable_name="chat_history"),          # allows past chat to be included
            HumanMessagePromptTemplate.from_template("{question}")      # inserts user's current question
        ]
    )
    # Load the Gemini 2.0 Flash model
    chat_model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.1,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    # Combine LLM, prompt, and memory into a conversation chain
    conversation = LLMChain(
        llm=chat_model,
        prompt=prompt,
        memory=memory,
        verbose=True  # helps with debugging/logging
    )
    # Ask the question and get the final answer
    result = conversation({"question": user_question})
    return result.get("text", "Sorry, I couldn't find an answer.")
