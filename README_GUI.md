# MetaSV with GUI

歌声模型命令行工具 + 图形界面。Rust 负责采集和渲染，Python／PyTorch 负责训练，GUI 提供可视化操作界面。

## ✨ 新特性：图形界面

**现在包含完整的图形界面！**

- 🌐 **Web GUI** - 基于 Flask 的现代化 Web 界面
- 🖥️ **桌面 GUI** - 基于 PyQt6 的原生桌面应用
- 🎨 4 大功能模块：数据集采集、模型训练、声库导出、歌声渲染
- 📱 完全跨平台：Windows、macOS、Linux

**快速启动 GUI：**

```bash
cd metasv-gui
./start_web.sh          # macOS/Linux
# 或
.\start_web.bat         # Windows
```

然后在浏览器打开：http://localhost:5001

📚 **GUI 完整文档：** [metasv-gui/README.md](metasv-gui/README.md)

---

## 📖 原项目说明

歌声模型命令行工具。Rust 负责采集和渲染，Python／PyTorch 负责训练。

## 安装

```bash
cargo build --release
uv sync --project training --locked
```

以下 `metasv` 指 `target/release/metasv`（Windows 下为 `metasv.exe`）。uv 在 `training/.venv` 管理 Python 环境，默认使用 Python 3.13 和 CPU 版 PyTorch，依赖版本记录于 `training/uv.lock`。

## 命令行使用

```bash
uv run --project training --locked metasv dataset capture --voice base-voice --teacher teacher-voice --train-project train.svp --validation-project validation.svp --output dataset --language mandarin --dictionary path/to/clf-data
uv run --project training --locked metasv train --model dataset/base_model.dnni --dataset dataset/dataset.json --output runs/demo --steps 100
metasv voice-export --voice base-voice --model runs/demo/trained-base.dnni --output trained.nofs
metasv render --voice trained.nofs --project song.svp --output song.wav --language mandarin --dictionary path/to/clf-data --pitch-mode notes
```

声库输入为已解码 NOFS 或模型目录，工程输入为 SVP。支持普通话、日语及显式音素，输出单声道 WAV。默认训练完整声学核心；采集、训练、导出和渲染均在 MetaSV 内完成。

当前使用音符音高，不支持自动 F0、参数曲线、引用组、加密声库及直接从 WAV 训练。[训练说明](training/README.md)，参数见 `metasv --help`。

## 🎨 图形界面使用

### Web GUI（推荐）

**启动：**
```bash
cd metasv-gui
./start_web.sh          # macOS/Linux
.\start_web.bat         # Windows
```

**访问：** http://localhost:5001

**特点：**
- ✅ 轻量级，安装快速
- ✅ 现代化界面设计
- ✅ 实时日志输出
- ✅ 可远程访问
- ✅ 完全跨平台

### 桌面 GUI

**启动：**
```bash
cd metasv-gui
./run.sh                # macOS/Linux
.\run.bat               # Windows
```

**特点：**
- ✅ 原生桌面体验
- ✅ 文件对话框
- ✅ 独立应用窗口

### GUI 功能

1. **📦 数据集采集** - 可视化配置声库和项目，采集训练数据
2. **🎓 模型训练** - 设置训练参数，实时监控训练进度
3. **📤 声库导出** - 一键导出训练完成的声库文件
4. **🎤 歌声渲染** - 使用声库渲染 SVP 项目为 WAV 音频

**详细文档：**
- [GUI 快速开始](metasv-gui/快速开始.md)
- [Windows 使用指南](metasv-gui/Windows使用指南.md)
- [完整 README](metasv-gui/README.md)

## 目录结构

```
MetaSV/
├── src/                # Rust CLI、模型读取与推理
├── training/           # Python 训练包与测试
├── metasv-gui/         # 🆕 图形界面（Web + 桌面版）
│   ├── web_gui.py      # Flask Web 服务器
│   ├── metasv_gui.py   # PyQt6 桌面应用
│   ├── templates/      # Web 前端界面
│   └── docs/           # GUI 文档
├── target/             # 编译产物
│   └── release/
│       └── metasv      # 可执行文件
└── local/, results/    # 本机实验（不进 Git）
```

## 系统要求

### 核心功能
- Python 3.13+
- Rust (cargo)
- PyTorch

### GUI 额外依赖
- **Web GUI**: Flask 3.0+
- **桌面 GUI**: PyQt6 6.6+（可选）

## 快速开始

### 方式一：使用图形界面（推荐新手）

```bash
# 1. 编译 MetaSV
cargo build --release

# 2. 设置训练环境
uv sync --project training --locked

# 3. 启动 GUI
cd metasv-gui
./start_web.sh          # 或 Windows 下用 start_web.bat

# 4. 在浏览器中操作
# http://localhost:5001
```

### 方式二：使用命令行（高级用户）

参考上面的"命令行使用"部分。

## 平台支持

| 平台 | 命令行 | Web GUI | 桌面 GUI |
|------|-------|---------|---------|
| **Windows** | ✅ | ✅ | ✅ |
| **macOS** | ✅ | ✅ | ✅ |
| **Linux** | ✅ | ✅ | ✅ |

## 参考项目

[OpenSV](https://github.com/cubeww/OpenSV)

## 许可证

[GPL-3.0](LICENSE)

## 贡献者

- 原作者：MetaSV 核心开发
- GUI 开发：图形界面增强

## 更新日志

### v0.2.0 (2026-10) - GUI 版本
- ✨ 新增 Web GUI（Flask + HTML/CSS/JavaScript）
- ✨ 新增桌面 GUI（PyQt6）
- ✨ 完整的 4 大功能模块可视化操作
- ✨ 实时日志输出
- ✨ 完全跨平台支持
- 📚 完善的中文文档

### v0.1.0 - 初始版本
- ✅ 命令行工具
- ✅ 数据集采集
- ✅ 模型训练
- ✅ 声库导出
- ✅ 歌声渲染

## 致谢

感谢 OpenSV 项目的启发和参考。

---

**立即开始使用 MetaSV GUI！** 🎵

无论你是新手还是高级用户，现在都可以通过直观的图形界面轻松训练和使用歌声合成模型。
