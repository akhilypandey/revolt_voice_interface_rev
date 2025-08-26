import asyncio
import json
import logging
from typing import AsyncGenerator, Optional
import google.generativeai as genai
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiLiveClient:
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL_NAME)
        self.conversation = None
        
    async def start_conversation(self) -> str:
        """Start a new conversation session"""
        try:
            # Initialize the conversation
            self.conversation = self.model.start_chat()
            logger.info("Conversation started successfully")
            return "Conversation started"
        except Exception as e:
            logger.error(f"Error starting conversation: {e}")
            raise
    
    async def send_audio_message(self, audio_data: bytes, mime_type: str = "audio/webm") -> AsyncGenerator[str, None]:
        """Send audio message and get streaming response"""
        if not self.conversation:
            await self.start_conversation()
            # Send system instructions as first message
            await self._send_system_instructions()
        
        try:
            # Create the audio part for the message
            audio_part = {
                "mime_type": mime_type,
                "data": audio_data
            }
            
            # Send the audio message and get streaming response
            response = await self.conversation.send_message_async(
                audio_part,
                stream=True
            )
            
            # Stream the response chunks
            async for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            logger.error(f"Error in send_audio_message: {e}")
            yield f"Error: {str(e)}"
    
    async def _send_system_instructions(self):
        """Send system instructions to set the AI's behavior"""
        try:
            # Send system instructions as a text message
            async for _ in self.send_text_message(Config.SYSTEM_INSTRUCTIONS):
                pass
        except Exception as e:
            logger.warning(f"Could not send system instructions: {e}")
    
    async def send_text_message(self, text: str) -> AsyncGenerator[str, None]:
        """Send text message and get streaming response (for testing)"""
        if not self.conversation:
            await self.start_conversation()
        
        try:
            response = await self.conversation.send_message_async(text, stream=True)
            
            async for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            logger.error(f"Error in send_text_message: {e}")
            yield f"Error: {str(e)}"
    
    def end_conversation(self):
        """End the current conversation"""
        self.conversation = None
        logger.info("Conversation ended")
