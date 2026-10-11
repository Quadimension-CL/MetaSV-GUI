@echo off
REM MetaSV Web GUI - Windows 启动脚本

echo ========================================
echo MetaSV Web GUI 启动中...
echo ========================================

cd /d "%~dp0"

REM 检查虚拟环境
if not exist "venv\Scripts\python.exe" (
    echo 首次运行，创建虚拟环境...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -q Flask
) else (
    call venv\Scripts\activate.bat
)

REM 启动 Web GUI
echo.
echo 启动 Web 服务器...
echo 请在浏览器中打开: http://localhost:5001
echo.
python web_gui.py

pause
