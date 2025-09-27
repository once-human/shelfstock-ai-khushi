import os
import sys
from datetime import datetime
from typing import List, Dict
import openai
import streamlit as st
from pydantic import BaseModel
from typing import List, Dict, Optional, Type, Union

"""
openai_api_helper.py

👋 About this file:
This module wraps the most common OpenAI API tasks into easy-to-use functions for students and designers
who want to quickly prototype AI-driven experiences without getting bogged down in API details.

It handles:
- Text generation and conversation
- Audio transcription (speech-to-text)
- Text-to-speech synthesis
- Structured responses using Pydantic models

This file makes all those steps easy.
"""

# ---------- OpenAI Client ----------

# Get API key from Streamlit secrets or environment variables
api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", "your-openai-api-key-here"))
client = openai.OpenAI(api_key=api_key)

# ---------- TEXT-TO-TEXT COMPLETION ----------

def generate_completion(
    message_history: List[Dict[str, str]],
    response_model: Optional[Type[BaseModel]] = None,
    temperature: float = 0.7,
    max_tokens: int = 1000
) -> Union[str, BaseModel]:
    """
    Generate a text completion using OpenAI's chat API.
    
    Args:
        message_history: List of message dictionaries with 'role' and 'content' keys
        response_model: Optional Pydantic model for structured responses
        temperature: Controls randomness (0.0 to 1.0)
        max_tokens: Maximum tokens to generate
        
    Returns:
        String response or Pydantic model instance
    """
    print(f"[generate_completion] Generating completion with {len(message_history)} messages")
    
    try:
        if response_model:
            # Use structured output
            response = client.chat.completions.create(
                model=st.secrets.get("LLM_MODEL", "gpt-4o"),
                messages=message_history,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"}
            )
            
            # Parse JSON response into Pydantic model
            import json
            content = response.choices[0].message.content
            json_data = json.loads(content)
            return response_model(**json_data)
        else:
            # Regular text completion
            response = client.chat.completions.create(
                model=st.secrets.get("LLM_MODEL", "gpt-4o"),
                messages=message_history,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
    except Exception as e:
        print(f"[generate_completion] Error: {e}")
        return "Sorry, I encountered an error generating a response."

# ---------- AUDIO TRANSCRIPTION ----------

def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribe audio file to text using OpenAI's Whisper API.
    
    Args:
        audio_file_path: Path to the audio file (mp3, wav, m4a, etc.)
        
    Returns:
        Transcribed text as string
    """
    print(f"[transcribe_audio] Started transcribing: {audio_file_path}")

    with open(audio_file_path, "rb") as audio_file:
        transcription_response = client.audio.transcriptions.create(
            model=st.secrets.get("TRANSCRIPTION_MODEL", "whisper-1"),
            file=audio_file,
            response_format="text"
        )

    print("[transcribe_audio] Finished transcribing audio.")
    return transcription_response

# ---------- TEXT-TO-SPEECH ----------

def synthesize_speech(
    text: str, 
    voice: str = "alloy",
    output_dir: str = "voice/ai/",
    instructions: Optional[str] = None
) -> str:
    """
    Convert text to speech using OpenAI's TTS API.
    
    Args:
        text: Text to convert to speech
        voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
        output_dir: Directory to save the audio file
        instructions: Optional instructions for voice generation
        
    Returns:
        Path to the generated audio file
    """
    print(f"[synthesize_speech] Converting text to speech: {text[:50]}...")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    filename = f"response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    filepath = os.path.join(output_dir, filename)

    with client.audio.speech.with_streaming_response.create(
        model=st.secrets.get("TEXT_TO_SPEECH_MODEL", "tts-1"),
        voice=voice,
        input=text,
        instructions=instructions
    ) as response:
        response.stream_to_file(filepath)

    print(f"[synthesize_speech] Audio saved to: {filepath}")
    return filepath

# ---------- UTILITY FUNCTIONS ----------

def create_message(role: str, content: str) -> Dict[str, str]:
    """
    Create a message dictionary for the chat API.
    
    Args:
        role: Message role ('system', 'user', 'assistant')
        content: Message content
        
    Returns:
        Message dictionary
    """
    return {"role": role, "content": content}

def add_to_history(history: List[Dict[str, str]], role: str, content: str) -> List[Dict[str, str]]:
    """
    Add a message to the conversation history.
    
    Args:
        history: Current conversation history
        role: Message role
        content: Message content
        
    Returns:
        Updated conversation history
    """
    history.append(create_message(role, content))
    return history
