@echo off
echo ==========================================
echo  VS Code Setup for arifOS
echo ==========================================
echo.
echo Installing recommended extensions...
echo.

call code --install-extension ms-python.python
call code --install-extension ms-python.vscode-pylance
call code --install-extension ms-python.black-formatter
call code --install-extension charliermarsh.ruff
call code --install-extension ms-toolsai.jupyter
call code --install-extension github.vscode-pull-request-github
call code --install-extension ms-vscode.powershell
echo.
echo ==========================================
echo  All extensions installed!
echo  Now opening arifOS in VS Code...
echo ==========================================
timeout /t 2 >nul
code .
