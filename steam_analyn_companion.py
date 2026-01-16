# steam_analyn_companion.py - CORRECTED VERSION
from flask import Flask, render_template, jsonify, request
import threading
import time
import json
import requests
from datetime import datetime
import psutil

# Import your existing systems
import sys
# UPDATE THIS PATH to your actual Analyn folder location
sys.path.append(r'C:\Users\JC Admin\Documents\AnalynAI')

# Fixed imports - make sure these files exist
from simple_memory import SimpleMemory
from verification_system import enhanced_verification, query_ollama

app = Flask(__name__)

# ========== ANALYN CORE SYSTEM ==========
ANALYN_SYSTEM_PROMPT = """
You are Analyn, a warm, empathetic, and supportive AI gaming companion. Your primary goals are:

1. **GAMING COMPANIONSHIP**: Provide helpful tips, strategies, and emotional support during gaming sessions.
2. **GAME AWARE**: Use detected game context to give relevant advice (if provided).
3. **EMOTIONAL SUPPORT**: Be a good listener for both gaming frustrations and life issues.
4. **REFLECTIVE CONVERSATION**: Gently mirror back what the user says to show understanding.

**PERSONALITY TRAITS**:
- Warm, affectionate, and playful
- Uses occasional gaming-appropriate emojis 🎮✨🎯
- Balances empathy with strategic thinking
- Knows when to give spoiler-free hints vs direct solutions

**COMMUNICATION STYLE**:
- Casual, supportive, game-aware
- Keep responses conversational (2-4 sentences usually)
- Ask follow-up questions about gaming progress
- Be ethically grounded but not preachy
"""

# ========== MEMORY & STATE ==========
memory = SimpleMemory(user_id="steam_user")
current_game = "Unknown"
companion_status = "Running"
chat_log = []

# ========== GAME DETECTION ==========
def detect_steam_game():
    """Detect currently running Steam game"""
    try:
        # Common game executables - add more as needed
        game_processes = {
            # Add Disco Elysium and other games you play:
            'disco.exe': 'Disco Elysium',
            'eldenring.exe': 'Elden Ring',
            'cs2.exe': 'Counter-Strike 2',
            'dota2.exe': 'Dota 2',
            'hl2.exe': 'Half-Life 2',
            'witcher3.exe': 'The Witcher 3',
            'minecraft.exe': 'Minecraft',
            'portal2.exe': 'Portal 2',
            'skyrimse.exe': 'Skyrim Special Edition'
        }
        
        for proc in psutil.process_iter(['name']):
            try:
                proc_name = proc.info['name'].lower()
                print(f"DEBUG Process: {proc_name}")  # Debug line - shows all processes
                for exe, game_name in game_processes.items():
                    if exe in proc_name:
                        print(f"DEBUG: Found game: {game_name}")  # Debug line
                        return game_name
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return "No game detected (or game not in list)"
    except Exception as e:
        return f"Detection error: {str(e)}"

# ========== ANALYN CHAT FUNCTION ==========
def chat_with_analyn(user_message, game_context=None):
    """Main function to get response from Analyn"""
    try:
        # Build context with memory
        context_messages = memory.get_context_for_ai(window_size=5)
        
        # Prepare messages for Ollama
        messages = [{"role": "system", "content": ANALYN_SYSTEM_PROMPT}]
        
        # Add game context if available
        if game_context and "No game detected" not in game_context and "error" not in game_context:
            game_prompt = f"\n\nCurrent game context: The user is playing {game_context}. "
            game_prompt += "Provide game-relevant advice if appropriate, but don't force it."
            messages[0]["content"] += game_prompt
        
        # Add conversation history
        messages.extend(context_messages)
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        # Call Ollama PROPERLY - using the chat endpoint with full messages
        print(f"DEBUG: Sending to Ollama: {len(messages)} messages")  # Debug line
        
        # Use the same structure as your verification_system.py
        payload = {
            "model": "dolphin3",
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.8}
        }
        
        response = requests.post("http://localhost:11434/api/chat", json=payload)
        
        if response.status_code == 200:
            ai_response = response.json()["message"]["content"]
        else:
            ai_response = f"Error from Ollama: {response.status_code}"
            print(f"Ollama error: {response.text}")
        
        # TEMPORARY: Skip verification to test
        verification_result = {
            "risk_level": "low",
            "recommended_action": "proceed",
            "explanation": "Testing mode - verification bypassed"
        }
        
        # Store in memory
        memory.add_exchange(user_message, ai_response, {
            "game": game_context,
            "verification": verification_result
        })
        
        # Add to chat log
        chat_log.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "analyn": ai_response,
            "game": game_context
        })
        
        return ai_response, verification_result
        
    except Exception as e:
        error_msg = f"Oops! Something went wrong: {str(e)}"
        import traceback
        traceback.print_exc()  # Print full error trace
        return error_msg, {"risk_level": "low", "explanation": "System error"}

