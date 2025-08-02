# 🌿 VillamBot – AI Chatbot for Villam Hub

VillamBot is the AI-powered assistant built for **Villam Hub**, a platform focused on sustainable agriculture and tree planting.  

This project uses **LangChain**, **Pinecone**, and **Gemini 2.0 Flash** to deliver relevant answers based only on Villam Hub’s verified data.

The chatbot:

* Takes a user's question.
* Searches the vector database (Pinecone) for relevant information from the `villamhub_rag_dataset.csv` document.
* Uses AI model (Google's Gemini 2.0 Flash) to understand the question and the retrieved information.
* Generates a concise and helpful answer.

GitHub repository: https://github.com/olamide-analyst/Villam-chatbot

 ## Features 
* AI-Powered Responses: uses Google's Gemini 2.0 Flash model for intelligent answers.
* Context-Aware: Retrieves relevant information from  `villamhub_rag_dataset.csv` using Pinecone vector search.
* Conversational Memory: Remembers previous parts of the conversation to provide more relevant follow-up answers.

## Tech Stack

* Python: The primary programming language.
* Langchain: A framework to simplify building applications with Large Language Models (LLMs).
* Google Generative AI (Gemini 2.0 Flash): The LLM used for understanding and generating text.
* GoogleGenerativeAIEmbeddings: For converting text into numerical representations (embeddings) that AI can understand.
* Pinecone: A vector database used to store and efficiently search through the embeddings of our knowledge base.
* CSVLoader: To load and read text from CSV files.
* Dotenv: To manage sensitive information like API keys.

## Purpose

This repo contains the **backend logic** and **testing environment** for VillamBot. It is meant for:
- Internal team members 
- AI/ML enthusiasts exploring the RAG pipelines


## Project Structure

| File/Folder                 | Description |
|----------------------------|-------------|
| `.gitignore`               | Hides the `.env` containing API keys |
| `.env.example`              | API keys template                     |
| `requirements.txt`         | Lists all Python libraries needed to run the chatbot |
| `villamhub_rag_dataset.csv`| Cleaned demo dataset containing Villam Hub knowledge |
| `villambot_pipeline.ipynb`       | Main chatbot logic for exploration and debugging:<br> embeds queries, retrieves data, and generates responses |
| `villambot.py`             | Main chatbot logic for integration |
| `villambot_pinecone.ipynb` | Notebook to load and upsert the dataset into Pinecone |
| `test_chatbot.py`| Notebook to test chatbot responses interactively |

##  Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/olamide-analyst/Villam-chatbot
cd villambot

```
 ### 2. Add Your Environment Variables (.env file)

Add API keys to `.env.example` file and rename to `.env` :

```
GOOGLE_API_KEY=google_generative_ai_key
PINECONE_API_KEY=pinecone_key
```

 `.env` is already excluded from version control via `.gitignore`.

### 3. Install Required Libraries
Install all the Python packages listed in  `requirements.txt`

```bash
pip install -r requirements.txt
```
## How to use 
The project has two main Python scripts:

*  `villambot_pinecone.ipynb`: This script processes the dataset `villamhub_rag_dataset.csv`, converts its content into embeddings/vectors (numerical representations), and stores(upsert) them in the Pinecone vector database. You only need to run this once (or whenever the dataset document changes).
  
*  `villambot_pipeline.ipynb` or `villambot.py`: These runs the chatbot engine logic (retrieval + Gemini 2.0 generation).
  
### Step 1: Upsert the Dataset to pinecone

Run `villambot_pinecone.ipynb` to upload the contents of `villamhub_rag_dataset.csv` to Pinecone.

### Step 2: Test the Chatbot

Use either:

* `test_chatbot.py` for interactive testing
```bash
streamlit run test_chatbot.py
```
  
* Or `villambot_pipeline.ipynb` to debug the full flow end-to-end


##  Backend Integration

For developers:
* All chatbot logic lives in `generate_response()` inside `villambot.py`

This is ready to be integrated with a **Flask**, **FastAPI**, or **Streamlit** frontend.

##  Notes

* The chatbot uses **Retrieval-Augmented Generation (RAG)**.
* Gemini 2.0 Flash is rate-limited on the free tier:

  * 15 requests/minute
  * 200 requests/day


##  Contributing

This project is maintained by the Villam Hub team.
For suggestions or pull requests, feel free to fork the repo or reach out directly.

## References

* HIV Chatbot Project Example: http://github.com/ajisco/DSA_HIV
* YouTube Gemini + LangChain Tutorial: https://youtu.be/DFjuV2YBoe4?si=2ND-frk2_Wjfv9FF