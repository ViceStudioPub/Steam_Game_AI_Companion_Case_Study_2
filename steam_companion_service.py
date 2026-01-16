# Runs as Windows Service - completely invisible
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket

class SteamCompanionService(win32serviceutil.ServiceFramework):
    _svc_name_ = "SteamAICompanion"
    _svc_display_name_ = "Steam AI Companion"
    _svc_description_ = "AI companion for Steam gaming sessions"
    
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.is_running = True
        
    def SvcStop(self):
        self.is_running = False
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        
    def SvcDoRun(self):
        # Your companion code here - runs completely hidden
        while self.is_running:
            time.sleep(60)  # Do work here