Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "C:\scripts\rollback_unpack.bat """ & WScript.Arguments(0) & """", 0, False