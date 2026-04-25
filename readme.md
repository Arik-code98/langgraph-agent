# RAG Agent — LangChain, LangGraph, and Groq

A tool-using AI agent built with LangGraph that follows the ReAct (Reason + Act) pattern. The agent decides at runtime whether to answer from its own knowledge or invoke a tool — either a date lookup or a semantic search over a document using ChromaDB. This builds on the previous LangChain RAG pipeline by introducing an autonomous decision-making layer on top of retrieval.

---

## How It Works

```
User Question
      |
      v
LangGraph ReAct Agent  (LLaMA 3.3 70B via Groq)
      |
      v
  Needs a tool?
  /           \
Yes            No
  |              |
  v              v
Which tool?   Answer directly
  /     \     from LLM knowledge
date   rag_search
tool      |
  |       v
  |   HuggingFaceEmbeddings
  |   ChromaDB similarity_search (k=2)
  |       |
  v       v
Tool result returned to agent
      |
      v
  Final Answer
```

---

## Tools

**get_current_date** — Returns today's date. Used when the question involves the current time or date.

**rag_search** — Performs semantic search over the ChromaDB vector store and retrieves the top-2 most relevant document chunks. Used when the question relates to the contents of the uploaded document.

---

## What Changed from the Previous Version

| | Previous (LCEL RAG pipeline) | This version (LangGraph Agent) |
|---|---|---|
| Execution model | Linear LCEL chain | LangGraph ReAct agent (graph-based) |
| Tool usage | None | `get_current_date` + `rag_search` |
| Retrieval trigger | Always retrieves | Agent decides when to retrieve |
| LLM role | Answer generator | Reasoning engine + decision maker |
| Pipeline control | Fixed sequence | Dynamic, condition-based graph |

---

## Tech Stack

- **LangGraph** - Graph-based agent orchestration with ReAct loop
- **LangChain** - Tool definitions, LLM integration, and chain utilities
- **LangChain Groq** - `ChatGroq` LLM wrapper
- **LangChain HuggingFace** - Embedding model wrapper (`all-MiniLM-L6-v2`)
- **LangChain Chroma** - Vector store integration
- **ChromaDB** - Underlying persistent vector database
- **Groq API** - LLM inference backend
- **LLaMA 3.3 70B Versatile** - The underlying large language model
- **python-dotenv** - Secure API key management

---

## Project Structure

```
project/
├── main.py                  # Agent definition and entry point
├── example.txt              # Source document (used to build the vector store)
├── chroma_langchain_db/     # Persisted ChromaDB vector store (must exist before running)
├── .env                     # Environment variables (not committed)
└── requirements.txt         # Project dependencies
```

---

## Setup and Installation

**1. Clone the repository**

```bash
git clone https://github.com/Arik-code98/langgraph-agent.git
cd langgraph-agent
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure environment variables**

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key from [https://console.groq.com](https://console.groq.com).

**4. Build the vector store**

The `chroma_langchain_db/` directory must exist before running the agent. The recommended approach is to run the [langchain-rag](https://github.com/Arik-code98/langchain-rag) project first — this will generate and persist the ChromaDB embeddings from `example.txt` into the correct directory.

Alternatively, add document loading, chunking, and embedding code directly to `main.py` before the agent is invoked.

**5. Run the agent**

```bash
python main.py
```

You will be prompted to enter a question. The agent will decide whether to use a tool or answer directly.

---

## Example Interactions

| Question | Agent behaviour |
|---|---|
| "What is today's date?" | Invokes `get_current_date` tool |
| "Summarize the document" | Invokes `rag_search` tool |
| "What is machine learning?" | Answers directly from LLM knowledge |

---

## Key Concepts Explored

- ReAct (Reason + Act) agent architecture
- Graph-based agent orchestration with LangGraph
- Runtime tool selection and conditional execution
- Wrapping retrieval as a callable LLM tool
- Combining LLM reasoning with external tool calls
- The difference between a fixed RAG chain and an agent-driven retrieval system

---

## Limitations and Improvements

- **Vector store must be pre-built**: The agent cannot ingest documents on its own — the ChromaDB directory must exist before running. Integrating document loading into the agent setup would make it self-contained.
- **Two tools only**: The current toolset is minimal. Adding tools for web search, calculation, or external APIs would significantly expand what the agent can handle.
- **No memory**: Each run is stateless — the agent has no memory of prior questions. Adding conversation memory would enable multi-turn interactions.
- **CLI only**: The agent runs in the terminal. Wrapping it in a FastAPI endpoint with a frontend would make it deployable as a web application.
- **Single document**: The RAG tool searches over one document's embeddings. Supporting multiple documents with per-document routing would make the agent more practical.
