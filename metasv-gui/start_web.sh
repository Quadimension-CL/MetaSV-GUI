#!/bin/bash
# MetaSV Web GUI 一键启动脚本

echo "🎵 MetaSV Web GUI 启动中..."

cd "$(dirname "$0")"

# 激活虚拟环境
source venv/bin/activate

# 启动服务器
python3 web_gui.py
