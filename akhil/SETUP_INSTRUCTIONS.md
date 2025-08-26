# Quick Setup Guide

## 🚀 Get Started in 3 Steps

### 1. Get Your API Key
1. Go to [Google AI Studio](https://aistudio.google.com)
2. Sign up/login and create a free API key
3. Copy the API key

### 2. Configure the Application
```bash
# Create .env file with your API key
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
```

### 3. Install and Run
```bash
# Install dependencies
pip3 install -r requirements.txt

# Start the application
python3 start.py
```

## 🎯 What You'll Get

- **Real-time voice chat** with Revolt Motors AI assistant
- **Interruption support** - you can interrupt the AI while it's speaking
- **Low latency** responses (1-2 seconds)
- **Multi-language support**
- **Clean, modern interface**

## 🎤 How to Use

1. Open http://localhost:8000 in your browser
2. Allow microphone access when prompted
3. Click the microphone button and start speaking
4. Ask about Revolt Motors products, services, or company info
5. Interrupt the AI anytime by clicking the mic button again

## 🔧 Testing Your Setup

Run the test script to verify everything is working:
```bash
python3 test_setup.py
```

## 📱 Features Demonstrated

- **Voice Input**: Natural speech-to-text conversion
- **Real-time Responses**: Streaming AI responses
- **Interruption Handling**: Stop AI mid-sentence
- **Multi-language**: Speak in various languages
- **Context Awareness**: AI remembers conversation history
- **Revolt Motors Focus**: AI only discusses relevant topics

## 🎥 Demo Requirements

For your demo video, make sure to show:
1. Natural conversation flow
2. Clear interruption of AI mid-response
3. Low latency responses
4. Professional UI/UX

## 🚨 Important Notes

- Use HTTPS in production (required for microphone access)
- The free API has rate limits - switch models in `config.py` for testing
- Ensure microphone permissions are granted in browser

## 📞 Support

If you encounter issues:
1. Check the README.md for detailed troubleshooting
2. Verify your API key is correct
3. Ensure all dependencies are installed
4. Test with the provided test script

---

**Ready to create your demo video! 🎬**
