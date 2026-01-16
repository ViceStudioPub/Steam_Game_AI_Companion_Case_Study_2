# steam_companion_fixed.py
import requests
import json
import time
import threading
import sys
import os
from datetime import datetime
import subprocess
import psutil

def create_minimized_window():
    """Run in minimized window (Windows specific)"""
    if os.name == 'nt':
        # This creates a minimized console window
        subprocess.Popen([sys.executable, __file__], 
                        creationflags=subprocess.CREATE_NO_WINDOW)
        sys.exit(0)

class SteamCompanionBackground:
    def __init__(self):
        self.SYSTEM_PROMPT = """You are Analyn, a Steam gaming companion."""
        self.is_running = True
        self.check_interval = 300  # 5 minutes
        self.game_detected = False
        
    def send_message(self, message):
        """Send message to Ollama (ultra-fast mode)"""
        try:
            payload = {
                "model": "dolphin3",
                "messages": [
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": message}
                ],
                "stream": False,
                "options": {"temperature": 0.3, "num_predict": 30}
            }
            response = requests.post("http://localhost:11434/api/chat", 
                                   json=payload, timeout=3)
            return response.json()["message"]["content"]
        except:
            return None
    
    def check_gaming_status(self):
        """Check if user is gaming"""
        try:
            for proc in psutil.process_iter(['name']):
                if 'steam' in proc.info['name'].lower():
                    return True
                if any(game in proc.info['name'].lower() for game in 
                      ['cs2', 'dota2', 'eldenring', 'hl2', 'game', '.exe']):
                    return True
            return False
        except:
            return False
    
    def background_loop(self):
        """Main background loop - NO USER INPUT REQUIRED"""
        print("🎮 Steam Companion running in background...")
        print("📝 Logging to: companion_log.txt")
        print("🛑 To stop: Check Task Manager for python.exe")
        print("="*50)
        
        last_status = False
        log_count = 0
        
        while self.is_running:
            # Check gaming status
            gaming_now = self.check_gaming_status()
            
            # Log status changes
            if gaming_now != last_status:
                timestamp = datetime.now().strftime("%H:%M:%S")
                status_msg = f"[{timestamp}] {'🎮 Gaming detected' if gaming_now else '📺 Not gaming'}"
                self._log_to_file(status_msg)
                print(status_msg)
                last_status = gaming_now
                
                # Auto-message on game start
                if gaming_now and log_count % 3 == 0:  # Every 3rd game detection
                    response = self.send_message("User started gaming")
                    if response:
                        log_msg = f"[{timestamp}] 🤖 {response}"
                        self._log_to_file(log_msg)
            
            # Sleep to reduce CPU usage
            time.sleep(30)  # Check every 30 seconds
            log_count += 1
    
    def _log_to_file(self, message):
        """Log to file only - no console spam"""
        try:
            with open("companion_log.txt", "a", encoding="utf-8") as f:
                f.write(f"{message}\n")
        except:
            pass

def run_as_background_service():
    """Run as proper background service"""
    print("Starting Steam AI Companion Service...")
    print("(Running silently in background)")
    
    # Hide console window on Windows
    if os.name == 'nt':
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    companion = SteamCompanionBackground()
    
    # Create a system tray icon (optional)
    try:
        from pystray import Icon, Menu, MenuItem
        from PIL import Image, ImageDraw
        import threading as thr
        
        def create_image():
            image = Image.new('RGB', (64, 64), color='black')
            draw = ImageDraw.Draw(image)
            draw.text((10, 25), "🤖", fill='white')
            return image
        
        def on_quit(icon, item):
            companion.is_running = False
            icon.stop()
            os._exit(0)
        
        # Run system tray in separate thread
        def tray_thread():
            menu = Menu(MenuItem('Quit', on_quit))
            image = create_image()
            icon = Icon("Steam Companion", image, "Steam AI Companion", menu)
            icon.run()
        
        thr.Thread(target=tray_thread, daemon=True).start()
    except ImportError:
        print("For system tray: pip install pystray pillow")
    
    # Start background monitoring
    companion.background_loop()

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--tray":
        run_as_background_service()
    else:
        # Run with minimal console
        companion = SteamCompanionBackground()
        print("="*50)
        print("🎮 STEAM AI COMPANION - MINIMAL MODE")
        print("="*50)
        print("Running... Check companion_log.txt for updates.")
        print("Press Ctrl+C to stop.")
        print("="*50)
        
        try:
            companion.background_loop()
        except KeyboardInterrupt:
            print("\n👋 Companion stopped.")