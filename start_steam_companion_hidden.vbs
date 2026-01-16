' start_steam_companion_hidden.vbs
' This runs Python script completely invisibly
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c python steam_companion_fixed.py", 0, False
Set WshShell = Nothing