$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\Jarvis.lnk")
$Shortcut.TargetPath = "pythonw.exe"
$Shortcut.Arguments = """$PSScriptRoot\start_jarvis.pyw"""
$Shortcut.WorkingDirectory = "$PSScriptRoot"
$Shortcut.WindowStyle = 7  # Minimized
$Shortcut.Description = "Start Jarvis AI Assistant"
$Shortcut.Save()
