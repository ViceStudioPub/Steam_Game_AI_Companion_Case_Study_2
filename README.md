# Analyn Steam AI Companion

*A lightweight, game-aware AI companion that runs in Steam Overlay, providing contextual assistance and emotional support during gaming sessions.*

## 🎯 Project Overview

Analyn is a local AI companion built to integrate seamlessly with Steam games. She provides:
- **Game-aware assistance** (tips, strategies, lore help)
- **Emotional support** during challenging gameplay
- **Conversational companionship** via Ollama's local LLMs
- **Steam Overlay integration** for in-game access without alt-tabbing

## 🏗️ Architecture


### Core Components:
- **`steam_analyn_companion.py`** - Main Flask server with web interface
- **`memory_system.py`** - Conversation memory and emotional state tracking
- **`verification_system.py`** - Safety verification layer
- **`simple_memory.py`** - Fallback memory system (no ChromaDB dependency)
- **Game Detection** - Real-time process monitoring for contextual awareness

## 🚀 Features

### ✅ Implemented
- **Steam Overlay Integration**: Access via `Shift+Tab` → Web Browser → `localhost:5000/simple`
- **Real-time Game Detection**: Automatically detects running Steam games
- **Local AI Processing**: Uses Ollama with `dolphin3` model (privacy-focused)
- **Conversation Memory**: Remains context-aware across sessions
- **Safety Verification**: Two-layer safety system with configurable strictness
- **Low Resource Usage**: Designed to minimize impact on gaming performance

### ⚠️ Current Limitations

#### Technical Constraints
1. **No Screen Analysis**: Analyn cannot see your screen or game visuals
2. **Text-Only Interface**: Communication is via chat only (no voice)
3. **Game Detection Limited**: Currently recognizes ~10 popular games via process names
4. **Local Only**: Requires local Ollama instance; no cloud fallback
5. **Python 3.14 Compatibility Issues**: Some libraries (ChromaDB) not fully compatible

#### Functional Boundaries
1. **No Game Control**: Cannot interact with or control your game
2. **No Real-time Stats**: Cannot read health, inventory, or game state
3. **No Spoilers**: Deliberately avoids specific spoilers; offers general guidance
4. **Response Latency**: 2-5 second response time depending on model load

## 🛠️ Setup Guide

