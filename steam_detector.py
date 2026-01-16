# steam_detector.py
import winreg  # Windows only
import psutil

def get_steam_games():
    """Get installed Steam games from registry"""
    games = {}
    try:
        # Windows registry path for Steam
        reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey_name) as subkey:
                        try:
                            name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            install = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                            if "steam" in install.lower():
                                games[name] = install
                        except:
                            continue
                except:
                    continue
    except:
        pass
    return games