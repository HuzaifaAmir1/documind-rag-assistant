from typing import Any, Dict
import os
from dotenv import load_dotenv
#from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.tools import tool
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import create_react_agent

load_dotenv()

# Initialize embeddings
# 
# embeddings = OpenAIEmbeddings(
#     model="text-embedding-004",
#     openai_api_key=os.environ.get("OPENAI_API_KEY"),
#     openai_api_base=os.environ.get("OPENAI_BASE_URL"),
# )

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.environ.get("OPENAI_API_KEY"),
)

# Initialize vector store
vectorstore = PineconeVectorStore(
    index_name="langchain-docs-2026", embedding=embeddings
)

# Initialize chat model (Grok)
# 
llm = ChatOpenAI(
    model="gemini-2.0-flash-lite",
    temperature=0,
    openai_api_key=os.environ.get("OPENAI_API_KEY"),
    openai_api_base=os.environ.get("OPENAI_BASE_URL"),
)

@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve relevant documentation to help answer user queries about LangChain."""
    retrieved_docs = vectorstore.as_retriever().invoke(query, k=4)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata.get('source', 'Unknown')}\n\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


def run_llm(query: str) -> Dict[str, Any]:
    system_prompt = (
        "You are DocuMind, a precise AI assistant for LangChain documentation. "
        "Always use the retrieve_context tool to find relevant documentation before answering. "
        "Cite the sources you use. "
        "If you cannot find the answer, say: I could not find this in the LangChain documentation."
    )

    agent = create_react_agent(llm, tools=[retrieve_context], prompt=system_prompt)

    messages = [{"role": "user", "content": query}]
    response = agent.invoke({"messages": messages})

    answer = response["messages"][-1].content

    context_docs = []
    for message in response["messages"]:
        if isinstance(message, ToolMessage) and hasattr(message, "artifact"):
            if isinstance(message.artifact, list):
                context_docs.extend(message.artifact)

    return {
        "answer": answer,
        "context": context_docs
    }


if __name__ == '__main__':
    result = run_llm(query="what are deep agents?")
    print(result)









