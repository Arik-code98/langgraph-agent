# RAG Agent using LangChain, LangGraph, and Groq

## Overview

This project implements a **tool-using AI agent** powered by a Large Language Model (LLaMA 3 via Groq API).
The agent follows the **ReAct (Reason + Act)** pattern to decide when to use tools and when to rely on its own knowledge.

It combines:

* **LLM reasoning**
* **Tool usage**
* **Retrieval-Augmented Generation (RAG)** using a vector database

---

## Features

* ReAct-based intelligent agent using LangGraph
* Tool calling capability (date tool + RAG search tool)
* Semantic search over documents using ChromaDB
* Uses HuggingFace embeddings for vector representation
* Falls back to general LLM knowledge when no tool is needed
* Interactive CLI-based question answering

---

## Tech Stack

* Python
* LangChain
* LangGraph
* Groq API (LLaMA 3)
* HuggingFace Embeddings
* ChromaDB
* python-dotenv

---

## Project Structure

```
.
├── main.py
├── chroma_langchain_db/
├── example.txt
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Arik-code98/langgraph-agent.git
cd langgraph-agent
```

### 2. Create a virtual environment (optional)

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Setup

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

## Important Note (RAG Setup)

The folder `chroma_langchain_db` must exist before running the agent.

You have two options:

### Option 1 (Recommended)

Generate the vector database using your **langchain-rag project** first.
This will create the `chroma_langchain_db` directory with embeddings.

### Option 2

Use `example.txt` and add code to:

* Load the document
* Split it into chunks
* Generate embeddings
* Store them in ChromaDB

This setup ensures the `rag_search` tool can retrieve relevant context.

---

## How It Works

### Tools

1. **get_current_date**

   * Returns today's date

2. **rag_search**

   * Performs semantic search on stored documents
   * Retrieves top relevant chunks

---

### Agent Flow

* User asks a question
* Agent decides:

  * Use a tool (date or RAG search), OR
  * Answer directly using LLM knowledge
* Executes the action
* Returns the final response

---

## Running the Project

```bash
python main.py
```

Example:

```
Ask a question: What is in the document?
```

---

## Example Capabilities

* "What is today's date?" → Uses date tool
* "Summarize the document" → Uses RAG tool
* "What is AI?" → Answers from general knowledge

---

## Key Concepts Learned

* ReAct agent architecture
* Tool calling with LLMs
* Retrieval-Augmented Generation (RAG)
* Vector databases and embeddings
* Combining reasoning + retrieval in one system

---

## Future Improvements

* Add more tools (calculator, APIs, etc.)
* Support multiple documents
* Build a web interface (FastAPI or Streamlit)
* Add memory and session handling