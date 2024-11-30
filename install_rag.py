def create_env_file():
    """Create .env file with default settings"""
    default_content = """LLM_ENDPOINT_URL=your_endpoint_url_here
LLM_API_KEY=your_api_key_here"""
    
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(default_content)#!/usr/bin/env python3
import os
import sys
import subprocess
import platform

def check_python():
    """Check Python version"""
    if sys.version_info < (3, 8):
        print("Python 3.8 or higher is required")
        sys.exit(1)

def install_dependencies():
    """Install required packages"""
    requirements = [
        "langchain",
        "chromadb",
        "python-dotenv",
        "requests",
        "sentence-transformers"
    ]
    
    print("Installing dependencies...")
    for package in requirements:
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "pip", 
            "install", 
            "--upgrade", 
            package
        ])

def create_env_file():
    """Create .env file with default settings"""
    with open(".env") as f:
        env_content = f.read().strip()
    
    with open(".env", "w") as f:
        f.write(env_content)

def download_rag_app():
    """Download the main RAG application"""
    import requests
    
    # Replace with your actual hosted RAG app URL
    rag_url = "https://your-domain.com/rag_app.py"
    
    try:
        response = requests.get(rag_url)
        response.raise_for_status()
        
        with open("rag_app.py", "w") as f:
            f.write(response.text)
            
    except Exception as e:
        print(f"Failed to download RAG app: {e}")
        sys.exit(1)

def main():
    print("Setting up RAG Application...")
    
    # Create project directory
    project_dir = "rag_project"
    os.makedirs(project_dir, exist_ok=True)
    os.chdir(project_dir)
    
    # Run setup steps
    check_python()
    install_dependencies()
    create_env_file()
    download_rag_app()
    
    print("\nSetup complete!")
    print("\nTo use the RAG application:")
    print("1. cd rag_project")
    print("2. Edit .env file with your credentials")
    print("3. Run: python rag_app.py")

if __name__ == "__main__":
    main() 