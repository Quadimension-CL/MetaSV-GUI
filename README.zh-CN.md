# MetaSV GUI

[简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [日本語](README.ja.md)

---

## 🎵 歌声合成模型训练工具（带图形界面）

歌声模型命令行工具 + 图形界面。Rust 负责采集和渲染，Python／PyTorch 负责训练，GUI 提供可视化操作界面。

## ✨ 新特性

- 🌐 **Web GUI** - 基于 Flask 的现代化 Web 界面
- 🖥️ **桌面 GUI** - 基于 PyQt6 的原生桌面应用
- 🎨 4 大功能模块：数据集采集、模型训练、声库导出、歌声渲染
- 📱 完全跨平台：Windows、macOS、Linux
- 🌍 多语言支持：简体中文、繁体中文、英语、日语

## 🚀 快速启动

### 启动图形界面

```bash
cd metasv-gui
./start_web.sh          # macOS/Linux
# 或
.\start_web.bat         # Windows
```

然后在浏览器打开：**http://localhost:5001**

### 命令行使用

```bash
# 编译
cargo build --release

# 设置训练环境
uv sync --project training --locked

# 使用
metasv --help
```

## 📖 文档

- [快速开始指南](metasv-gui/docs/zh-CN/快速开始.md)
- [Windows 使用指南](metasv-gui/docs/zh-CN/Windows使用指南.md)
- [完整 README](metasv-gui/docs/zh-CN/README.md)

## 🎨 GUI 功能

### 1. 📦 数据集采集
配置声库和项目，采集训练数据

### 2. 🎓 模型训练
设置训练参数，实时监控训练进度

### 3. 📤 声库导出
一键导出训练完成的声库文件

### 4. 🎤 歌声渲染
使用声库渲染 SVP 项目为 WAV 音频

## 🖥️ 平台支持

| 平台 | 命令行 | Web GUI | 桌面 GUI |
|------|-------|---------|---------|
| **Windows** | ✅ | ✅ | ✅ |
| **macOS** | ✅ | ✅ | ✅ |
| **Linux** | ✅ | ✅ | ✅ |

## 📋 系统要求

### 核心功能
- Python 3.13+
- Rust (cargo)
- PyTorch

### GUI 额外依赖
- **Web GUI**: Flask 3.0+
- **桌面 GUI**: PyQt6 6.6+（可选）

## 🌍 语言支持

GUI 界面支持切换语言：
- 🇨🇳 简体中文
- 🇹🇼 繁體中文
- 🇬🇧 English
- 🇯🇵 日本語

## 📂 项目结构

```
MetaSV-GUI/
├── src/                    # Rust CLI、模型读取与推理
├── training/               # Python 训练包
├── metasv-gui/            # 图形界面（Web + 桌面版）
│   ├── web_gui.py         # Flask Web 服务器
│   ├── metasv_gui.py      # PyQt6 桌面应用
│   ├── templates/         # Web 前端界面
│   ├── locales/           # 🆕 翻译文件
│   └── docs/              # 文档
└── target/release/        # 编译产物
```

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

## 📄 许可证

[GPL-3.0](LICENSE)

## 🙏 致谢

感谢 [OpenSV](https://github.com/cubeww/OpenSV) 项目的启发和参考。

## 📮 联系方式

- Issues: [GitHub Issues](https://github.com/Quadimension-CL/MetaSV-GUI/issues)
- Discussions: [GitHub Discussions](https://github.com/Quadimension-CL/MetaSV-GUI/discussions)

---

**立即开始使用 MetaSV GUI！** 🎵

无论你是新手还是高级用户，现在都可以通过直观的图形界面轻松训练和使用歌声合成模型。
