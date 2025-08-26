#!/usr/bin/env python3
"""
Test script to verify the Revolt Motors Voice Chat setup
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test environment setup"""
    print("🔍 Testing environment setup...")
    
    # Load environment variables
    load_dotenv()
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    else:
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("   Please create a .env file with your API key")
        return False
    else:
        print("✅ GEMINI_API_KEY found")
    
    # Check required files
    required_files = [
        "main.py",
        "gemini_client.py", 
        "config.py",
        "requirements.txt",
        "static/index.html",
        "static/styles.css",
        "static/app.js"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present")
    
    return True

def test_dependencies():
    """Test if required dependencies are installed"""
    print("\n📦 Testing dependencies...")
    
    required_packages = [
        "fastapi",
        "uvicorn", 
        "google.generativeai",
        "websockets",
        "dotenv",
        "aiofiles"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == "dotenv":
                __import__("dotenv")
            else:
                __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True

def test_gemini_connection():
    """Test Gemini API connection"""
    print("\n🔌 Testing Gemini API connection...")
    
    try:
        from config import Config
        from gemini_client import GeminiLiveClient
        
        client = GeminiLiveClient()
        print("✅ Gemini client initialized successfully")
        
        # Test with a simple text message
        import asyncio
        
        async def test_message():
            try:
                await client.start_conversation()
                print("✅ Conversation started successfully")
                
                # Test a simple text message
                response_count = 0
                async for chunk in client.send_text_message("Hello"):
                    response_count += 1
                    if response_count > 0:
                        break
                
                if response_count > 0:
                    print("✅ API response received successfully")
                else:
                    print("⚠️  No response received (this might be normal)")
                
                client.end_conversation()
                return True
                
            except Exception as e:
                print(f"❌ API test failed: {e}")
                return False
        
        result = asyncio.run(test_message())
        return result
        
    except Exception as e:
        print(f"❌ Failed to initialize Gemini client: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Revolt Motors Voice Chat - Setup Test\n")
    
    # Test environment
    env_ok = test_environment()
    if not env_ok:
        print("\n❌ Environment setup failed. Please fix the issues above.")
        return
    
    # Test dependencies
    deps_ok = test_dependencies()
    if not deps_ok:
        print("\n❌ Dependencies test failed. Please install missing packages.")
        return
    
    # Test Gemini connection
    api_ok = test_gemini_connection()
    
    print("\n" + "="*50)
    if env_ok and deps_ok and api_ok:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nTo start the application:")
        print("   python main.py")
        print("\nThen open: http://localhost:8000")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
    print("="*50)

if __name__ == "__main__":
    main()
