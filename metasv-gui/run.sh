#!/bin/bash
# MetaSV GUI 启动脚本

# 切换到脚本所在目录
cd "$(dirname "$0")"

# 检查并安装依赖
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -q -r requirements.txt

# 启动 GUI
echo "启动 MetaSV GUI..."
python3 metasv_gui.py
