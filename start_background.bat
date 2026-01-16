@echo off
echo Starting Background AI Companion...
echo Ollama will run minimized...
start /min ollama serve
timeout /t 5 /nobreak
python background_companion.py
pause