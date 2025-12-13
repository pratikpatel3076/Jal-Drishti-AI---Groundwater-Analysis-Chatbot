#!/usr/bin/env python3
"""
Setup script for Jal Drishti AI Chatbot
This script helps set up the AI-powered groundwater chatbot
"""

import os
import sys
import subprocess
import json

def print_banner():
    print("🌊" + "="*60)
    print("   Jal Drishti AI - Groundwater Chatbot Setup")
    print("="*62)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_node_version():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js version: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    print("❌ Node.js is not installed or not in PATH")
    return False

def install_backend_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing backend dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'backend/requirements.txt'], check=True)
        print("✅ Backend dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install backend dependencies: {e}")
        return False

def install_frontend_dependencies():
    """Install Node.js dependencies"""
    print("\n📦 Installing frontend dependencies...")
    try:
        os.chdir('frontend')
        subprocess.run(['npm', 'install'], check=True)
        os.chdir('..')
        print("✅ Frontend dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install frontend dependencies: {e}")
        return False

def create_env_file():
    """Create .env file for configuration"""
    env_path = 'backend/.env'
    if os.path.exists(env_path):
        print("✅ .env file already exists")
        return True
    
    print("\n🔧 Creating .env file...")
    env_content = """# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Set default language
DEFAULT_LANGUAGE=EN

# Chart configuration
CHART_DPI=300
CHART_FIGSIZE=10,6

# Memory configuration
MAX_CONVERSATION_MEMORY=10
"""
    
    try:
        with open(env_path, 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        print("   ⚠️  Please add your OpenAI API key to backend/.env")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def check_data_files():
    """Check if required data files exist"""
    data_file = 'backend/ingres_clone.json'
    if os.path.exists(data_file):
        print("✅ Groundwater data file found")
        return True
    else:
        print("❌ Groundwater data file not found")
        print(f"   Please ensure {data_file} exists")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n🚀 Setup Complete! Next steps:")
    print("="*50)
    print("1. Add your OpenAI API key to backend/.env")
    print("2. Ensure backend/ingres_clone.json contains groundwater data")
    print("3. Start the backend server:")
    print("   cd backend && python app.py")
    print("4. Start the frontend (in a new terminal):")
    print("   cd frontend && npm run dev")
    print("5. Or run both together:")
    print("   cd frontend && npm run dev:all")
    print("\n🌊 Enjoy your AI-powered groundwater chatbot!")

def main():
    print_banner()
    
    # Check system requirements
    if not check_python_version():
        sys.exit(1)
    
    if not check_node_version():
        print("   Please install Node.js from https://nodejs.org/")
        sys.exit(1)
    
    # Install dependencies
    if not install_backend_dependencies():
        sys.exit(1)
    
    if not install_frontend_dependencies():
        sys.exit(1)
    
    # Create configuration files
    create_env_file()
    
    # Check data files
    check_data_files()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
