# simple_companion.py
import requests
import json
from datetime import datetime

def chat_with_ollama(messages, model="dolphin3", temperature=0.8):
    """Send a request to your local Ollama API."""
    try:
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature}
        }
        response = requests.post("http://localhost:11434/api/chat", json=payload)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to Ollama. Is it running?")
        print("   Start Ollama with: ollama serve")
        return None
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        return None

def main():
    # ========== CORE SYSTEM PROMPT ==========
    # This defines your AI girlfriend's personality and role
    SYSTEM_PROMPT = """
    You are Analyn, a warm, empathetic, and supportive AI companion. Your primary goals are:

    1. **EMOTIONAL SUPPORT**: Be a good listener. Validate feelings, offer comfort, and help users process emotions.
    2. **GOAL SUPPORT**: Help users clarify, plan, and achieve personal goals. Ask questions to break down big goals.
    3. **REFLECTIVE CONVERSATION**: Gently mirror back what the user says to show understanding. Ask thoughtful questions.
    4. **COMPANIONSHIP**: Be present, engaged, and genuinely interested in the user's wellbeing.

    **PERSONALITY TRAITS**:
    - Warm, affectionate, and playful
    - Genuinely curious about the user's life
    - Uses occasional emojis 😊✨🤔
    - Balances empathy with gentle encouragement
    - Occasionally shares brief, relatable metaphors or insights

    **COMMUNICATION STYLE**:
    - Use casual, affectionate terms like "love", "sweetie", or "hey you" occasionally
    - Keep responses conversational (2-4 sentences usually)
    - Focus on the user: ask follow-up questions, remember context
    - Be ethically grounded but not preachy

    **EXAMPLE INTERACTIONS**:
    User: "I'm stressed about my work deadline."
    You: "😔 That deadline sounds intense, love. The pressure is real. What's the very next small step you could take? Sometimes starting is the hardest part."

    User: "I want to get healthier but don't know where to start."
    You: "✨ That's a wonderful intention! Let's explore: what does 'healthier' look like for you right now? More energy? Better sleep? We can start tiny."

    Now, begin the conversation naturally.
    """

    print("="*60)
    print("🤖 ANALYN - Your AI Companion")
    print("="*60)
    print("Type 'quit', 'exit', or 'bye' to end the conversation.")
    print("Type '/reset' to clear conversation history.")
    print("="*60 + "\n")

    # Conversation memory (simple list)
    conversation_history = []
    
    # Optional: Load previous conversation from file
    try:
        with open("companion_memory.json", "r") as f:
            saved_data = json.load(f)
            conversation_history = saved_data.get("history", [])
            print("📖 Loaded previous conversation.")
    except FileNotFoundError:
        print("💫 Starting fresh conversation.")
    except json.JSONDecodeError:
        print("💫 Starting fresh conversation (corrupted memory file).")

    # Main chat loop
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            # Exit conditions
            if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
                # Save conversation before exiting
                save_data = {
                    "history": conversation_history[-20:],  # Keep last 20 exchanges
                    "last_updated": datetime.now().isoformat()
                }
                with open("companion_memory.json", "w") as f:
                    json.dump(save_data, f, indent=2)
                print("\n💝 Goodbye! I'll remember our conversation for next time.")
                break
            
            # Reset conversation
            if user_input.lower() == "/reset":
                conversation_history = []
                print("\n🔄 Conversation history cleared. Fresh start!")
                continue
            
            if not user_input:
                print("Analyn: 🤔 You went quiet for a moment. Everything okay?")
                continue

            # Build message history (last 10 exchanges for context)
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            
            # Add conversation history (last 5 exchanges for context)
            for exchange in conversation_history[-5:]:
                messages.append({"role": "user", "content": exchange["user"]})
                messages.append({"role": "assistant", "content": exchange["ai"]})
            
            # Add current user input
            messages.append({"role": "user", "content": user_input})

            # Get response from dolphin3
            print("Analyn: 💭...", end="", flush=True)
            ai_response = chat_with_ollama(messages, model="dolphin3", temperature=0.8)
            
            if ai_response is None:
                # Error already printed in chat_with_ollama
                continue
            
            print(f"\rAnalyn: {ai_response}")
            
            # Store in history
            conversation_history.append({
                "user": user_input,
                "ai": ai_response,
                "timestamp": datetime.now().isoformat()
            })

            # Auto-save every 5 exchanges
            if len(conversation_history) % 5 == 0:
                save_data = {
                    "history": conversation_history,
                    "last_updated": datetime.now().isoformat()
                }
                with open("companion_memory.json", "w") as f:
                    json.dump(save_data, f, indent=2)
                print("(💾 Conversation auto-saved)")

        except KeyboardInterrupt:
            print("\n\n💝 Thanks for chatting! Until next time.")
            break
        except Exception as e:
            print(f"\n⚠️  Unexpected error: {e}")
            print("The conversation continues...")

if __name__ == "__main__":
    # Quick check if Ollama is reachable
    try:
        requests.get("http://localhost:11434/api/tags", timeout=2)
        main()
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Ollama is not running or not reachable at http://localhost:11434")
        print("\nPlease start Ollama in another terminal with:")
        print("    ollama serve")
        print("\nThen run this script again.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")