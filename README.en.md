# MetaSV GUI

[简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [English](README.md) | [日本語](README.ja.md)

---

## 🎵 Singing Synthesis Model Training Tool with GUI

A command-line tool and graphical interface for singing voice synthesis. Rust handles capture and rendering, Python/PyTorch handles training, and GUI provides visual operation interface.

## ✨ Features

- 🌐 **Web GUI** - Modern web interface based on Flask
- 🖥️ **Desktop GUI** - Native desktop application based on PyQt6
- 🎨 4 Core Modules: Dataset Capture, Model Training, Voice Export, Singing Rendering
- 📱 Fully Cross-platform: Windows, macOS, Linux
- 🌍 Multi-language Support: Simplified Chinese, Traditional Chinese, English, Japanese

## 🚀 Quick Start

### Launch GUI

```bash
cd metasv-gui
./start_web.sh          # macOS/Linux
# or
.\start_web.bat         # Windows
```

Then open in browser: **http://localhost:5001**

### Command Line

```bash
# Build
cargo build --release

# Setup training environment
uv sync --project training --locked

# Usage
metasv --help
```

## 📖 Documentation

- [Quick Start Guide](metasv-gui/docs/en/QUICKSTART.md)
- [Windows User Guide](metasv-gui/docs/en/WINDOWS.md)
- [Complete README](metasv-gui/docs/en/README.md)

## 🎨 GUI Features

### 1. 📦 Dataset Capture
Configure voice banks and projects to capture training data

### 2. 🎓 Model Training
Set training parameters and monitor training progress in real-time

### 3. 📤 Voice Export
One-click export of trained voice bank files

### 4. 🎤 Singing Rendering
Render SVP projects to WAV audio using voice banks

## 🖥️ Platform Support

| Platform | CLI | Web GUI | Desktop GUI |
|----------|-----|---------|-------------|
| **Windows** | ✅ | ✅ | ✅ |
| **macOS** | ✅ | ✅ | ✅ |
| **Linux** | ✅ | ✅ | ✅ |

## 📋 Requirements

### Core
- Python 3.13+
- Rust (cargo)
- PyTorch

### GUI
- **Web GUI**: Flask 3.0+
- **Desktop GUI**: PyQt6 6.6+ (optional)

## 🌍 Language Support

The GUI interface supports switching between:
- 🇨🇳 Simplified Chinese (简体中文)
- 🇹🇼 Traditional Chinese (繁體中文)
- 🇬🇧 English
- 🇯🇵 Japanese (日本語)

## 📂 Project Structure

```
MetaSV-GUI/
├── src/                    # Rust CLI, model reading and inference
├── training/               # Python training package
├── metasv-gui/            # GUI (Web + Desktop)
│   ├── web_gui.py         # Flask web server
│   ├── metasv_gui.py      # PyQt6 desktop app
│   ├── templates/         # Web frontend
│   ├── locales/           # 🆕 Translation files
│   └── docs/              # Documentation
└── target/release/        # Build output
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

[GPL-3.0](LICENSE)

## 🙏 Acknowledgments

Thanks to [OpenSV](https://github.com/cubeww/OpenSV) for inspiration and reference.

## 📮 Contact

- Issues: [GitHub Issues](https://github.com/Quadimension-CL/MetaSV-GUI/issues)
- Discussions: [GitHub Discussions](https://github.com/Quadimension-CL/MetaSV-GUI/discussions)

---

**Start using MetaSV GUI now!** 🎵

Whether you're a beginner or an advanced user, you can now easily train and use singing synthesis models through an intuitive graphical interface.
