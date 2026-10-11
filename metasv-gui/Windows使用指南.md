# MetaSV GUI - Windows 使用指南

## 🪟 Windows 完整安装步骤

### 1. 安装前置软件

#### Python 3.10+
1. 访问 https://www.python.org/downloads/
2. 下载最新的 Python 3.x 版本
3. 安装时**勾选"Add Python to PATH"**
4. 验证安装：
   ```powershell
   python --version
   ```

#### Rust 工具链
1. 访问 https://rustup.rs/
2. 下载并运行 `rustup-init.exe`
3. 选择默认安装选项
4. 验证安装：
   ```powershell
   cargo --version
   rustc --version
   ```

#### CMake (编译 MetaSV 需要)
1. 访问 https://cmake.org/download/
2. 下载 Windows 安装包
3. 安装时选择"Add CMake to PATH"
4. 验证安装：
   ```powershell
   cmake --version
   ```

#### Git (可选，用于克隆项目)
1. 访问 https://git-scm.com/download/win
2. 下载并安装
3. 使用默认选项

### 2. 获取 MetaSV

#### 方式一：从 macOS 复制
将整个 `MetaSV-main` 文件夹复制到 Windows 电脑，例如：
```
C:\Users\你的用户名\Documents\MetaSV-main\
```

#### 方式二：从 GitHub 克隆
```powershell
git clone https://github.com/[项目地址]/MetaSV.git
cd MetaSV
```

### 3. 编译 MetaSV

```powershell
# 打开 PowerShell，进入项目目录
cd C:\Users\你的用户名\Documents\MetaSV-main

# 编译 Release 版本
cargo build --release

# 等待编译完成（首次编译可能需要 10-20 分钟）
```

编译完成后，可执行文件位于：
```
C:\Users\你的用户名\Documents\MetaSV-main\target\release\metasv.exe
```

### 4. 设置 Python 训练环境

```powershell
# 安装 uv 包管理器
pip install uv

# 设置环境变量并同步训练依赖
$env:UV_LINK_MODE="copy"
uv sync --project training --locked
```

### 5. 启动图形界面

#### 🌐 Web GUI（推荐）

**双击启动：**
1. 进入 `metasv-gui` 目录
2. 双击 `start_web.bat`
3. 等待浏览器自动打开，或手动访问 http://localhost:5001

**命令行启动：**
```powershell
cd metasv-gui
.\start_web.bat
```

#### 🖥️ 桌面 GUI

**双击启动：**
1. 进入 `metasv-gui` 目录
2. 双击 `run.bat`
3. 等待桌面应用程序打开

**命令行启动：**
```powershell
cd metasv-gui
.\run.bat
```

## 📁 Windows 路径格式

在 GUI 中输入路径时使用以下格式：

### 绝对路径（推荐）
```
C:\Users\用户名\Documents\voices\voice.nofs
C:\Users\用户名\Music\project.svp
D:\VOCALOID\clf-data
```

### 相对路径
```
.\voices\voice.nofs
..\data\project.svp
```

**提示：** 可以直接在文件资源管理器中复制路径，然后粘贴到 GUI 中。

## 🔧 Windows 特定配置

### 修改 web_gui.py 的路径查找

由于 Windows 使用 `metasv.exe`，需要确保路径正确：

```python
def find_metasv():
    """查找 MetaSV 可执行文件"""
    # Windows 路径
    default_path = Path(__file__).parent.parent / "target" / "release" / "metasv.exe"
    if default_path.exists():
        return str(default_path)
    
    # macOS/Linux 路径
    default_path = Path(__file__).parent.parent / "target" / "release" / "metasv"
    if default_path.exists():
        return str(default_path)
    
    return None
```

### PowerShell 执行策略

如果遇到"无法加载脚本"错误：

