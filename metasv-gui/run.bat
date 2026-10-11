@echo off
REM MetaSV PyQt6 桌面 GUI - Windows 启动脚本

echo ========================================
echo MetaSV 桌面 GUI 启动中...
echo ========================================

cd /d "%~dp0"

REM 检查虚拟环境
if not exist "venv\Scripts\python.exe" (
    echo 首次运行，创建虚拟环境...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -q PyQt6
) else (
    call venv\Scripts\activate.bat
)

REM 启动桌面 GUI
echo.
echo 启动桌面应用程序...
python metasv_gui.py

pause
