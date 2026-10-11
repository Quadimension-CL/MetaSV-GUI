# MetaSV GUI

[简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [日本語](README.ja.md)

---

## 🎵 歌声合成モデルトレーニングツール（GUI付き）

歌声モデルのコマンドラインツール + グラフィカルインターフェース。Rustがキャプチャとレンダリングを担当し、Python／PyTorchがトレーニングを担当、GUIが視覚的な操作インターフェースを提供します。

## ✨ 新機能

- 🌐 **Web GUI** - Flaskベースのモダンなウェブインターフェース
- 🖥️ **デスクトップGUI** - PyQt6ベースのネイティブデスクトップアプリケーション
- 🎨 4つのコア機能：データセットキャプチャ、モデルトレーニング、ボイスバンクエクスポート、歌声レンダリング
- 📱 完全なクロスプラットフォーム対応：Windows、macOS、Linux
- 🌍 多言語サポート：簡体字中国語、繁体字中国語、英語、日本語

## 🚀 クイックスタート

### GUIの起動

```bash
cd metasv-gui
./start_web.sh          # macOS/Linux
# または
.\start_web.bat         # Windows
```

その後、ブラウザで開く：**http://localhost:5001**

### コマンドラインの使用

```bash
# ビルド
cargo build --release

# トレーニング環境のセットアップ
uv sync --project training --locked

# 使用方法
metasv --help
```

## 📖 ドキュメント

- [クイックスタートガイド](metasv-gui/docs/ja/クイックスタート.md)
- [Windows使用ガイド](metasv-gui/docs/ja/Windows使用ガイド.md)
- [完全なREADME](metasv-gui/docs/ja/README.md)

## 🎨 GUI機能

### 1. 📦 データセットキャプチャ
ボイスバンクとプロジェクトを設定し、トレーニングデータをキャプチャ

### 2. 🎓 モデルトレーニング
トレーニングパラメータを設定し、トレーニングの進行状況をリアルタイムで監視

### 3. 📤 ボイスバンクエクスポート
ワンクリックでトレーニング済みボイスバンクファイルをエクスポート

### 4. 🎤 歌声レンダリング
ボイスバンクを使用してSVPプロジェクトをWAVオーディオにレンダリング

## 🖥️ プラットフォームサポート

| プラットフォーム | CLI | Web GUI | デスクトップGUI |
|---------|-----|---------|-------------|
| **Windows** | ✅ | ✅ | ✅ |
| **macOS** | ✅ | ✅ | ✅ |
| **Linux** | ✅ | ✅ | ✅ |

## 📋 システム要件

### コア機能
- Python 3.13+
- Rust (cargo)
- PyTorch

### GUI追加依存関係
- **Web GUI**: Flask 3.0+
- **デスクトップGUI**: PyQt6 6.6+（オプション）

## 🌍 言語サポート

GUIインターフェースは言語切り替えに対応：
- 🇨🇳 簡体字中国語
- 🇹🇼 繁体字中国語
- 🇬🇧 English
- 🇯🇵 日本語

## 📂 プロジェクト構造

```
MetaSV-GUI/
├── src/                    # Rust CLI、モデルの読み込みと推論
├── training/               # Pythonトレーニングパッケージ
├── metasv-gui/            # グラフィカルインターフェース（Web + デスクトップ）
│   ├── web_gui.py         # Flask Webサーバー
│   ├── metasv_gui.py      # PyQt6デスクトップアプリ
│   ├── templates/         # Webフロントエンドインターフェース
│   ├── locales/           # 🆕 翻訳ファイル
│   └── docs/              # ドキュメント
└── target/release/        # ビルド出力
```

## 🤝 貢献

貢献を歓迎します！お気軽にPull Requestを送信してください。

## 📄 ライセンス

[GPL-3.0](LICENSE)

## 🙏 謝辞

[OpenSV](https://github.com/cubeww/OpenSV)プロジェクトからのインスピレーションと参考に感謝します。

## 📮 お問い合わせ

- Issues: [GitHub Issues](https://github.com/Quadimension-CL/MetaSV-GUI/issues)
- Discussions: [GitHub Discussions](https://github.com/Quadimension-CL/MetaSV-GUI/discussions)

---

**今すぐMetaSV GUIを使い始めましょう！** 🎵

初心者でも上級ユーザーでも、直感的なグラフィカルインターフェースを通じて、歌声合成モデルを簡単にトレーニングして使用できるようになりました。
