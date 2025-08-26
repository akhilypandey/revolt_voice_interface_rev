# revolt_voice_interface_rev

A real-time conversational voice interface using the Gemini Live API, replicating the functionality of the Revolt Motors chatbot.

## Features

- **Real-time Voice Chat**: Natural conversation with AI using voice input
- **Interruption Support**: Users can interrupt the AI while it's speaking
- **Low Latency**: Optimized for 1-2 second response times
- **Multi-language Support**: Built-in support for various languages
- **Clean UI**: Modern, responsive interface
- **Server-to-Server Architecture**: Secure communication with Gemini Live API

## Prerequisites

- Python 3.8 or higher
- Google AI Studio API key
- Modern web browser with microphone access

## Setup Instructions

### 1. Get API Key

1. Visit [Google AI Studio](https://aistudio.google.com)
2. Create a free account
3. Generate an API key
4. Copy the API key for the next step

### 2. Environment Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd revolt-motors-voice-chat
```

2. Create a `.env` file in the root directory:
```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the Application

1. Start the server:
```bash
python main.py
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

3. Allow microphone access when prompted
4. Click the microphone button and start speaking!

## Usage

### Voice Chat
- Click the microphone button to start recording
- Speak your question about Revolt Motors
- The AI will respond in real-time
- You can interrupt the AI by clicking the microphone again

### Text Chat (Alternative)
- Type your message in the text input field
- Press Enter or click Send
- Get instant text responses

## Technical Details

### Architecture
- **Backend**: FastAPI with WebSocket support
- **Frontend**: Vanilla JavaScript with modern CSS
- **API**: Google Gemini Live API (server-to-server)
- **Audio**: WebM format with Opus codec

### Model Configuration
The application uses `gemini-2.5-flash-preview-native-audio-dialog` by default.

For development/testing to avoid rate limits, you can switch to:
- `gemini-2.0-flash-live-001`
- `gemini-live-2.5-flash-preview`

Edit `config.py` to change the model.

### System Instructions
The AI is configured with specific instructions to only discuss Revolt Motors topics:
- Company information
- Product details (RV300, RV400, etc.)
- Services and support
- Showroom locations

## Project Structure

```
revolt-motors-voice-chat/
├── main.py                 # FastAPI server
├── gemini_client.py        # Gemini Live API client
├── config.py              # Configuration and system instructions
├── requirements.txt       # Python dependencies
├── static/
│   ├── index.html         # Main HTML page
│   ├── styles.css         # CSS styles
│   └── app.js            # Frontend JavaScript
└── README.md             # This file
```

## Troubleshooting

### Common Issues

1. **Microphone Access Denied**
   - Check browser permissions
   - Ensure HTTPS is used (required for microphone access)

2. **API Key Error**
   - Verify your API key is correct
   - Check the `.env` file exists and contains the key

3. **Rate Limit Exceeded**
   - Switch to a different model in `config.py`
   - Wait for rate limit reset

4. **Connection Issues**
   - Check if the server is running
   - Verify port 8000 is available

### Development Mode

For extensive testing, consider using the interactive playground:
https://aistudio.google.com/live

## API Documentation

- [Gemini Live API Docs](https://ai.google.dev/gemini-api/docs/live)
- [Example Applications](https://ai.google.dev/gemini-api/docs/live#example-applications)

## License

This project is for educational and demonstration purposes.

## Contributing

Feel free to submit issues and enhancement requests!
