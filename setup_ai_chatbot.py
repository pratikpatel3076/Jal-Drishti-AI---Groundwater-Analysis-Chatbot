#!/usr/bin/env python3
"""
Setup script for Jal Drishti AI Chatbot
"""
import os
import sys
import subprocess

REQUIREMENTS = "backend/requirements.txt"
DATA_FILE = "backend/ingres_clone.json"

def print_banner():
    print("=" * 60)
    print("   Jal Drishti AI - Groundwater Chatbot Setup")
    print("=" * 60)

def check_python():
    if sys.version_info < (3, 8):
        print(f"ERROR: Python 3.8+ required, found {sys.version_info[0]}.{sys.version_info[1]}")
        return False
    print(f"Python: {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}")
    return True

def check_node():
    try:
        r = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
        print(f"Node.js: {r.stdout.strip()}")
        return True
    except Exception:
        print("ERROR: Node.js not found in PATH")
        return False

def install_python():
    print("\nInstalling Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS], check=True)
        print("OK: Python dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FAILED: pip install exited with code {e.returncode}")
        return False

def install_node():
    print("\nInstalling Node.js dependencies...")
    try:
        subprocess.run(["npm", "install"], check=True)
        print("OK: Node.js dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FAILED: npm install exited with code {e.returncode}")
        return False

def create_env():
    env_path = "backend/.env"
    if os.path.exists(env_path):
        print(f"OK: {env_path} already exists")
        return True
    with open(env_path, "w") as f:
        f.write("OPENAI_API_KEY=sk-your_key_here\nDEFAULT_LANGUAGE=EN\n")
    print(f"OK: {env_path} created (please add your OpenAI key)")
    return True

def check_data():
    if os.path.exists(DATA_FILE):
        print(f"OK: {DATA_FILE} found")
        return True
    print(f"WARNING: {DATA_FILE} not found — chatbot will not have data to query")
    print(f"  Place your CGWB groundwater JSON at: {DATA_FILE}")
    return False

def main():
    print_banner()
    ok = True
    ok &= check_python()
    ok &= check_node()
    if not ok:
        sys.exit(1)
    install_python()
    install_node()
    create_env()
    check_data()
    print("\nSetup complete. Run: npm run dev")
    print("  Frontend: http://localhost:8080")
    print("  Backend:  http://localhost:5000")

if __name__ == "__main__":
    main()
