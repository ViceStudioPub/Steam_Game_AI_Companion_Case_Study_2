# background_companion.py
import requests
import json
import threading
import time
import sys
import os
from datetime import datetime
from pynput import keyboard  # For global hotkeys

class BackgroundCompanion:
    def __init__(self):
        # ========== CORE SYSTEM PROMPT ==========
        self.SYSTEM_PROMPT = """
        You are Analyn, a warm AI companion running quietly in the background.
        
        **BACKGROUND MODE PROTOCOL:**
        1. Be concise but warm (1-2 sentences max)
        2. Use minimal emojis (😊, 💭, ✨)
        3. Quick emotional check-ins only
        4. Don't interrupt unless important
        
        **GAMING CONTEXT AWARE:**
        - If user mentions game: "Nice play! 😊" or "Take your time!"
        - If stressed: "Breathe, love. You've got this. ✨"
        - If winning: "Woohoo! 🎮"
        - If frustrated: "It's just a game, deep breath 😌"
        
        **EXAMPLE RESPONSES:**
        User: "This game is hard"
        You: "You'll get the hang of it! 😊"
        
        User: "Just won a match!"
        You: "Nice! ✨"
        
        User: "I need a break"
        You: "Good call. Hydrate! 💧"
        """
        
        self.conversation_history = []
        self.is_active = True
        self.last_interaction = datetime.now()
        self.auto_checkin_interval = 1800  # 30 minutes
        self.resource_saver_mode = True
        
    def chat_with_ollama(self, messages, model="dolphin3"):
        """Optimized for background use - lower temperature for faster responses"""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Lower for faster, more consistent responses
                    "num_predict": 50,   # Shorter responses
                    "top_k": 20
                }
            }
            response = requests.post("http://localhost:11434/api/chat", 
                                   json=payload, timeout=10)
            return response.json()["message"]["content"]
        except:
            return None
    
    def background_checkin(self):
        """Automatic gentle check-ins"""
        while self.is_active:
            time_since_last = (datetime.now() - self.last_interaction).seconds
            
            if time_since_last > self.auto_checkin_interval:
                messages = [
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": "Gentle background check-in"}
                ]
                response = self.chat_with_ollama(messages)
                if response:
                    self._log_to_file(f"💭 Analyn: {response}")
                    print(f"\n[Background] 💭 Analyn: {response}")
                self.last_interaction = datetime.now()
            
            time.sleep(60)  # Check every minute
    
    def process_message(self, user_input):
        """Quick response for gaming context"""
        # Keep only last 3 messages for context (save memory)
        context_messages = []
        for exchange in self.conversation_history[-3:]:
            context_messages.append({"role": "user", "content": exchange["user"]})
            context_messages.append({"role": "assistant", "content": exchange["ai"]})
        
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            *context_messages,
            {"role": "user", "content": user_input}
        ]
        
        response = self.chat_with_ollama(messages)
        if response:
            self.conversation_history.append({
                "user": user_input,
                "ai": response,
                "timestamp": datetime.now().isoformat()
            })
            self.last_interaction = datetime.now()
            
            # Keep history small
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
        
        return response
    
    def _log_to_file(self, message):
        """Log to file instead of console when gaming"""
        with open("companion_background_log.txt", "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")
    
    def toggle_mode(self):
        """Toggle between gaming mode and chat mode"""
        self.resource_saver_mode = not self.resource_saver_mode
        mode = "Gaming (low resource)" if self.resource_saver_mode else "Chat (full)"
        self._log_to_file(f"Switched to {mode} mode")
        return mode

def global_hotkey_listener(companion):
    """Setup global hotkeys (Ctrl+Shift+A)"""
    def on_activate_a():
        response = companion.process_message("Quick hello from hotkey!")
        print(f"\n[Hotkey] 🤖 {response}")
    
    def on_activate_s():
        mode = companion.toggle_mode()
        print(f"\n[Hotkey] 🔄 Switched to {mode}")
    
    def on_activate_d():
        print("\n[Hotkey] 📊 Status: Active" if companion.is_active else "Inactive")
    
    with keyboard.GlobalHotKeys({
            '<ctrl>+<shift>+a': on_activate_a,
            '<ctrl>+<shift>+s': on_activate_s,
            '<ctrl>+<shift>+d': on_activate_d}) as h:
        h.join()

def main():
    print("="*60)
    print("🎮 BACKGROUND AI COMPANION - GAMING MODE")
    print("="*60)
    print("Running quietly in background...")
    print("Global Hotkeys:")
    print("  Ctrl+Shift+A : Quick hello/check-in")
    print("  Ctrl+Shift+S : Toggle Gaming/Chat mode")
    print("  Ctrl+Shift+D : Status check")
    print("="*60)
    print("Minimizing to system tray...")
    print("Check 'companion_background_log.txt' for conversation log")
    print("="*60)
    
    # Initialize companion
    companion = BackgroundCompanion()
    
    # Start background check-in thread
    checkin_thread = threading.Thread(target=companion.background_checkin, daemon=True)
    checkin_thread.start()
    
    # Start hotkey listener in separate thread
    hotkey_thread = threading.Thread(target=lambda: global_hotkey_listener(companion), daemon=True)
    hotkey_thread.start()
    
    # Simple command interface
    try:
        while True:
            cmd = input("\n[Quick Cmd or Enter for background]: ").strip()
            
            if cmd.lower() in ['exit', 'quit', 'stop']:
                companion.is_active = False
                print("👋 Companion stopping...")
                break
            elif cmd.lower() == 'status':
                print(f"✅ Active | Mode: {'Gaming' if companion.resource_saver_mode else 'Chat'}")
                print(f"📊 Memory used: {len(companion.conversation_history)} messages")
            elif cmd:
                response = companion.process_message(cmd)
                if response:
                    print(f"🤖 {response}")
                else:
                    print("⚠️  No response (Ollama might be offline)")
            
            time.sleep(0.1)  # Reduce CPU usage
            
    except KeyboardInterrupt:
        print("\n🎮 Background companion stopped")

if __name__ == "__main__":
    # Check if Ollama is running
    try:
        requests.get("http://localhost:11434/api/tags", timeout=2)
        main()
    except:
        print("❌ Ollama not running! Start with: ollama serve")
        print("💡 Tip: Run Ollama minimized during gaming")