# MetaSV GUI

[简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [日本語](README.ja.md)

---

## 🎵 歌聲合成模型訓練工具（附圖形介面）

歌聲模型命令列工具 + 圖形介面。Rust 負責採集和渲染，Python／PyTorch 負責訓練，GUI 提供視覺化操作介面。

## ✨ 新特性

- 🌐 **Web GUI** - 基於 Flask 的現代化 Web 介面
- 🖥️ **桌面 GUI** - 基於 PyQt6 的原生桌面應用程式
- 🎨 4 大功能模組：資料集採集、模型訓練、聲庫匯出、歌聲渲染
- 📱 完全跨平台：Windows、macOS、Linux
- 🌍 多語言支援：簡體中文、繁體中文、英語、日語

## 🚀 快速啟動

### 啟動圖形介面

```bash
cd metasv-gui
./start_web.sh          # macOS/Linux
# 或
.\start_web.bat         # Windows
```

然後在瀏覽器開啟：**http://localhost:5001**

### 命令列使用

```bash
# 編譯
cargo build --release

# 設定訓練環境
uv sync --project training --locked

# 使用
metasv --help
```

## 📖 文件

- [快速開始指南](metasv-gui/docs/zh-TW/快速開始.md)
- [Windows 使用指南](metasv-gui/docs/zh-TW/Windows使用指南.md)
- [完整 README](metasv-gui/docs/zh-TW/README.md)

## 🎨 GUI 功能

### 1. 📦 資料集採集
配置聲庫和專案，採集訓練資料

### 2. 🎓 模型訓練
設定訓練參數，即時監控訓練進度

### 3. 📤 聲庫匯出
一鍵匯出訓練完成的聲庫檔案

### 4. 🎤 歌聲渲染
使用聲庫將 SVP 專案渲染為 WAV 音訊

## 🖥️ 平台支援

| 平台 | 命令列 | Web GUI | 桌面 GUI |
|------|-------|---------|---------|
| **Windows** | ✅ | ✅ | ✅ |
| **macOS** | ✅ | ✅ | ✅ |
| **Linux** | ✅ | ✅ | ✅ |

## 📋 系統需求

### 核心功能
- Python 3.13+
- Rust (cargo)
- PyTorch

### GUI 額外依賴
- **Web GUI**: Flask 3.0+
- **桌面 GUI**: PyQt6 6.6+（可選）

## 🌍 語言支援

GUI 介面支援切換語言：
- 🇨🇳 簡體中文
- 🇹🇼 繁體中文
- 🇬🇧 English
- 🇯🇵 日本語

## 📂 專案結構

```
MetaSV-GUI/
├── src/                    # Rust CLI、模型讀取與推理
├── training/               # Python 訓練套件
├── metasv-gui/            # 圖形介面（Web + 桌面版）
│   ├── web_gui.py         # Flask Web 伺服器
│   ├── metasv_gui.py      # PyQt6 桌面應用程式
│   ├── templates/         # Web 前端介面
│   ├── locales/           # 🆕 翻譯檔案
│   └── docs/              # 文件
└── target/release/        # 編譯產物
```

## 🤝 貢獻

歡迎貢獻！請隨時提交 Pull Request。

## 📄 授權

[GPL-3.0](LICENSE)

## 🙏 致謝

感謝 [OpenSV](https://github.com/cubeww/OpenSV) 專案的啟發和參考。

## 📮 聯絡方式

- Issues: [GitHub Issues](https://github.com/Quadimension-CL/MetaSV-GUI/issues)
- Discussions: [GitHub Discussions](https://github.com/Quadimension-CL/MetaSV-GUI/discussions)

---

**立即開始使用 MetaSV GUI！** 🎵

無論你是新手還是進階使用者，現在都可以透過直覺的圖形介面輕鬆訓練和使用歌聲合成模型。