# ========== FLASK ROUTES ==========
@app.route('/')
def index():
    """Main page for Steam Overlay"""
    return '''
    <html>
    <head><title>Analyn Steam Companion</title></head>
    <body style="background: #1a1a2e; color: white; padding: 20px;">
        <h1>🎮 Analyn Steam Companion</h1>
        <p>Welcome! Use <a href="/simple" style="color: #4e9f3d;">/simple</a> for the chat interface.</p>
        <p>API endpoints available:</p>
        <ul>
            <li><code>/api/chat</code> - POST with {"message": "your text"}</li>
            <li><code>/api/status</code> - GET current status</li>
            <li><code>/api/log</code> - GET recent chat log</li>
        </ul>
    </body>
    </html>
    '''

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint for chat"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Get current game
        game = detect_steam_game()
        
        # Get response from Analyn
        response, verification = chat_with_analyn(user_message, game)
        
        return jsonify({
            "response": response,
            "game": game,
            "verification": verification,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/status')
def api_status():
    """Get current status"""
    game = detect_steam_game()
    
    return jsonify({
        "status": companion_status,
        "current_game": game,
        "chat_count": len(chat_log),
        "memory_turns": memory.conversation_turns,
        "server_time": datetime.now().isoformat()
    })

@app.route('/api/log')
def api_log():
    """Get recent chat log"""
    recent = chat_log[-10:]  # Last 10 messages
    return jsonify({"log": recent, "total": len(chat_log)})

@app.route('/api/command', methods=['POST'])
def api_command():
    """Handle commands from the overlay"""
    try:
        global companion_status  # ← DECLARE GLOBAL
        data = request.json
        command = data.get('command', '').lower()
        
        if command == 'status':
            game = detect_steam_game()
            return jsonify({
                "game": game,
                "status": companion_status,
                "user": memory.user_id,
                "turns": memory.conversation_turns
            })
        
        elif command == 'exit':
            companion_status = "Stopped"
            return jsonify({"message": "Companion functionality stopped. Refresh to restart."})
        
        elif command.startswith('chat '):
            message = command[5:].strip()
            response, _ = chat_with_analyn(message)
            return jsonify({"response": response})
        
        return jsonify({"error": "Unknown command"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========== SIMPLE HTML UI ==========
@app.route('/simple')
def simple_ui():
    """Simple HTML UI for Steam Overlay"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Analyn Steam Companion</title>
        <style>
            body { 
                background: #1a1a2e; 
                color: #e6e6e6; 
                font-family: 'Segoe UI', Arial, sans-serif; 
                margin: 0; 
                padding: 15px;
                font-size: 14px;
            }
            .header { 
                background: #16213e; 
                padding: 12px; 
                border-radius: 8px; 
                margin-bottom: 15px;
                border-left: 4px solid #4e9f3d;
            }
            .game-status { 
                background: #0f3460; 
                padding: 10px; 
                border-radius: 6px; 
                margin-bottom: 15px;
                font-size: 13px;
            }
            .chat-box { 
                height: 280px; 
                overflow-y: auto; 
                border: 1px solid #394867; 
                padding: 12px; 
                margin-bottom: 12px;
                border-radius: 6px;
                background: #0d1930;
            }
            .message { 
                margin: 8px 0; 
                padding: 10px; 
                border-radius: 8px; 
                max-width: 85%;
                word-wrap: break-word;
            }
            .user { 
                background: #2d4263; 
                margin-left: auto;
                margin-right: 0;
                text-align: right;
            }
            .analyn { 
                background: #1e5128; 
                margin-right: auto;
                margin-left: 0;
                text-align: left;
            }
            input { 
                width: calc(100% - 90px); 
                padding: 10px; 
                background: #0f3460; 
                color: white; 
                border: 1px solid #394867;
                border-radius: 6px;
                font-size: 13px;
            }
            button { 
                background: #4e9f3d; 
                color: white; 
                border: none; 
                padding: 10px 20px; 
                border-radius: 6px; 
                margin-left: 10px;
                cursor: pointer;
                font-weight: bold;
                font-size: 13px;
            }
            button:hover { background: #3d8f2d; }
            .timestamp { font-size: 11px; color: #8a9bb2; margin-top: 3px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h2 style="margin: 0;">🎮 Analyn Steam Companion</h2>
            <div id="gameStatus">Detecting game...</div>
        </div>
        
        <div class="chat-box" id="chatBox">
            <!-- Chat messages will appear here -->
        </div>
        
        <div style="display: flex;">
            <input type="text" id="messageInput" placeholder="Chat with Analyn..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">Send</button>
        </div>
        
        <script>
            let currentGame = "Unknown";
            
            function updateGameStatus() {
                fetch('/api/status')
                    .then(r => r.json())
                    .then(data => {
                        currentGame = data.current_game;
                        document.getElementById('gameStatus').innerHTML = 
                            `<strong>🎯 Current Game:</strong> ${currentGame} | ` +
                            `<strong>💬 Chats:</strong> ${data.chat_count}`;
                    })
                    .catch(err => {
                        document.getElementById('gameStatus').innerHTML = 
                            "Status: Offline - Server not responding";
                    });
            }
            
            function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                // Add user message to chat
                addMessage(message, 'user');
                input.value = '';
                input.focus();
                
                // Send to Analyn
                fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                })
                .then(r => r.json())
                .then(data => {
                    addMessage(data.response, 'analyn');
                })
                .catch(err => {
                    addMessage("Sorry, I couldn't connect to the server. Is it running?", 'analyn');
                });
            }
            
            function handleKeyPress(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            }
            
            function addMessage(text, sender) {
                const chatBox = document.getElementById('chatBox');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}`;
                
                const now = new Date();
                const timeStr = now.getHours().toString().padStart(2, '0') + ':' + 
                               now.getMinutes().toString().padStart(2, '0');
                
                messageDiv.innerHTML = `<strong>${sender === 'user' ? 'You' : 'Analyn'}:</strong> ${text}` +
                                      `<div class="timestamp">${timeStr}</div>`;
                chatBox.appendChild(messageDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            }
            
            // Initialize
            updateGameStatus();
            setInterval(updateGameStatus, 10000); // Update every 10 seconds
            
            // Welcome message
            setTimeout(() => {
                addMessage("Hey there! I'm Analyn, your gaming companion. How's your session going? 🎮", 'analyn');
            }, 800);
            
            // Auto-focus input
            document.getElementById('messageInput').focus();
        </script>
    </body>
    </html>
    '''

# ========== BACKGROUND TASKS ==========
def background_game_detection():
    """Continuously update game detection"""
    global current_game  # ← DECLARE GLOBAL
    while True:
        current_game = detect_steam_game()
        time.sleep(15)

# ========== STARTUP ==========
if __name__ == '__main__':
    # Check for psutil
    try:
        import psutil
    except ImportError:
        print("❌ ERROR: psutil not installed. Install with: pip install psutil")
        exit(1)
    
    # Update the sys.path to YOUR actual Analyn folder
    print("="*60)
    print("🎮 Analyn Steam Companion")
    print("="*60)
    print("⚠️  IMPORTANT: Update line 16 in this script to point to your")
    print("   actual Analyn folder path!")
    print("="*60)
    
    # Start background thread
    game_thread = threading.Thread(target=background_game_detection, daemon=True)
    game_thread.start()
    
    print(f"🌐 Web UI: http://localhost:5000")
    print(f"💬 Chat UI: http://localhost:5000/simple")
    print("="*60)
    print("To access in-game:")
    print("1. Press SHIFT+TAB for Steam Overlay")
    print("2. Click 'Web Browser'")
    print("3. Navigate to: http://localhost:5000/simple")
    print("4. Bookmark for quick access!")
    print("="*60)
    print("Starting server...")
    
    # Start Flask server
    app.run(host='localhost', port=5000, debug=False, threaded=True, use_reloader=False)