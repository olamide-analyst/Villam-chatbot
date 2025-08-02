# 🌿 VillamBot – AI Chatbot for Villam Hub

VillamBot is an AI-powered assistant built for **Villam Hub**, a platform focused on sustainable agriculture and tree planting.  
This project uses **LangChain**, **Pinecone**, and **Gemini 2.0 Flash** to deliver relevant answers based only on Villam Hub’s verified data.

## Purpose

This repo contains the **backend logic** and **testing environment** for VillamBot. It is meant for:
- Internal team members 
- AI/ML enthusiasts exploring the RAG pipelines

## Project Structure

| File/Folder                 | Description |
|----------------------------|-------------|
| `.gitignore`               | Hides sensitive files like `.env` containing API keys |
| `requirements.txt`         | Lists all Python dependencies needed to run the chatbot |
| `villamhub_rag_dataset.csv`| Cleaned demo dataset containing Villam Hub knowledge |
| `rag_pipeline.ipynb`       | Main chatbot logic for exploration and debugging:<br> embeds queries, retrieves data, and generates responses |
| `villambot.py`             | Main chatbot logic for integration |
| `villambot_pinecone.ipynb` | Notebook to load and upsert the dataset into Pinecone |
| `test_chatbot.ipynb`       | Notebook to test chatbot responses interactively |

##  Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/villambot.git
cd villambot

```
 ### 2. Add Your Environment Variables

Create a `.env` file in the root directory with the following:

```
GOOGLE_API_KEY=your_google_generative_ai_key
PINECONE_API_KEY=your_pinecone_key
```

 `.env` is already excluded from version control via `.gitignore`.

### 3. Install Required Libraries

Make sure you're in your Python environment, then install dependencies:

```bash
pip install -r requirements.txt
```
## How to use 
### Step 1: Upsert the Dataset

Run `villambot_pinecone.ipynb` to upload the contents of `villamhub_rag_dataset.csv` to Pinecone.

### Step 2: Test the Chatbot

Use either:

* `test_chatbot.ipynb` for interactive testing
* Or `rag_pipeline.ipynb` to debug the full flow end-to-end


##  Backend Integration

For developers:
* All chatbot logic lives in `generate_response()` inside `villambot.py`

This is ready to be integrated with a **Flask**, **FastAPI**, or **Streamlit** frontend.

##  Notes

* The chatbot uses **Retrieval-Augmented Generation (RAG)**.
* Gemini 2.0 Flash is rate-limited on the free tier:

  * 15 requests/minute
  * 200 requests/day


## 🤝 Contributing

This project is maintained by the Villam Hub team.
For suggestions or pull requests, feel free to fork the repo or reach out directly.

