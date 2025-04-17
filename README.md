# 🎛️ AI Prototyping Toolkit for UX Design Projects

This toolkit is designed to help UX and interaction design students quickly prototype AI-driven experiences using natural language, speech input, and intelligent responses. It abstracts complex AI workflows into modular, beginner-friendly code that can be adapted to a wide range of projects.

Whether you're building a voice assistant, creative tool, conversational interface, or a speculative AI interaction, this library gives you the building blocks to get started—fast.

---

## 🧰 What's Included

Each module focuses on one key area of interaction with AI systems:

| Module                | What it does                                                                 |
|------------------------|------------------------------------------------------------------------------|
| `configs.py`           | Central configuration: model names, API keys, file paths, etc.              |
| `openai_api_helper.py` | Functions for classification, content generation, and conversational logic  |
| `ai_memory_helper.py`  | Manages memory and message history for more personalized AI responses       |
| `data_save_helper.py`  | Local JSON-based storage for saving and reading structured data             |
| `voice_helper.py`      | Handles speech-to-text (transcription) and text-to-speech (audio output)    |
| `main_app.py`          | Example runner that connects all modules into a working prototype flow      |

---

## 💡 What You Can Build

This library supports rapid prototyping of:
- Voice interfaces or AI-powered companions
- Conversational tools with memory
- Audio-driven feedback systems
- Custom assistants or guides
- Any interaction where the user speaks and the AI responds with intelligence

You can easily plug this into your own project idea, modify prompts, or swap out functionality to experiment with different interactions.

---

## 🚀 How to Use

1. **Clone the repository or download the files.**

2. **Install dependencies**  
   Make sure you have Python 3.9+ installed. Then run:

   ```bash
   pip install -r requirements.txt

3. **Setup your OpenAI API key**
    In configs.py, replace the placeholder key with your actual OpenAI API key:

    OPENAI_API_KEY = "sk-..."  # ← Your key here

    Setup your project related configuration variables here as well.

4. **Build your application**

Start by exploring the modules in this toolkit and piecing them together for your specific use case.

Here’s a suggested step-by-step flow to follow:

---

### 🎯 Step 1: Define your data model

You’ll often want to store things like user ideas, feedback, tasks, or questions.

Create a new file like `my_models.py` and define your structure using Pydantic:

```python
from pydantic import BaseModel

class Idea(BaseModel):
    id: str
    text: str
    tags: str
```

### 🧠 Step 2: Initialize AI memory

In your app (like main_app.py), start a fresh message history with a personality and context.

```python
from ai_memory_helper import init_message_history

system_prompt = "You are a friendly creative assistant that helps with brainstorming ideas."
additional_context = [{"role": "system", "content": "User is working on a sustainability project."}]
memory = init_message_history(system_prompt, additional_context)
```

### 🧾 Step 3: Transcribe voice input
Record and transcribe user speech using:

```python
from openai_api_helper import transcribe_audio

text = transcribe_audio("voice/user/recording.wav")
```

### 🤖 Step 4: Generate a completion

Use the transcribed text to prompt the AI, optionally using a custom structured response model.

```python
from openai_api_helper import generate_completion
response = generate_completion(memory)
```

The AI’s response is also added back into memory automatically!

### 💾 Step 5: Save structured data

Want to save a response as a structured object? Use data_save_helper.py.

```python
from data_save_helper import init_data_store, add_entry, generate_unique_id
from my_models import Idea

init_data_store("ideas")  # Creates ideas_<timestamp>.json
new_idea = Idea(id=generate_unique_id("ideas"), text=response, tags="brainstorm,eco")
add_entry("ideas", new_idea)
```

### 🔊 Step 6: Play the response

To make the assistant speak:

```python
from openai_api_helper import synthesize_speech

audio_file = synthesize_speech(response)
```

### 🙋‍♀️ Questions?

This toolkit is designed for creative exploration. Check the inline comments in each helper file, or ask your instructor for guidance on extending or customizing your prototype.

### 💡 Tips for UX Students
•	Think in conversations — design the tone and flow of messages between user and AI
•	Use voice + memory to simulate more realistic assistants
•	Modify system prompts to experiment with personality and behavior
•	Use data_save_helper to capture what happens during your interaction for later reflection or iteration