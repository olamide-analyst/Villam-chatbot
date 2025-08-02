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
pinecone_index = pc.Index("villambot")  

# Prompt template
system_prompt_template = """
Your name is VillamBot. you are a friendly and reliable assistant for Villam Hub. You are to Answer questions very very briefly and accurately.

Use the following information to answer the user's question:

{doc_content}

Provide very brief accurate and helpful response based on the provided information and your expertise.

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
        return "No relevant information found."

    return "\n".join(top_chunks).replace("{", "{{").replace("}", "}}")


# Main function to generate response
def generate_response(user_question, history=[]):
    """Generate a response using Pinecone + Gemini 2.0 with optional memory."""
    # 1. Retrieve the most relevant chunks from Pinecone
    context = retrieve_relevant_chunks(user_question)
    
    # 2. Format the system prompt using the retrieved content
    system_prompt = system_prompt_template.format(doc_content=context)
     
    # 3. Convert the passed chat history to LangChain format
    chat_history = ChatMessageHistory()
    for msg in history:
        if msg["role"] == "user":
            chat_history.add_user_message(msg["content"])
        elif msg["role"] == "assistant":
            chat_history.add_ai_message(msg["content"])
  
    # 4. Initialize memory for the chain
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=chat_history,
        return_messages=True
    )
    # 5. Define the full chat prompt
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(system_prompt),   # gives VillamBot its role + retrieved info
            MessagesPlaceholder(variable_name="chat_history"),          # allows past chat to be included
            HumanMessagePromptTemplate.from_template("{question}")      # inserts user's current question
        ]
    )
    # 6. Load the Gemini 2.0 Flash model
    chat_model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.1,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    # 7. Combine LLM, prompt, and memory into a conversation chain
    conversation = LLMChain(
        llm=chat_model,
        prompt=prompt,
        memory=memory,
        verbose=True  # helps with debugging/logging
    )
    # 8. Ask the question and get the final answer
    result = conversation({"question": user_question})
    return result.get("text", "Sorry, I couldn't find an answer.")
