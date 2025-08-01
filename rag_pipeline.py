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
You are VillamBot, a warm, grounded, and reliable assistant for Villam Hub.
Your role is to support users on their journey to sustainable living by helping them understand our platform services,
farming tips, and how to grow food at home.

Use the following information to answer the user's question:

{doc_content}

Provide very brief accurate and helpful farming response based on the provided information and your expertise.

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
def generate_response(user_question: str, chat_history: list = []) -> str:
    """
    user_question: User's latest message
    chat_history: List of previous messages like:
        [{"role": "user", "content": "Hi"}, {"role": "assistant", "content": "Hello"}]
    """

    context = retrieve_relevant_chunks(user_question)
    system_prompt = system_prompt_template.format(doc_content=context)

    # Build LangChain memory
    chat_mem = ChatMessageHistory()
    for msg in chat_history:
        if msg["role"] == "user":
            chat_mem.add_user_message(msg["content"])
        elif msg["role"] == "assistant":
            chat_mem.add_ai_message(msg["content"])

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=chat_mem,
        return_messages=True
    )

    # Full conversation prompt
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
    )

    # Gemini 2.0 Flash LLM
    chat_model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.1,
        google_api_key=GOOGLE_API_KEY
    )

    # Build and run chain
    conversation = LLMChain(
        llm=chat_model,
        prompt=prompt,
        memory=memory,
        verbose=False
    )

    result = conversation({"question": user_question})
    return result.get("text", "Sorry, I couldn't find an answer.")
