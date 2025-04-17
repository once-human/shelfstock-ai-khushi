# streamlit_app.py

"""
🎙️ Streamlit UI for HeyNote
This is your creative space to interact with your AI assistant via voice or file upload.
You can update the assistant’s personality, give it context, and review past responses.
"""

import streamlit as st
import os
import time
from datetime import datetime
import sounddevice as sd
from scipy.io.wavfile import write

from main_app import run_ai_flow, update_settings

# ----------------------------------
# 🔧 Basic Setup
# ----------------------------------
st.set_page_config(page_title="HeyNote", layout="wide")

USER_VOICE_DIR = "voice/user/"
AI_VOICE_DIR = "voice/ai/"
os.makedirs(USER_VOICE_DIR, exist_ok=True)
os.makedirs(AI_VOICE_DIR, exist_ok=True)

# Session state for keeping things across interactions
for key in ["recording", "recording_buffer", "recording_start_time", "about_you", "ai_personality"]:
    st.session_state.setdefault(key, None)
st.session_state.setdefault("ai_history", [])
st.session_state.setdefault("log_messages", [])

# ----------------------------------
# 🧠 Sidebar: Logs
# ----------------------------------
with st.sidebar:
    st.header("🧾 Backend Logs")
    for msg in st.session_state.log_messages[-10:][::-1]:
        st.text(msg)

# ----------------------------------
# 👤 Assistant Setup
# ----------------------------------
st.title("🎙️ HeyNote - Voice AI Assistant")
st.markdown("Set your assistant's vibe and introduce yourself.")

about_you = st.text_input("🧑 About You", value=st.session_state.about_you or "", placeholder="e.g. I'm exploring design + AI...")
ai_personality = st.text_input("🤖 AI Personality", value=st.session_state.ai_personality or "", placeholder="e.g. Friendly, curious, good listener.")

if st.button("💾 Save Personality"):
    st.session_state.about_you = about_you
    st.session_state.ai_personality = ai_personality
    update_settings(about_you, ai_personality)
    st.success("Personality updated!")
    st.session_state.log_messages.append("[INFO] Settings updated.")

# ----------------------------------
# 🎤 Voice Input Section
# ----------------------------------
st.markdown("## 🎧 Record Your Message")

filename = f"user_input_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
user_audio_path = os.path.join(USER_VOICE_DIR, filename)

# uploaded_file = st.file_uploader("📁 Or upload a voice file", type=["wav", "mp3", "m4a"])

record_button = st.button("🔴 Start/Stop Recording")

# If audio file uploaded
# if uploaded_file:
#     with open(user_audio_path, "wb") as f:
#         f.write(uploaded_file.read())
#     st.success("Audio uploaded! Running AI...")
#     st.session_state.log_messages.append(f"[INFO] File uploaded: {user_audio_path}")

#     try:
#         result_audio = update_settings(user_audio_path)
#         if result_audio and os.path.exists(result_audio):
#             st.success("✅ AI response ready")
#             st.audio(result_audio)
#             st.session_state.ai_history.append(result_audio)
#         else:
#             st.error("No response generated.")
#     except Exception as e:
#         st.error("Something went wrong.")
#         st.session_state.log_messages.append(f"[ERROR] {e}")

# If using mic
if record_button:
    st.session_state.recording = not st.session_state.recording

    if st.session_state.recording:
        st.success("🎙️ Recording... click again to stop.")
        st.session_state.recording_buffer = sd.rec(int(60 * 44100), samplerate=44100, channels=1)
        st.session_state.recording_start_time = time.time()
        st.session_state.log_messages.append("[INFO] Recording started.")
    else:
        sd.stop()
        duration = int(time.time() - st.session_state.recording_start_time)
        audio = st.session_state.recording_buffer[:duration * 44100]
        write(user_audio_path, 44100, audio)
        st.session_state.log_messages.append(f"[INFO] Recording saved: {user_audio_path}")

        try:
            result_audio = run_ai_flow(user_audio_path)
            if result_audio and os.path.exists(result_audio):
                st.success("✅ AI responded!")
                st.audio(result_audio)
                st.session_state.ai_history.append(result_audio)
            else:
                st.error("No response generated.")
        except Exception as e:
            st.error("Something went wrong.")
            st.session_state.log_messages.append(f"[ERROR] {e}")

# ----------------------------------
# 📜 History
# ----------------------------------
if st.session_state.ai_history:
    st.markdown("## 🗂️ Response History")
    for i, audio_path in enumerate(reversed(st.session_state.ai_history), 1):
        st.markdown(f"**Response {i}**")
        st.audio(audio_path)