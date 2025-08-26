import asyncio
import json
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import aiofiles
from gemini_client import GeminiLiveClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Revolt Motors Voice Chat", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Store active connections
active_connections: dict[str, WebSocket] = {}
gemini_clients: dict[str, GeminiLiveClient] = {}

@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serve the main HTML page"""
    async with aiofiles.open("static/index.html", "r") as f:
        content = await f.read()
    return HTMLResponse(content=content)

@app.get("/debug", response_class=HTMLResponse)
async def get_debug():
    """Serve the debug HTML page"""
    async with aiofiles.open("debug_voice.html", "r") as f:
        content = await f.read()
    return HTMLResponse(content=content)

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time voice chat"""
    await websocket.accept()
    active_connections[client_id] = websocket
    
    try:
        # Initialize Gemini client for this connection
        gemini_clients[client_id] = GeminiLiveClient()
        await gemini_clients[client_id].start_conversation()
        
        logger.info(f"Client {client_id} connected")
        
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                message_type = message.get("type")
                
                if message_type == "audio":
                    # Handle audio message
                    audio_data = message.get("audio_data")
                    mime_type = message.get("mime_type", "audio/webm")
                    
                    if audio_data:
                        # Convert base64 to bytes
                        import base64
                        audio_bytes = base64.b64decode(audio_data)
                        
                        # Send to Gemini and stream response
                        async for chunk in gemini_clients[client_id].send_audio_message(audio_bytes, mime_type):
                            await websocket.send_text(json.dumps({
                                "type": "response_chunk",
                                "text": chunk
                            }))
                        
                        # Send end of response marker
                        await websocket.send_text(json.dumps({
                            "type": "response_end"
                        }))
                
                elif message_type == "text":
                    # Handle text message (for testing)
                    text = message.get("text", "")
                    
                    async for chunk in gemini_clients[client_id].send_text_message(text):
                        await websocket.send_text(json.dumps({
                            "type": "response_chunk",
                            "text": chunk
                        }))
                    
                    await websocket.send_text(json.dumps({
                        "type": "response_end"
                    }))
                
                elif message_type == "ping":
                    # Handle ping for connection health
                    await websocket.send_text(json.dumps({
                        "type": "pong"
                    }))
                    
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": str(e)
                }))
                
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}")
    finally:
        # Cleanup
        if client_id in active_connections:
            del active_connections[client_id]
        if client_id in gemini_clients:
            gemini_clients[client_id].end_conversation()
            del gemini_clients[client_id]
        logger.info(f"Client {client_id} disconnected")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "active_connections": len(active_connections)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
