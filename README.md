# 🥪 Snaxi: Your Goofy Onboarding Buddy

Snaxi is a private AI-powered assistant that helps new employees (or anyone learning something new) quickly understand documentation.  
Upload your files (PDF, DOCX, TXT), and Snaxi will chunk them, embed them, and let you chat with them.  
It’s like having a goofy, snack-loving buddy that explains boring manuals in plain English. 😋  

---

## ✨ Features
- 📂 Upload PDFs, DOCX, or TXT files
- 🔍 Semantic search using embeddings (MiniLM + Chroma)
- 💬 Chat with your documents via local LLM (Ollama + Mistral/Dolphin-Mistral)
- 📝 Save notes during chats (auto-saved to `notes/`)
- 🎨 Fun, goofy personality to keep things light

---

## 🛠️ Installation

### 1. Clone the repo
```bash
git clone https://github.com/Rachel-VA/Snaxi_Onborading_Smart_Assistant_AI-LLM.git
cd Snaxi_Onborading_Smart_Assistant_AI-LLM

# Requirements

Python 3.11.5

Ollama
 with mistral:latest or dolphin-mistral:7b model installed

pip (latest version recommended)


## Note
This project uses two local folders during runtime:

data/chroma/ → stores the vector database (embeddings).

notes/ → stores saved notes created by the user.

These folders are not included in the repository because:

They can become very large (hundreds of MB).

They are generated dynamically when you run the project.

Notes are user-specific and private.
