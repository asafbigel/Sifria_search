# create_full_index.py (Final Version)

import requests
import json
from bs4 import BeautifulSoup
import boto3
from langchain_aws import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from tqdm import tqdm

def create_full_genesis_index(index_name="faiss_index_genesis"):
    """
    Downloads all chapters of Genesis, combines them, splits the full text
    into small chunks, creates embeddings, and saves the index.
    """
    print("Starting to build the full index for the book of Genesis...")
    all_docs_from_chapters = []

    # Stage 1: Download all chapters
    for chapter in tqdm(range(1, 51), desc="Downloading Chapters"):
        url = f"https://www.sefaria.org/api/texts/Genesis.{chapter}"
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            hebrew_verses_with_html = data.get('he', [])
            if not hebrew_verses_with_html:
                continue

            full_chapter_html = "\n".join(hebrew_verses_with_html)
            soup = BeautifulSoup(full_chapter_html, 'html.parser')
            clean_chapter_text = soup.get_text()
            
            # Create one large Document for the whole chapter, with metadata
            source_metadata = {"source": f"Genesis, Chapter {chapter}"}
            doc = Document(page_content=clean_chapter_text, metadata=source_metadata)
            all_docs_from_chapters.append(doc)

        except requests.exceptions.RequestException as e:
            print(f"\nWarning: Could not download Chapter {chapter}. Error: {e}")
            continue

    if not all_docs_from_chapters:
        print("❌ Error: No text could be processed. Exiting.")
        return

    print(f"\nSuccessfully downloaded {len(all_docs_from_chapters)} chapters.")

    # Stage 2: Split the downloaded text into small, uniform chunks
    print("Now splitting all downloaded text into smaller chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=350,      # You can experiment with this value
        chunk_overlap=40,
        length_function=len,
    )
    final_chunks = text_splitter.split_documents(all_docs_from_chapters)
    print(f"Total text was split into {len(final_chunks)} chunks.")
    
    # Stage 3: Create the vector index from the final chunks
    try:
        print("Initializing Bedrock embeddings model...")
        bedrock_client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
        embeddings_model = BedrockEmbeddings(
            client=bedrock_client,
            model_id="amazon.titan-embed-text-v2:0"
        )

        print("Creating vector index from all chunks... This will take several minutes.")
        vector_db = FAISS.from_documents(documents=final_chunks, embedding=embeddings_model)
        
        vector_db.save_local(index_name)
        print(f"✅ Success! Full Genesis vector index saved to the folder '{index_name}'")

    except Exception as e:
        print(f"❌ An unexpected error occurred during indexing: {e}")


# --- Script Execution ---
if __name__ == "__main__":
    create_full_genesis_index()