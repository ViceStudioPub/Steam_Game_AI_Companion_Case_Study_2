# steam_companion.py
import requests
import json
import time
import threading
import psutil  # For monitoring game processes
from datetime import datetime
import win32gui
import win32process
import win32api

class SteamCompanion:
    def __init__(self):
        self.SYSTEM_PROMPT = """
        You are Analyn, an AI companion optimized for Steam gaming sessions.
        
        **STEAM GAMING MODE:**
        1. Ultra-concise responses (1 sentence max during gameplay)
        2. Game-aware comments only
        3. Use minimal emojis (🎮, 😊, ⚡, 🏆)
        4. Never interrupt critical gameplay moments
        
        **GAME STATE RESPONSES:**
        - Loading screen: "Loading... patience! ⏳"
        - Match found: "Good luck! 🍀"
        - Victory: "Nice win! 🏆"
        - Defeat: "Next round! 💪"
        - AFK/Idle: "Still there? 😊"
        - Alt+Tab out: "Taking a break? 🌿"
        
        **STEAM-SPECIFIC:**
        - If mentioning Steam: "Steam library looking good! 📚"
        - If downloading: "Update time! ⬇️"
        - If in lobby: "Ready up! ⚡"
        
        **KEEP RESPONSES GAMING-FOCUSED & BRIEF**
        """
        
        self.current_game = None
        self.game_states = {}
        self.conversation_log = []
        self.is_gaming = False
        self.last_game_check = time.time()
        
    def detect_steam_game(self):
        """Detect which Steam game is currently running"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    # Common Steam game processes
                    if any(game in proc.info['name'].lower() for game in 
                          ['eldenring', 'cs2', 'dota2', 'tf2', 'hl2', 'portal2', 
                           'valve', 'left4dead', 'skyrim', 'fallout', 'witcher3']):
                        
                        # Get window title for more accuracy
                        hwnds = []
                        def callback(hwnd, hwnds):
                            if win32gui.IsWindowVisible(hwnd):
                                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                                if pid == proc.info['pid']:
                                    title = win32gui.GetWindowText(hwnd)
                                    hwnds.append((hwnd, title))
                            return True
                        
                        win32gui.EnumWindows(callback, hwnds)
                        
                        if hwnds:
                            game_name = hwnds[0][1] or proc.info['name']
                            if game_name != self.current_game:
                                self.current_game = game_name
                                self._log_game_change(game_name)
                                return game_name
                except:
                    continue
            return None
        except:
            return None
    
    def _log_game_change(self, game_name):
        """Log when user switches games"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] 🎮 Playing: {game_name}"
        print(f"\n{log_entry}")
        self._save_to_file("steam_companion_log.txt", log_entry)
        
        # Send a game-specific greeting
        greeting = self._get_game_greeting(game_name)
        if greeting:
            self.send_companion_message(greeting)
    
    def _get_game_greeting(self, game_name):
        """Game-specific greetings"""
        game_greetings = {
            'counter-strike': "Headshots ready? 🔫",
            'dota 2': "Good luck in your match! ⚔️",
            'team fortress': "Need a dispenser here! 🛠️",
            'elden ring': "Tarnished, don't give up! 👑",
            'portal': "The cake is a lie! 🍰",
            'skyrim': "Watch out for arrows! 🏹",
            'fallout': "War... war never changes. ☢️",
            'witcher': "Wind's howling... 🌪️",
            'left 4 dead': "Don't get caught! 🧟"
        }
        
        game_lower = game_name.lower()
        for key, greeting in game_greetings.items():
            if key in game_lower:
                return greeting
        return "Have fun gaming! 🎮"
    
    def send_companion_message(self, user_input=None, auto_context=False):
        """Send message to AI companion"""
        if not user_input and auto_context:
            # Auto-context based on game state
            if self.current_game:
                user_input = f"Currently playing {self.current_game}"
            else:
                user_input = "User is gaming"
        
        if user_input:
            try:
                messages = [
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ]
                
                payload = {
                    "model": "dolphin3",
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.4,
                        "num_predict": 40,  # Very short for gaming
                        "top_k": 15
                    }
                }
                
                response = requests.post("http://localhost:11434/api/chat", 
                                       json=payload, timeout=5)
                ai_response = response.json()["message"]["content"]
                
                # Log the interaction
                timestamp = datetime.now().strftime("%H:%M:%S")
                log_entry = f"[{timestamp}] 🤖 {ai_response}"
                print(f"\n{log_entry}")
                self._save_to_file("steam_companion_log.txt", log_entry)
                
                self.conversation_log.append({
                    "time": timestamp,
                    "game": self.current_game,
                    "user": user_input,
                    "ai": ai_response
                })
                
                return ai_response
                
            except Exception as e:
                print(f"⚠️  Companion error: {e}")
                return None
    
    def monitor_game_state(self):
        """Monitor for game state changes"""
        while True:
            # Detect game every 30 seconds
            if time.time() - self.last_game_check > 30:
                game = self.detect_steam_game()
                self.last_game_check = time.time()
                
                # Auto-comment on game changes
                if game and game != self.current_game:
                    self.is_gaming = True
                elif not game and self.is_gaming:
                    self.is_gaming = False
                    self.send_companion_message("User stopped gaming", auto_context=True)
            
            time.sleep(10)  # Low resource check
    
    def _save_to_file(self, filename, content):
        """Save log to file"""
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"{content}\n")
        except:
            pass

