"""
main_app.py

🎉 Example: HeyNote Voice Assistant for UX Prototyping

This script shows how to build a simple voice-driven note-taking assistant using our
helper modules:

  1. openai_api_helper.py  -> text completion, speech-to-text, text-to-speech
  2. ai_memory_helper.py   -> manage conversation memory (message history)
  3. data_save_helper.py   -> CRUD operations on JSON data files per session

✨ How it works:
  - Transcribe user audio (or accept text) into text
  - Classify the intent via AI (add note, update note, list notes)
  - Perform the action on a local JSON data store
  - Generate an AI response and play it back as audio

🔧 To customize for your project:
  - Change the `system_prompt` and `ai_personality`
  - Modify or extend `InferenceResponse` for your own intents
  - Use the same pattern to manage different data models!
"""

import os
from typing import List, Dict
from pydantic import BaseModel, Field

# Import our helper modules
from code_library.openai_api_helper import (
    generate_completion,
    transcribe_audio,
    synthesize_speech
)
from code_library.ai_memory_helper import (
    init_message_history,
    append_to_memory,
    get_memory
)
from code_library.data_save_helper import (
    init_data_store,
    read_data,
    add_entry,
    update_entry,
    generate_unique_id
)

# ---------- CONFIGURATION ----------
# First thing to do is, update OPENAI_API_KEY in configs.py with your own API key!

# Define a simple Note model for storing data
class Note(BaseModel):
    id: str
    content: str
    tags: str

# Pydantic model for classifying intents from user input
class InferenceResponse(BaseModel):
    intent: str = Field(..., description="One of ['add_note', 'update_note', 'list_notes']")
    content: str = Field(..., description="Text content for the note or query.")
    tags: str = Field(None, description="Optional comma-separated tags.")
    note_id: str = Field(None, description="ID of note to update (for update_note).")

# ---------- INITIAL SETUP ----------
# 1. Create a fresh JSON file for notes
default_notes = [
        {
            "id": "1",
            "content": "Research generative typography for the design systems module.",
            "tags": "typography, design, project"
        },
        {
            "id": "2",
            "content": "Ask about submission deadline for the capstone project.",
            "tags": "capstone, deadline, project"
        },
        {
            "id": "3",
            "content": "Summarize readings from 'Design as Art' by Bruno Munari.",
            "tags": "reading, summary, design"
        }
    ]

DATA_FILE = init_data_store(initial_data=default_notes)

# 2. Start conversation memory with system instructions
system_prompt = "You are HeyNote, a friendly voice assistant for design students."
ai_personality = {"role": "system", "content": "You speak in a clear, concise, and enthusiastic tone."}
memory = init_message_history(system_prompt, additional_context=[ai_personality])

# ---------- APPLICATION LOGIC ----------
def classify_intent_and_get_response(text: str) -> InferenceResponse:
    """
    Ask the AI to classify user input into a defined intent schema.
    """
    # Add user message to memory
    append_to_memory(memory, role="user", content=text)

    # Define classification prompt (customize as you like!)
    classification_prompt = (
        "Classify the user's intent into one of: add_note, update_note, list_notes. "
        "Return a JSON with keys: intent, content, tags, note_id."
    )

    # Ask AI with structured response parsing
    inference: InferenceResponse = generate_completion(
        message_history=memory,
        response_format=InferenceResponse
    )
    return inference


def add_note_action(inf: InferenceResponse) -> str:
    """
    Create a new Note entry and save it via data_save_helper.
    """
    new_id = generate_unique_id()
    note = Note(id=new_id, content=inf.content, tags=inf.tags or "")
    add_entry(note)
    return f"Got it! I added your note: '{note.content}'"


def update_note_action(inf: InferenceResponse) -> str:
    """
    Update an existing Note's content using its ID.
    """
    success = update_entry(inf.note_id, {"content": inf.content})
    if success:
        return f"Your note #{inf.note_id} has been updated!"
    else:
        return f"Oops—I couldn't find a note with ID {inf.note_id}."


def list_notes_action() -> str:
    """
    Retrieve and summarize all notes.
    """
    notes: List[Dict] = read_data()
    if not notes:
        return "There are no notes yet. Try adding one!"
    summary = "Here are your notes:\n"
    for n in notes:
        summary += f"- [{n['id']}] {n['content']} (tags: {n.get('tags','')} )\n"
    return summary

def update_settings(user_details, new_ai_personality):
    current_user_details = user_details
    ai_personality = new_ai_personality
    init_message_history()
    print("Updatig Settions: \n" + current_user_details + "\n" + ai_personality)


def run_ai_flow(audio_file_path):
    """
    Main loop: get user input, run AI flow, and play back audio.
    """
    print("🎙️ Welcome to HeyNote Voice Assistant Prototype!")
    
    # If input audio file existed on the path, transcribe it
    print("[INFO] Transcribing your audio file...")
    user_text = transcribe_audio(audio_file_path)

    print(f"[USER]: {user_text}")

    # Classify intent and get InferenceResponse
    user_intent = classify_intent_and_get_response(user_text)

    # Decide what to do based on intent
    if user_intent.intent == "add_note":
        reply_text = add_note_action(user_intent)
    elif user_intent.intent == "update_note":
        reply_text = update_note_action(user_intent)
    elif user_intent.intent == "list_notes":
        reply_text = list_notes_action()
    else:
        reply_text = "Sorry, I didn't understand that. Try saying 'add note' or 'list notes'."

    # Save assistant reply to memory
    append_to_memory(memory, role="assistant", content=reply_text)

    # Generate audio response
    audio_path = synthesize_speech(reply_text)
    print(f"[ASSISTANT]: {reply_text}")
    print(f"🔊 Audio saved to: {audio_path}")
