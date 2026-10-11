#!/usr/bin/env python3
"""
MetaSV Web GUI with Multi-language Support
Supports: Simplified Chinese, Traditional Chinese, English, Japanese
"""

from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import os
import json
from pathlib import Path
import threading

app = Flask(__name__)

# 全局变量存储当前运行的进程
current_process = None
current_log = []

def find_metasv():
    """查找 MetaSV 可执行文件"""
    # Windows 路径
    default_path_win = Path(__file__).parent.parent / "target" / "release" / "metasv.exe"
    if default_path_win.exists():
        return str(default_path_win)

    # macOS/Linux 路径
    default_path_unix = Path(__file__).parent.parent / "target" / "release" / "metasv"
    if default_path_unix.exists():
        return str(default_path_unix)

    return None

METASV_PATH = find_metasv()

# 加载翻译文件
def load_translations():
    """加载所有语言的翻译文件"""
    translations = {}
    locales_dir = Path(__file__).parent / "locales"

    if locales_dir.exists():
        for locale_file in locales_dir.glob("*.json"):
            lang = locale_file.stem
            with open(locale_file, 'r', encoding='utf-8') as f:
                translations[lang] = json.load(f)

    return translations

TRANSLATIONS = load_translations()

def run_command(command, env=None):
    """在后台运行命令"""
    global current_process, current_log
    current_log = []

    try:
        current_process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True,
            env=env or os.environ.copy()
        )

        for line in iter(current_process.stdout.readline, ''):
            if line:
                current_log.append(line.rstrip())

        current_process.wait()
        return current_process.returncode
    except Exception as e:
        current_log.append(f"错误 / Error: {str(e)}")
        return 1

@app.route('/')
def index():
    """主页"""
    lang = request.args.get('lang', 'zh-CN')
    return render_template('index_i18n.html',
                         metasv_path=METASV_PATH,
                         lang=lang,
                         translations=TRANSLATIONS)

@app.route('/api/translations')
def get_translations():
    """获取所有翻译"""
    return jsonify(TRANSLATIONS)

@app.route('/api/capture', methods=['POST'])
def capture():
    """数据集采集"""
    data = request.json

    env = os.environ.copy()
    env['UV_LINK_MODE'] = 'copy'

    command = (
        f'cd "{Path(METASV_PATH).parent.parent}" && '
        f'uv run --project training --locked "{METASV_PATH}" dataset capture '
        f'--voice "{data["base_voice"]}" '
        f'--teacher "{data["teacher_voice"]}" '
        f'--train-project "{data["train_project"]}" '
        f'--validation-project "{data["validation_project"]}" '
        f'--output "{data["output"]}" '
        f'--language {data["language"]} '
        f'--dictionary "{data["dictionary"]}"'
    )

    thread = threading.Thread(target=run_command, args=(command, env))
    thread.start()

    return jsonify({"status": "started", "command": command})

@app.route('/api/train', methods=['POST'])
def train():
    """模型训练"""
    data = request.json

    env = os.environ.copy()
    env['UV_LINK_MODE'] = 'copy'

    command = (
        f'cd "{Path(METASV_PATH).parent.parent}" && '
        f'uv run --project training --locked "{METASV_PATH}" train '
        f'--model "{data["model"]}" '
        f'--dataset "{data["dataset"]}" '
        f'--output "{data["output"]}" '
        f'--steps {data["steps"]}'
    )

    if data.get("seconds", 0) > 0:
        command += f' --seconds {data["seconds"]}'

    thread = threading.Thread(target=run_command, args=(command, env))
    thread.start()

    return jsonify({"status": "started", "command": command})

@app.route('/api/export', methods=['POST'])
def export():
    """声库导出"""
    data = request.json

    command = (
        f'"{METASV_PATH}" voice-export '
        f'--voice "{data["voice"]}" '
        f'--model "{data["model"]}" '
        f'--output "{data["output"]}"'
    )

    thread = threading.Thread(target=run_command, args=(command,))
    thread.start()

    return jsonify({"status": "started", "command": command})

@app.route('/api/render', methods=['POST'])
def render():
    """歌声渲染"""
    data = request.json

    command = (
        f'"{METASV_PATH}" render '
        f'--voice "{data["voice"]}" '
        f'--project "{data["project"]}" '
        f'--output "{data["output"]}" '
        f'--language {data["language"]} '
        f'--dictionary "{data["dictionary"]}" '
        f'--pitch-mode {data["pitch_mode"]}'
    )

    thread = threading.Thread(target=run_command, args=(command,))
    thread.start()

    return jsonify({"status": "started", "command": command})

@app.route('/api/logs')
def get_logs():
    """获取实时日志"""
    global current_log
    return jsonify({"logs": current_log})

@app.route('/api/stop', methods=['POST'])
def stop():
    """停止当前进程"""
    global current_process
    if current_process:
        current_process.terminate()
        return jsonify({"status": "stopped"})
    return jsonify({"status": "no_process"})

if __name__ == '__main__':
    port = 5001
    print("=" * 50)
    print("MetaSV Web GUI (Multi-language)")
    print("=" * 50)
    print(f"MetaSV Path: {METASV_PATH}")
    print(f"\nOpen in browser: http://localhost:{port}")
    print("Languages: 简体中文 | 繁體中文 | English | 日本語")
    print("\nPress Ctrl+C to stop")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=port)