```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 💡 Windows 使用技巧

### 1. 路径自动补全
在 PowerShell 中输入路径时按 `Tab` 键自动补全

### 2. 复制路径
在文件资源管理器中：
- 按住 `Shift` + 右键点击文件
- 选择"复制为路径"
- 粘贴到 GUI 中（记得去掉引号）

### 3. 创建桌面快捷方式
右键拖动 `start_web.bat` 到桌面，选择"创建快捷方式"

### 4. 任务栏固定
运行 Web GUI 后，在任务栏的浏览器图标上右键，选择"固定到任务栏"

## 🐛 Windows 常见问题

### 问题：找不到 Python
**错误：** `'python' 不是内部或外部命令`

**解决方案：**
1. 重新安装 Python，勾选"Add to PATH"
2. 或手动添加到环境变量：
   - 右键"此电脑" → 属性 → 高级系统设置
   - 环境变量 → Path → 新建
   - 添加：`C:\Users\你的用户名\AppData\Local\Programs\Python\Python3xx`

### 问题：Rust 编译失败
**错误：** `error: linker 'link.exe' not found`

**解决方案：**
安装 Visual Studio Build Tools：
1. 访问 https://visualstudio.microsoft.com/downloads/
2. 下载"Visual Studio 2022 生成工具"
3. 安装时选择"使用 C++ 的桌面开发"

### 问题：端口被占用
**错误：** `Address already in use`

**解决方案：**
```powershell
# 查找占用端口的程序
netstat -ano | findstr :5001

# 结束进程（替换 PID 为实际进程 ID）
taskkill /F /PID <PID>

# 或修改 web_gui.py 使用其他端口
```

### 问题：PyQt6 安装失败
**错误：** `Could not find a version that satisfies the requirement PyQt6`

**解决方案：**
```powershell
# 更新 pip
python -m pip install --upgrade pip

# 重新安装
pip install PyQt6
```

### 问题：训练环境错误
**错误：** UV 同步失败

**解决方案：**
```powershell
# 设置环境变量
$env:UV_LINK_MODE="copy"

# 清理并重新同步
cd MetaSV-main
uv sync --project training --locked --reinstall
```

## 📊 性能对比

| 特性 | Windows | macOS | Linux |
|------|---------|-------|-------|
| 编译速度 | ⚡⚡ | ⚡⚡⚡ | ⚡⚡⚡ |
| 运行速度 | ⚡⚡⚡ | ⚡⚡⚡ | ⚡⚡⚡ |
| GUI 体验 | ✅ 完全支持 | ✅ 完全支持 | ✅ 完全支持 |
| 训练速度 | 🖥️ 取决于硬件 | 🖥️ 取决于硬件 | 🖥️ 取决于硬件 |

## 🎯 推荐配置

### 最低配置
- CPU: Intel i5 / AMD Ryzen 5
- RAM: 8GB
- 存储: 10GB 可用空间
- Python: 3.10+

### 推荐配置
- CPU: Intel i7 / AMD Ryzen 7
- RAM: 16GB
- GPU: NVIDIA GTX 1660+ (用于训练加速)
- 存储: 20GB+ SSD
- Python: 3.11+

### 训练加速配置
- GPU: NVIDIA RTX 3060+ (12GB+ VRAM)
- RAM: 32GB
- 存储: NVMe SSD

## 🚀 GPU 加速（可选）

如果你有 NVIDIA 显卡并想加速训练：

```powershell
# 安装 CUDA 版本的 PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

然后训练时会自动使用 GPU。

## 📚 其他资源

- **MetaSV 文档**: `README.md`
- **训练说明**: `training/README.md`
- **快速开始**: `快速开始.md`
- **Web GUI 文档**: `metasv-gui/README.md`

## ✅ 检查清单

安装完成后检查：

- [ ] Python 已安装并添加到 PATH
- [ ] Rust 已安装（`cargo --version` 有输出）
- [ ] MetaSV 已编译（`target/release/metasv.exe` 存在）
- [ ] Python 训练环境已设置
- [ ] GUI 可以启动（Web 或桌面版）
- [ ] 浏览器可以访问 http://localhost:5001

全部完成后，你就可以在 Windows 上使用 MetaSV GUI 了！

## 💬 需要帮助？

如果遇到问题：
1. 检查本文档的"常见问题"部分
2. 确保所有前置软件正确安装
3. 查看错误信息并搜索解决方案

---

**Windows 版本完全支持！** 🎉

所有功能在 Windows 上与 macOS/Linux 完全一致。
