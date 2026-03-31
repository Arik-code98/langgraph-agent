from langchain_core.tools import tool
from datetime import date
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langgraph.prebuilt import create_react_agent
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",
)

@tool
def get_current_date() -> str:
    """Returns today's date."""
    return str(date.today())

@tool
def rag_search(query: str) -> str:
    """Use this tool to search the document for any information."""
    results = vector_store.similarity_search(query, k=2)
    return "\n\n".join([doc.page_content for doc in results])

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
tools = [get_current_date, rag_search]
llm_with_tools = llm.bind_tools(tools)

agent = create_react_agent(llm, tools)

question = input("Ask a question: ")
response = agent.invoke({"messages": [{"role": "user", "content": question}]})
print(response["messages"][-1].content)