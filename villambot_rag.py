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
def generate_response(question):
    """Generate a response using Pinecone retrieval and Gemini 2.0 Flash."""
    import asyncio

    # Embed the user’s question
    query_embed = embed_model.embed_query(question)
    query_embed = [float(val) for val in query_embed]

    # Query Pinecone
    results = pinecone_index.query(
        vector=query_embed,
        top_k=3,
        include_values=False,
        include_metadata=True
    )

    # Extract matched content
    doc_contents = []
    print("\n" + "="*50)
    print(f"RETRIEVED DOCUMENTS FOR: '{question}'")
    for i, match in enumerate(results.get('matches', [])):
        text = match['metadata'].get('text', '')
        doc_contents.append(text)
        print(f"\nDOCUMENT {i+1}:\n{text}\n")
    print("="*50 + "\n")

    # Prepare retrieved content
    doc_content = "\n".join(doc_contents).replace('{', '{{').replace('}', '}}') \
        if doc_contents else "No relevant information found."

    # Format system prompt
    formatted_prompt = system_prompt_template.format(doc_content=doc_content)

    # Prepare Gemini model
    chat = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.1,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # Create the final prompt for Gemini
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(formatted_prompt),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
    )

    # No memory
    chain = LLMChain(llm=chat, prompt=prompt, verbose=True)

    # Run and return result
    result = chain.invoke({"question": question})
    return result.get("text", "Sorry, I couldn't find a good answer.")