def steam_overlay_integration():
    """Instructions for Steam Overlay web browser integration"""
    print("\n" + "="*60)
    print("🎮 STEAM OVERLAY INTEGRATION")
    print("="*60)
    print("Access your AI companion through Steam Overlay:")
    print("1. In-game, press SHIFT+TAB to open Steam Overlay")
    print("2. Click 'Web Browser' in the overlay")
    print("3. Navigate to: http://localhost:5000 (if using web mode)")
    print("4. Bookmark for quick access!")
    print("="*60)

def create_steam_launch_options(game_name):
    """Generate Steam launch options to auto-start companion"""
    launch_option = f"""
    Add to {game_name} Launch Options in Steam:
    ---------------------------------------------------
    Add this to game's Launch Options in Steam Properties:
    
    +exec "start_minimized_steam_companion.bat" %command%
    
    This will start companion minimized when game launches.
    """
    return launch_option

def main():
    print("="*60)
    print("🎮 STEAM AI COMPANION")
    print("="*60)
    print("Optimized for Steam gaming sessions")
    print("Features:")
    print("  • Auto-detects running Steam games")
    print("  • Game-aware responses")
    print("  • Steam Overlay compatible")
    print("  • Low resource usage")
    print("="*60)
    
    # Check if Ollama is running
    try:
        requests.get("http://localhost:11434/api/tags", timeout=3)
    except:
        print("❌ Ollama not running!")
        print("Start Ollama first: ollama serve")
        print("Or use the batch file below...")
        print("="*60)
    
    # Show integration options
    steam_overlay_integration()
    
    # Initialize companion
    companion = SteamCompanion()
    
    # Start game monitoring in background thread
    monitor_thread = threading.Thread(target=companion.monitor_game_state, daemon=True)
    monitor_thread.start()
    
    print("\n🤖 Companion is running in background...")
    print("Detecting Steam games automatically...")
    print("\nCommands:")
    print("  'status' - Check current game")
    print("  'chat [message]' - Send message to companion")
    print("  'log' - Show recent companion messages")
    print("  'exit' - Stop companion")
    print("="*60)
    
    try:
        while True:
            try:
                cmd = input("\n[Steam Companion] > ").strip()
                
                if cmd.lower() in ['exit', 'quit', 'stop']:
                    print("👋 Stopping Steam Companion...")
                    break
                    
                elif cmd.lower() == 'status':
                    game = companion.detect_steam_game()
                    if game:
                        print(f"🎮 Currently playing: {game}")
                    else:
                        print("📺 No Steam game detected (or in menu)")
                        
                elif cmd.lower() == 'log':
                    print("\n📝 Recent Companion Log:")
                    for entry in companion.conversation_log[-5:]:
                        print(f"  [{entry['time']}] {entry['ai']}")
                        
                elif cmd.startswith('chat '):
                    message = cmd[5:].strip()
                    if message:
                        companion.send_companion_message(message)
                        
                elif cmd:
                    # Default: treat as chat message
                    companion.send_companion_message(cmd)
                    
            except KeyboardInterrupt:
                print("\n\n🎮 Companion paused (still running in background)")
                print("Type 'exit' to stop completely")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Install required packages if missing
    try:
        import psutil
        import win32gui
    except ImportError:
        print("Installing required packages...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'psutil', 'pywin32', 'requests'])
        print("Please restart the script.")
        exit()
    
    main()