### Prerequisites
- Python 3.14+ (tested with 3.14.0)
- [Ollama](https://ollama.com/) with `dolphin3` model
- Steam client with overlay enabled
- Windows 10/11 (game detection optimized for Windows)

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/steam-ai-companion.git
cd steam-ai-companion

# Install dependencies
pip install flask psutil requests numpy

# Install Ollama (if not already installed)
# Download from https://ollama.com/

# Pull the AI model
ollama pull dolphin3




Here's a comprehensive `README.md` you can publish with your project. It documents your process, setup, and important limitations clearly:

```markdown
# Analyn Steam AI Companion

*A lightweight, game-aware AI companion that runs in Steam Overlay, providing contextual assistance and emotional support during gaming sessions.*

## 🎯 Project Overview

Analyn is a local AI companion built to integrate seamlessly with Steam games. She provides:
- **Game-aware assistance** (tips, strategies, lore help)
- **Emotional support** during challenging gameplay
- **Conversational companionship** via Ollama's local LLMs
- **Steam Overlay integration** for in-game access without alt-tabbing

## 🏗️ Architecture

```
Steam Game → Steam Overlay (Shift+Tab) → Local Flask Server → Ollama AI → Game Context → Response
```

### Core Components:
- **`steam_analyn_companion.py`** - Main Flask server with web interface
- **`memory_system.py`** - Conversation memory and emotional state tracking
- **`verification_system.py`** - Safety verification layer
- **`simple_memory.py`** - Fallback memory system (no ChromaDB dependency)
- **Game Detection** - Real-time process monitoring for contextual awareness

## 🚀 Features

### ✅ Implemented
- **Steam Overlay Integration**: Access via `Shift+Tab` → Web Browser → `localhost:5000/simple`
- **Real-time Game Detection**: Automatically detects running Steam games
- **Local AI Processing**: Uses Ollama with `dolphin3` model (privacy-focused)
- **Conversation Memory**: Remains context-aware across sessions
- **Safety Verification**: Two-layer safety system with configurable strictness
- **Low Resource Usage**: Designed to minimize impact on gaming performance

### ⚠️ Current Limitations

#### Technical Constraints
1. **No Screen Analysis**: Analyn cannot see your screen or game visuals
2. **Text-Only Interface**: Communication is via chat only (no voice)
3. **Game Detection Limited**: Currently recognizes ~10 popular games via process names
4. **Local Only**: Requires local Ollama instance; no cloud fallback
5. **Python 3.14 Compatibility Issues**: Some libraries (ChromaDB) not fully compatible

#### Functional Boundaries
1. **No Game Control**: Cannot interact with or control your game
2. **No Real-time Stats**: Cannot read health, inventory, or game state
3. **No Spoilers**: Deliberately avoids specific spoilers; offers general guidance
4. **Response Latency**: 2-5 second response time depending on model load

## 🛠️ Setup Guide

### Prerequisites
- Python 3.14+ (tested with 3.14.0)
- [Ollama](https://ollama.com/) with `dolphin3` model
- Steam client with overlay enabled
- Windows 10/11 (game detection optimized for Windows)

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/steam-ai-companion.git
cd steam-ai-companion

# Install dependencies
pip install flask psutil requests numpy

# Install Ollama (if not already installed)
# Download from https://ollama.com/

# Pull the AI model
ollama pull dolphin3
```

### Configuration
1. **Update Paths**: Edit `steam_analyn_companion.py` line 16 with your project path
2. **Add Games**: Extend the `game_processes` dictionary with your games' .exe names
3. **Customize Prompts**: Modify `ANALYN_SYSTEM_PROMPT` for different personality/game focus

### Running
```bash
# Start the companion
python steam_analyn_companion.py

# In-game: Press Shift+Tab → Web Browser → http://localhost:5000/simple
# Bookmark for quick access!
```

## 📚 Development Journey

### Key Learnings
1. **Python 3.14 Compatibility**: Had to work around ChromaDB incompatibility by implementing `chromadb-client` fallback
2. **Steam Integration Challenges**: Game detection via process monitoring proved more reliable than Steam API
3. **Prompt Engineering**: Iteratively developed system prompts balancing helpfulness with safety
4. **Resource Management**: Optimized memory usage to avoid impacting game performance

### Technical Decisions
- **Chose Ollama over cloud APIs** for privacy and offline functionality
- **Implemented two-tier memory system** (SimpleMemory + ChromaDB) for flexibility
- **Designed for Steam Overlay** rather than external window for seamless experience
- **Built verification system** to maintain ethical boundaries while gaming

## 🔮 Future Enhancements

### Planned Features
1. **Game-Specific Modules**: Dedicated helpers for popular games (Elden Ring, Disco Elysium, etc.)
2. **Performance Monitoring**: Optional FPS/game performance tracking
3. **Voice Integration**: Text-to-speech for responses
4. **Community Game Database**: Crowdsourced game detection patterns

### Research Areas
1. **Lightweight Screen Analysis**: Exploring OCR for minimal text reading
2. **Predictive Assistance**: Anticipating player needs based on game progress
3. **Cross-Platform Support**: Extending to other gaming platforms

## 🧪 Testing Results

### What Works Well
- Game detection accurately identifies running processes
- Ollama integration provides low-latency, contextual responses
- Steam Overlay integration is seamless and non-intrusive
- Memory system maintains conversation context effectively

### Known Issues
- Sometimes triggers safety verification too aggressively
- Game detection requires manual .exe entry for new games
- No automatic updates when switching games mid-conversation

## 🤝 Contributing

This is a learning project open to:
- Game detection improvements
- Prompt engineering experiments
- Performance optimizations
- Additional game-specific modules

### Areas Needing Contribution:
1. **More Games**: Add detection for additional Steam games
2. **Linux/Mac Support**: Adapt game detection for other OS
3. **UI Improvements**: Better Steam Overlay interface design
4. **Documentation**: Additional setup guides and tutorials

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- **Ollama** for making local LLMs accessible
- **Flask** for lightweight web server framework
- **Steam** for providing overlay functionality
- **Disco Elysium** for being the perfect testbed for narrative-focused AI assistance

---

*"The perfect gaming companion doesn't alt-tab."*
```

## 📁 **Suggested Repository Structure:**
```
Steam_AI_Analyn_Companion/
├── README.md                    # This file
├── steam_analyn_companion.py    # Main Flask server
├── memory_system.py            # Enhanced memory with fallback
├── simple_memory.py            # Lightweight memory system
├── verification_system.py      # Safety/verification layer
├── simple_companion.py         # Original standalone version
├── requirements.txt            # Python dependencies
├── companion_memory.json       # Conversation history (gitignored)
├── chroma_memory/              # Vector DB storage (gitignored)
└── screenshots/
    ├── steam_overlay_working.png
    ├── game_detection_working.png
    └── chat_examples.png
```

## 🎯 **Publishing Tips:**

1. **Add a `requirements.txt`:**
   ```txt
   flask>=2.3.0
   psutil>=5.9.0
   requests>=2.31.0
   numpy>=1.24.0
   chromadb-client>=1.4.0
   ```

2. **Create `.gitignore`:**
   ```gitignore
   __pycache__/
   *.pyc
   companion_memory.json
   chroma_memory/
   *.log
   venv/
   .env
   ```

3. **Include a simple setup script** (`setup.bat` for Windows):
   ```batch
   @echo off
   echo Installing Analyn Steam Companion...
   pip install -r requirements.txt
   echo.
   echo Downloading dolphin3 model...
   ollama pull dolphin3
   echo.
   echo Setup complete! Run: python steam_analyn_companion.py
   pause
   ```
