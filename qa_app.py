# qa_app.py (Corrected for import path)

import boto3
from langchain_aws import BedrockEmbeddings
from langchain_aws.llms.bedrock import Bedrock # <-- CORRECTED IMPORT
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def answer_question(question: str, index_folder: str = "faiss_index_genesis"):
    """
    Loads a local FAISS index, finds relevant documents for a question,
    and uses Bedrock to generate an answer.
    """
    print(f"Loading vector index from: {index_folder}")
    print(f"Answering question: {question}\n")

    try:
        # Step 1: Initialize Bedrock clients
        bedrock_client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
        
        embeddings_model = BedrockEmbeddings(
            client=bedrock_client,
            model_id="cohere.embed-multilingual-v3:0"
        )
        
        llm = Bedrock(
            client=bedrock_client,
            model_id="ai21.jamba-1-5-large-v1:0",
            model_kwargs={"maxTokens": 1024, "temperature": 0.1}
        )
        print("Bedrock clients initialized.")

        # Step 2: Load the local FAISS index
        vector_db = FAISS.load_local(
            index_folder, 
            embeddings_model, 
            allow_dangerous_deserialization=True
        )
        print("FAISS index loaded successfully.")

        # Step 3: Search the index for relevant documents
        retrieved_docs = vector_db.similarity_search(question, k=5)
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        print("\n--- Retrieved Context ---\n")
        print(context)
        print("\n-------------------------\n")

        # Step 4: Create a prompt and chain to generate the answer
        prompt_template = """
        Use the following context to answer the question at the end. 
        If you don't know the answer from the context provided, just say that you don't know.
        Answer in Hebrew.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
        
        prompt = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        
        # Step 5: Run the chain and get the answer
        print("Generating answer...")
        result = llm_chain.invoke({"context": context, "question": question})

        print("\n--- Final Answer ---")
        print(result['text'])

    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

# --- Script Execution ---
if __name__ == "__main__":
    user_question = "את מי שלח יעקב לראות את שלום אחיו?"
    answer_question(user_question)