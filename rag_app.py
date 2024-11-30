import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms.base import LLM
from langchain.chains import RetrievalQA
import requests

load_dotenv()

class CustomLLM(LLM):
    endpoint_url: str
    api_key: str

    def __init__(self, endpoint_url, api_key):
        super().__init__()
        self.endpoint_url = endpoint_url
        self.api_key = api_key

    def _call(self, prompt: str) -> str:
        """Call the custom endpoint."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            # Add any other parameters your endpoint requires
        }

        response = requests.post(
            self.endpoint_url,
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            return response.json()["response"]  # Adjust based on your API response structure
        else:
            raise Exception(f"API call failed: {response.text}")

    @property
    def _llm_type(self) -> str:
        return "custom"

class RAGApp:
    def __init__(self):
        # Initialize API credentials
        self.endpoint_url = os.getenv("LLM_ENDPOINT_URL")
        self.api_key = os.getenv("LLM_API_KEY")
        
        if not (self.endpoint_url and self.api_key):
            raise ValueError("Please set LLM_ENDPOINT_URL and LLM_API_KEY in .env file")
        
        # Initialize embeddings (using HuggingFace as an alternative to OpenAI)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        
        # Initialize custom LLM
        self.llm = CustomLLM(
            endpoint_url=self.endpoint_url,
            api_key=self.api_key
        )
        
        # Initialize document store
        self.vector_store = None
        
    def load_documents(self, file_path):
        """Load and process documents"""
        loader = TextLoader(file_path)
        documents = loader.load()
        
        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(documents)
        
        self.vector_store = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings
        )
        
    def query(self, question: str) -> str:
        """Query the RAG system"""
        if not self.vector_store:
            return "Please load documents first."
            
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(),
            return_source_documents=True
        )
        
        response = qa_chain.invoke({"query": question})
        return response["result"]

# Example usage
if __name__ == "__main__":
    # Create RAG app instance
    rag = RAGApp()
    
    # Load sample document
    rag.load_documents("path/to/your/document.txt")
    
    # Query the system
    question = "What is this document about?"
    answer = rag.query(question)
    print(f"Q: {question}\nA: {answer}") 