#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import shutil

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
    if platform.system() == "Windows":
        # Use pip for Windows
        for package in requirements:
            subprocess.check_call([
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                package
            ])
    else:
        # Use pipenv for Linux
        try:
            # Check if pipenv is installed
            if not shutil.which("pipenv"):
                print("pipenv not found. Please install it first:")
                print("For Arch Linux: sudo pacman -S python-pipenv")
                print("For Ubuntu: sudo apt install pipenv")
                print("For other distributions, check your package manager")
                sys.exit(1)
            
            # Install dependencies using pipenv
            subprocess.check_call([
                "pipenv",
                "install"
            ] + requirements)
            
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
            sys.exit(1)

def create_env_file():
    """Create .env file with default settings"""
    default_content = """LLM_ENDPOINT_URL=your_endpoint_url_here
LLM_API_KEY=your_api_key_here"""
    
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(default_content)

def download_rag_app():
    """Download the main RAG application"""
    import requests
    
    # Replace with your actual GitHub repository and branch
    github_repo = "https://raw.githubusercontent.com/AkkhilCodingHub/RAG_app/main/rag_app.py"
    
    try:
        response = requests.get(github_repo)
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
    print(f"1. cd {project_dir}")
    print("2. Edit .env file with your credentials")
    if platform.system() != "Windows":
        print("3. Run: pipenv shell")
        print("4. Run: python rag_app.py")
    else:
        print("3. Run: python rag_app.py")

if __name__ == "__main__":
    main()