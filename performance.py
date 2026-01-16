# performance_monitor.py
import psutil
import time

def check_gaming_performance():
    """Monitor if companion affects game performance"""
    game_cpu = 0
    companion_cpu = 0
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            name = proc.info['name'].lower()
            if 'steam' in name or '.exe' in name and 'game' in name:
                game_cpu += proc.info['cpu_percent'] or 0
            elif 'python' in name and 'companion' in ' '.join(proc.cmdline()):
                companion_cpu = proc.info['cpu_percent'] or 0
        except:
            continue
    
    return {
        "game_cpu": game_cpu,
        "companion_cpu": companion_cpu,
        "acceptable": companion_cpu < 5.0  # Companion should use <5% CPU
    }