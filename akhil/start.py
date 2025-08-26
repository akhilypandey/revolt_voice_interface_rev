#!/usr/bin/env python3
"""
Startup script for Revolt Motors Voice Chat
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

def check_environment():
    """Check if environment is properly set up"""
    load_dotenv()
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found!")
        print("\nPlease create a .env file with your API key:")
        print("echo 'GEMINI_API_KEY=your_api_key_here' > .env")
        print("\nGet your API key from: https://aistudio.google.com")
        return False
    
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Revolt Motors Voice Chat...")
    print("📍 Server will be available at: http://localhost:8000")
    print("🎤 Make sure to allow microphone access when prompted")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main startup function"""
    print("🎯 Revolt Motors Voice Chat")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Check if dependencies are installed
    try:
        import fastapi
        import uvicorn
        import google.generativeai
        print("✅ Dependencies found")
    except ImportError:
        print("📦 Installing missing dependencies...")
        if not install_dependencies():
            sys.exit(1)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
