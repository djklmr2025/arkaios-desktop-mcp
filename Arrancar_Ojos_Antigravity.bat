@echo off
echo ========================================================
echo Iniciando Los Ojos de Antigravity (Puente HTTP local)
echo ========================================================
echo Este servidor corre en el primer plano y permite que 
echo la IA tome capturas de pantalla y haga clics por ti.
echo Por favor, mantén esta ventana abierta.
echo ========================================================
cd /d "%~dp0"
call venv\Scripts\activate.bat
python eyes_server.py
pause
