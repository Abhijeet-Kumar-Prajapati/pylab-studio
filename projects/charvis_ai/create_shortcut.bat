@echo off
set shortcutPath=%USERPROFILE%\Desktop\Charvis.lnk
set targetPath=%USERPROFILE%\Music\abhijeet\charvis_ai.py

if exist "%shortcutPath%" (
    del "%shortcutPath%"
)

powershell "$s=(New-Object -COMObject WScript.Shell).CreateShortcut('%shortcutPath%');$s.TargetPath='%targetPath%';$s.Save()"
