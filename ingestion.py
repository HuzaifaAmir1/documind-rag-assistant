import asyncio
import os
from typing import List

from dotenv import load_dotenv
from langchain_core.documents import Document
#from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_tavily import TavilyCrawl
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# Initialize embeddings
# 
# embeddings = OpenAIEmbeddings(
#     model="text-embedding-004",
#     openai_api_key=os.environ.get("OPENAI_API_KEY"),
#     openai_api_base=os.environ.get("OPENAI_BASE_URL"),
#)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.environ.get("OPENAI_API_KEY"),
)

# Initialize Pinecone vector store
vectorstore = PineconeVectorStore(
    index_name="langchain-docs-2026", embedding=embeddings
)

# Initialize Tavily crawler
tavily_crawl = TavilyCrawl()


async def main():
    print("=" * 50)
    print("Starting documentation ingestion pipeline...")
    print("=" * 50)

    print("\n[1/4] Crawling LangChain documentation with Tavily...")
    
    res = tavily_crawl.invoke(
        {
            "url": "https://python.langchain.com/docs/introduction/",
            "max_depth": 1,
            "extract_depth": "basic",
        }
    )

    # Print raw response keys so we can debug if needed
    print(f"Tavily response keys: {res.keys()}")

    # Handle different possible response formats
    results = []
    if "results" in res:
        results = res["results"]
    elif "pages" in res:
        results = res["pages"]
    elif isinstance(res, list):
        results = res
    else:
        print(f"Unexpected response format: {res}")
        return

    print(f"[2/4] Crawled {len(results)} pages successfully")

    # Convert to LangChain Documents
    all_docs = []
    for item in results:
        # Handle different key names
        url = item.get("url", item.get("source", "unknown"))
        content = item.get("raw_content", item.get("content", item.get("text", "")))
        
        if content:
            all_docs.append(
                Document(
                    page_content=content,
                    metadata={"source": url},
                )
            )
            print(f"  Added: {url}")

    if not all_docs:
        print("No documents were extracted. Check your Tavily API key.")
        return

    print(f"\n[3/4] Splitting {len(all_docs)} documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000, chunk_overlap=200
    )
    splitted_docs = text_splitter.split_documents(all_docs)
    print(f"  Created {len(splitted_docs)} chunks")

    print(f"\n[4/4] Storing chunks in Pinecone...")
    # Add in small batches
    batch_size = 50
    batches = [
        splitted_docs[i: i + batch_size]
        for i in range(0, len(splitted_docs), batch_size)
    ]
    for i, batch in enumerate(batches):
        vectorstore.add_documents(batch)
        print(f"  Stored batch {i + 1}/{len(batches)}")

    print("\n" + "=" * 50)
    print("Pipeline complete!")
    print(f"  Pages crawled : {len(all_docs)}")
    print(f"  Chunks stored : {len(splitted_docs)}")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())



