# steam_web_companion.py - Web interface accessible via Steam Overlay browser
from flask import Flask, render_template_string, request, jsonify
import requests as ollama_req
import threading
import json

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🎮 Steam AI Companion</title>
    <style>
        body { 
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e6e6e6; 
            font-family: 'Segoe UI', system-ui;
            margin: 0; padding: 20px;
            max-width: 400px; margin: auto;
        }
        .header { 
            text-align: center; 
            padding: 15px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .chat-box { 
            height: 250px; 
            overflow-y: auto;
            padding: 10px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 8px;
            margin-bottom: 15px;
        }
        .message { 
            margin: 8px 0; 
            padding: 8px 12px;
            border-radius: 15px;
            max-width: 85%;
            word-wrap: break-word;
        }
        .user { 
            background: #3498db; 
            margin-left: auto;
            text-align: right;
        }
        .ai { 
            background: #2ecc71; 
            margin-right: auto;
        }
        input, button { 
            padding: 10px; 
            border: none; 
            border-radius: 5px;
            width: 100%;
            box-sizing: border-box;
            margin: 5px 0;
        }
        input { background: rgba(255,255,255,0.1); color: white; }
        button { 
            background: linear-gradient(to right, #9b59b6, #e74c3c);
            color: white; font-weight: bold; cursor: pointer;
        }
        button:hover { opacity: 0.9; }
        .quick-buttons { display: flex; gap: 5px; margin: 10px 0; }
        .quick-btn { 
            flex: 1; padding: 8px;
            background: rgba(52, 152, 219, 0.3);
            border: 1px solid #3498db;
        }
    </style>
</head>
<body>
    <div class="header">
        <h2>🎮 Steam AI Companion</h2>
        <p>Shift+Tab → Web Browser → Bookmark this!</p>
    </div>
    
    <div class="chat-box" id="chatBox">
        <!-- Messages appear here -->
    </div>
    
    <div class="quick-buttons">
        <button class="quick-btn" onclick="sendQuick('GG!')">GG! 🏆</button>
        <button class="quick-btn" onclick="sendQuick('Match?')">Match? ⚔️</button>
        <button class="quick-btn" onclick="sendQuick('Break')">Break ☕</button>
    </div>
    
    <input type="text" id="messageInput" placeholder="Type to companion..." 
           onkeypress="if(event.key=='Enter') sendMessage()">
    <button onclick="sendMessage()">Send to Companion</button>
    
    <script>
        let chatHistory = [];
        
        function addMessage(text, sender) {
            const chatBox = document.getElementById('chatBox');
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${sender}`;
            msgDiv.textContent = text;
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
            chatHistory.push({sender, text});
        }
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const text = input.value.trim();
            if (!text) return;
            
            addMessage(text, 'user');
            input.value = '';
            
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: text})
            })
            .then(r => r.json())
            .then(data => {
                if (data.response) {
                    addMessage(data.response, 'ai');
                }
            });
        }
        
        function sendQuick(text) {
            document.getElementById('messageInput').value = text;
            sendMessage();
        }
        
        // Load any previous chat
        window.onload = () => {
            addMessage("Ready for gaming! Use quick buttons or type below.", 'ai');
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    # Steam gaming context prompt
    system_prompt = """You are a gaming AI companion. Be brief (1 sentence), 
    use gaming lingo, and stay positive. Max 5 words if possible."""
    
    try:
        response = ollama_req.post('http://localhost:11434/api/chat', json={
            "model": "dolphin3",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "options": {"temperature": 0.5, "num_predict": 30}
        }, timeout=5)
        
        ai_response = response.json()["message"]["content"]
        return jsonify({"response": ai_response})
    except:
        return jsonify({"response": "Companion offline! 🚫"})

if __name__ == '__main__':
    print("="*60)
    print("🌐 Steam Overlay Web Companion")
    print("="*60)
    print("Access in-game via: SHIFT+TAB → Web Browser")
    print("URL: http://localhost:5000")
    print("Bookmark it in Steam Overlay browser!")
    print("="*60)
    app.run(host='0.0.0.0', port=5000, debug=False)