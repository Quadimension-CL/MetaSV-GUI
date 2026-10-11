#!/usr/bin/env python3
"""
快速启动 MetaSV GUI
双击此文件即可运行
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # 获取脚本所在目录
    script_dir = Path(__file__).parent

    # 切换到脚本目录
    os.chdir(script_dir)

    # 检查虚拟环境
    venv_dir = script_dir / "venv"
    python_exe = venv_dir / "bin" / "python3"

    if not venv_dir.exists():
        print("首次运行，正在设置环境...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        subprocess.run([str(python_exe), "-m", "pip", "install", "-q", "-r", "requirements.txt"])

    # 启动 GUI
    subprocess.run([str(python_exe), "metasv_gui.py"])

if __name__ == "__main__":
    main()
