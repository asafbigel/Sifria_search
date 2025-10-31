# create_index.py

import boto3
from langchain_aws import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def create_vector_index(file_path, index_name):
    """
    Reads a text file, splits it into chunks, creates embeddings using Bedrock,
    and saves them to a local FAISS vector index.
    """
    print(f"Starting to create index from file: {file_path}")

    try:
        # Step 1: Read the text from the file
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        print("Successfully read the text file.")

        # Step 2: Split the text into smaller chunks
        # This is crucial for the RAG model to find relevant pieces of information.
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len,
        )
        chunks = text_splitter.split_text(text)
        print(f"Text split into {len(chunks)} chunks.")

        # Step 3: Initialize the Bedrock embeddings model
        # This will be used to convert our text chunks into vectors.
        bedrock_client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
        embeddings_model = BedrockEmbeddings(
            client=bedrock_client,
            model_id="amazon.titan-embed-text-v2:0" # This is the ID for the embedding model
        )
        print("Bedrock embeddings model initialized.")

        # Step 4: Create the vector index from the chunks
        # LangChain's FAISS class handles the process of calling the embedding model
        # for each chunk and storing the result in a searchable index.
        print("Creating vector index... This may take a moment.")
        vector_db = FAISS.from_texts(texts=chunks, embedding=embeddings_model)
        
        # Step 5: Save the index locally to a file
        vector_db.save_local(index_name)
        print(f"✅ Success! Vector index has been created and saved to the folder '{index_name}'")

    except FileNotFoundError:
        print(f"❌ Error: The file '{file_path}' was not found. Make sure it's in the same directory.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

# --- Script Execution ---
if __name__ == "__main__":
    # The clean text file you created in the previous step
    source_file = "bereshit_chapter_1.txt"
    
    # The name of the folder where the index will be saved
    local_index_folder = "faiss_index"
    
    create_vector_index(source_file, local_index_folder)