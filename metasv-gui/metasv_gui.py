#!/usr/bin/env python3
"""
MetaSV GUI - 图形界面应用
支持数据集采集、模型训练、声库导出和歌声渲染
"""

import sys
import os
import subprocess
import json
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog,
    QSpinBox, QComboBox, QProgressBar, QGroupBox, QFormLayout, QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont


class CommandRunner(QThread):
    """后台运行命令的线程"""
    output = pyqtSignal(str)
    finished = pyqtSignal(int)
    progress = pyqtSignal(int)

    def __init__(self, command, env=None):
        super().__init__()
        self.command = command
        self.env = env or os.environ.copy()
        self.process = None

    def run(self):
        try:
            self.process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env=self.env,
                shell=True
            )

            for line in iter(self.process.stdout.readline, ''):
                if line:
                    self.output.emit(line.rstrip())

            self.process.wait()
            self.finished.emit(self.process.returncode)

        except Exception as e:
            self.output.emit(f"错误: {str(e)}")
            self.finished.emit(1)

    def stop(self):
        if self.process:
            self.process.terminate()


class DatasetTab(QWidget):
    """数据集采集标签页"""

    def __init__(self, metasv_path, parent=None):
        super().__init__(parent)
        self.metasv_path = metasv_path
        self.runner = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 输入文件组
        input_group = QGroupBox("输入文件")
        input_layout = QFormLayout()

        self.base_voice_input = self.create_file_input("选择基础声库 (.nofs)")
        self.teacher_voice_input = self.create_file_input("选择教师声库 (.nofs)")
        self.train_project_input = self.create_file_input("选择训练项目 (.svp)")
        self.validation_project_input = self.create_file_input("选择验证项目 (.svp)")
        self.dictionary_input = self.create_dir_input("选择词典目录 (clf-data)")

        input_layout.addRow("基础声库:", self.base_voice_input)
        input_layout.addRow("教师声库:", self.teacher_voice_input)
        input_layout.addRow("训练项目:", self.train_project_input)
        input_layout.addRow("验证项目:", self.validation_project_input)
        input_layout.addRow("词典目录:", self.dictionary_input)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # 配置组
        config_group = QGroupBox("配置")
        config_layout = QFormLayout()

        self.language_combo = QComboBox()
        self.language_combo.addItems(["mandarin", "japanese"])

        self.output_input = self.create_dir_input("选择输出目录")

        config_layout.addRow("语言:", self.language_combo)
        config_layout.addRow("输出目录:", self.output_input)

        config_group.setLayout(config_layout)
        layout.addWidget(config_group)

        # 控制按钮
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始采集")
        self.start_btn.clicked.connect(self.start_capture)
        self.stop_btn = QPushButton("停止")
        self.stop_btn.clicked.connect(self.stop_capture)
        self.stop_btn.setEnabled(False)

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)

        # 输出日志
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Courier", 10))
        layout.addWidget(QLabel("输出日志:"))
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def create_file_input(self, button_text):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        line_edit = QLineEdit()
        button = QPushButton(button_text)
        button.clicked.connect(lambda: self.browse_file(line_edit))

        layout.addWidget(line_edit)
        layout.addWidget(button)
        widget.setLayout(layout)
        widget.line_edit = line_edit
        return widget

    def create_dir_input(self, button_text):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        line_edit = QLineEdit()
        button = QPushButton(button_text)
        button.clicked.connect(lambda: self.browse_dir(line_edit))

        layout.addWidget(line_edit)
        layout.addWidget(button)
        widget.setLayout(layout)
        widget.line_edit = line_edit
        return widget

    def browse_file(self, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if file_path:
            line_edit.setText(file_path)

    def browse_dir(self, line_edit):
        dir_path = QFileDialog.getExistingDirectory(self, "选择目录")
        if dir_path:
            line_edit.setText(dir_path)

    def start_capture(self):
        # 验证输入
        base_voice = self.base_voice_input.line_edit.text()
        teacher_voice = self.teacher_voice_input.line_edit.text()
        train_project = self.train_project_input.line_edit.text()
        validation_project = self.validation_project_input.line_edit.text()
        dictionary = self.dictionary_input.line_edit.text()
        output = self.output_input.line_edit.text()
        language = self.language_combo.currentText()

        if not all([base_voice, teacher_voice, train_project, validation_project, dictionary, output]):
            QMessageBox.warning(self, "输入错误", "请填写所有必需字段")
            return

        # 构建命令
        env = os.environ.copy()
        env['UV_LINK_MODE'] = 'copy'

        command = (
            f'cd "{Path(self.metasv_path).parent}" && '
            f'uv run --project training --locked "{self.metasv_path}" dataset capture '
            f'--voice "{base_voice}" '
            f'--teacher "{teacher_voice}" '
            f'--train-project "{train_project}" '
            f'--validation-project "{validation_project}" '
            f'--output "{output}" '
            f'--language {language} '
            f'--dictionary "{dictionary}"'
        )

        self.log_output.clear()
        self.log_output.append(f"执行命令:\n{command}\n")

        self.runner = CommandRunner(command, env)
        self.runner.output.connect(self.log_output.append)
        self.runner.finished.connect(self.capture_finished)
        self.runner.start()

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop_capture(self):
        if self.runner:
            self.runner.stop()

    def capture_finished(self, code):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        if code == 0:
            self.log_output.append("\n✓ 采集完成！")
            QMessageBox.information(self, "完成", "数据集采集完成！")
        else:
            self.log_output.append(f"\n✗ 采集失败，退出码: {code}")


class TrainTab(QWidget):
    """模型训练标签页"""

    def __init__(self, metasv_path, parent=None):
        super().__init__(parent)
        self.metasv_path = metasv_path
        self.runner = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 输入文件组
        input_group = QGroupBox("输入文件")
        input_layout = QFormLayout()

        self.model_input = self.create_file_input("选择基础模型 (.dnni)")
        self.dataset_input = self.create_file_input("选择数据集 (dataset.json)")
        self.output_input = self.create_dir_input("选择输出目录")

        input_layout.addRow("基础模型:", self.model_input)
        input_layout.addRow("数据集:", self.dataset_input)
        input_layout.addRow("输出目录:", self.output_input)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # 训练参数组
        param_group = QGroupBox("训练参数")
        param_layout = QFormLayout()

        self.steps_spin = QSpinBox()
        self.steps_spin.setRange(10, 1000000)
        self.steps_spin.setValue(6000)
        self.steps_spin.setSingleStep(100)

        self.seconds_spin = QSpinBox()
        self.seconds_spin.setRange(0, 86400)
        self.seconds_spin.setValue(1800)
        self.seconds_spin.setSingleStep(300)
        self.seconds_spin.setSpecialValueText("无限制")

        param_layout.addRow("训练步数:", self.steps_spin)
        param_layout.addRow("时间限制(秒):", self.seconds_spin)

        param_group.setLayout(param_layout)
        layout.addWidget(param_group)

        # 控制按钮
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始训练")
        self.start_btn.clicked.connect(self.start_train)
        self.stop_btn = QPushButton("停止")
        self.stop_btn.clicked.connect(self.stop_train)
        self.stop_btn.setEnabled(False)

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)

        # 输出日志
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Courier", 10))
        layout.addWidget(QLabel("训练日志:"))
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def create_file_input(self, button_text):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        line_edit = QLineEdit()
        button = QPushButton(button_text)
        button.clicked.connect(lambda: self.browse_file(line_edit))

        layout.addWidget(line_edit)
        layout.addWidget(button)
        widget.setLayout(layout)
        widget.line_edit = line_edit
        return widget

    def create_dir_input(self, button_text):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        line_edit = QLineEdit()
        button = QPushButton(button_text)
        button.clicked.connect(lambda: self.browse_dir(line_edit))

        layout.addWidget(line_edit)
        layout.addWidget(button)
        widget.setLayout(layout)
        widget.line_edit = line_edit
        return widget

    def browse_file(self, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if file_path:
            line_edit.setText(file_path)

    def browse_dir(self, line_edit):
        dir_path = QFileDialog.getExistingDirectory(self, "选择目录")
        if dir_path:
            line_edit.setText(dir_path)

    def start_train(self):
        model = self.model_input.line_edit.text()
        dataset = self.dataset_input.line_edit.text()
        output = self.output_input.line_edit.text()
        steps = self.steps_spin.value()
        seconds = self.seconds_spin.value()

        if not all([model, dataset, output]):
            QMessageBox.warning(self, "输入错误", "请填写所有必需字段")
            return

        env = os.environ.copy()
        env['UV_LINK_MODE'] = 'copy'

        command = (
            f'cd "{Path(self.metasv_path).parent}" && '
            f'uv run --project training --locked "{self.metasv_path}" train '
            f'--model "{model}" '
            f'--dataset "{dataset}" '
            f'--output "{output}" '
            f'--steps {steps}'
        )

        if seconds > 0:
            command += f' --seconds {seconds}'

        self.log_output.clear()
        self.log_output.append(f"执行命令:\n{command}\n")

        self.runner = CommandRunner(command, env)
        self.runner.output.connect(self.log_output.append)
        self.runner.finished.connect(self.train_finished)
        self.runner.start()

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop_train(self):
        if self.runner:
            self.runner.stop()

    def train_finished(self, code):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        if code == 0:
            self.log_output.append("\n✓ 训练完成！")
            QMessageBox.information(self, "完成", "模型训练完成！")
        else:
            self.log_output.append(f"\n✗ 训练失败，退出码: {code}")


class ExportTab(QWidget):
    """声库导出标签页"""

    def __init__(self, metasv_path, parent=None):
        super().__init__(parent)
        self.metasv_path = metasv_path
        self.runner = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        input_group = QGroupBox("输入文件")
        input_layout = QFormLayout()

        self.voice_input = self.create_file_input("选择基础声库")
        self.model_input = self.create_file_input("选择训练模型 (.dnni)")
        self.output_input = self.create_save_input("保存声库文件 (.nofs)")

        input_layout.addRow("基础声库:", self.voice_input)
        input_layout.addRow("训练模型:", self.model_input)
        input_layout.addRow("输出文件:", self.output_input)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # 导出按钮
        self.export_btn = QPushButton("导出声库")
        self.export_btn.clicked.connect(self.export_voice)
        layout.addWidget(self.export_btn)

        # 输出日志
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Courier", 10))
        layout.addWidget(QLabel("输出日志:"))
        layout.addWidget(self.log_output)

        layout.addStretch()
        self.setLayout(layout)

    def create_file_input(self, button_text):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        line_edit = QLineEdit()
        button = QPushButton(button_text)
        button.clicked.connect(lambda: self.browse_file(line_edit))

        layout.addWidget(line_edit)
        layout.addWidget(button)
        widget.setLayout(layout)
        widget.line_edit = line_edit
        return widget

    def create_save_input(self, button_text):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        line_edit = QLineEdit()
        button = QPushButton(button_text)
        button.clicked.connect(lambda: self.save_file(line_edit))

        layout.addWidget(line_edit)
        layout.addWidget(button)
        widget.setLayout(layout)
        widget.line_edit = line_edit
        return widget

    def browse_file(self, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if file_path:
            line_edit.setText(file_path)

    def save_file(self, line_edit):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "NOFS Files (*.nofs)")
        if file_path:
            line_edit.setText(file_path)

    def export_voice(self):
        voice = self.voice_input.line_edit.text()
        model = self.model_input.line_edit.text()
        output = self.output_input.line_edit.text()

        if not all([voice, model, output]):
            QMessageBox.warning(self, "输入错误", "请填写所有必需字段")
            return

        command = (
            f'"{self.metasv_path}" voice-export '
            f'--voice "{voice}" '
            f'--model "{model}" '
            f'--output "{output}"'
        )

        self.log_output.clear()
        self.log_output.append(f"执行命令:\n{command}\n")

        self.runner = CommandRunner(command)
        self.runner.output.connect(self.log_output.append)
        self.runner.finished.connect(self.export_finished)
        self.runner.start()

        self.export_btn.setEnabled(False)

    def export_finished(self, code):
        self.export_btn.setEnabled(True)
        if code == 0:
            self.log_output.append("\n✓ 导出完成！")
            QMessageBox.information(self, "完成", "声库导出完成！")
        else:
            self.log_output.append(f"\n✗ 导出失败，退出码: {code}")


class RenderTab(QWidget):
    """歌声渲染标签页"""

    def __init__(self, metasv_path, parent=None):
        super().__init__(parent)
        self.metasv_path = metasv_path
        self.runner = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        input_group = QGroupBox("输入文件")
        input_layout = QFormLayout()

        self.voice_input = self.create_file_input("选择声库 (.nofs)")
        self.project_input = self.create_file_input("选择项目 (.svp)")
        self.dictionary_input = self.create_dir_input("选择词典目录 (clf-data)")
        self.output_input = self.create_save_input("保存音频文件 (.wav)")

        input_layout.addRow("声库:", self.voice_input)
        input_layout.addRow("项目:", self.project_input)
        input_layout.addRow("词典目录:", self.dictionary_input)
        input_layout.addRow("输出文件:", self.output_input)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # 渲染参数
        param_group = QGroupBox("渲染参数")
        param_layout = QFormLayout()

        self.language_combo = QComboBox()
        self.language_combo.addItems(["mandarin", "japanese"])

        self.pitch_mode_combo = QComboBox()
        self.pitch_mode_combo.addItems(["notes", "auto"])

        param_layout.addRow("语言:", self.language_combo)
        param_layout.addRow("音高模式:", self.pitch_mode_combo)

        param_group.setLayout(param_layout)
        layout.addWidget(param_group)

        # 渲染按钮
        self.render_btn = QPushButton("开始渲染")
        self.render_btn.clicked.connect(self.start_render)
        layout.addWidget(self.render_btn)

        # 输出日志
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Courier", 10))
        layout.addWidget(QLabel("输出日志:"))
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def create_file_input(self, button_text):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        line_edit = QLineEdit()
        button = QPushButton(button_text)
        button.clicked.connect(lambda: self.browse_file(line_edit))

        layout.addWidget(line_edit)
        layout.addWidget(button)
        widget.setLayout(layout)
        widget.line_edit = line_edit
        return widget

    def create_dir_input(self, button_text):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        line_edit = QLineEdit()
        button = QPushButton(button_text)
        button.clicked.connect(lambda: self.browse_dir(line_edit))

        layout.addWidget(line_edit)
        layout.addWidget(button)
        widget.setLayout(layout)
        widget.line_edit = line_edit
        return widget

    def create_save_input(self, button_text):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        line_edit = QLineEdit()
        button = QPushButton(button_text)
        button.clicked.connect(lambda: self.save_file(line_edit))

        layout.addWidget(line_edit)
        layout.addWidget(button)
        widget.setLayout(layout)
        widget.line_edit = line_edit
        return widget

    def browse_file(self, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if file_path:
            line_edit.setText(file_path)

    def browse_dir(self, line_edit):
        dir_path = QFileDialog.getExistingDirectory(self, "选择目录")
        if dir_path:
            line_edit.setText(dir_path)

    def save_file(self, line_edit):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "WAV Files (*.wav)")
        if file_path:
            line_edit.setText(file_path)

    def start_render(self):
        voice = self.voice_input.line_edit.text()
        project = self.project_input.line_edit.text()
        dictionary = self.dictionary_input.line_edit.text()
        output = self.output_input.line_edit.text()
        language = self.language_combo.currentText()
        pitch_mode = self.pitch_mode_combo.currentText()

        if not all([voice, project, dictionary, output]):
            QMessageBox.warning(self, "输入错误", "请填写所有必需字段")
            return

        command = (
            f'"{self.metasv_path}" render '
            f'--voice "{voice}" '
            f'--project "{project}" '
            f'--output "{output}" '
            f'--language {language} '
            f'--dictionary "{dictionary}" '
            f'--pitch-mode {pitch_mode}'
        )

        self.log_output.clear()
        self.log_output.append(f"执行命令:\n{command}\n")

        self.runner = CommandRunner(command)
        self.runner.output.connect(self.log_output.append)
        self.runner.finished.connect(self.render_finished)
        self.runner.start()

        self.render_btn.setEnabled(False)

    def render_finished(self, code):
        self.render_btn.setEnabled(True)
        if code == 0:
            self.log_output.append("\n✓ 渲染完成！")
            QMessageBox.information(self, "完成", "歌声渲染完成！")
        else:
            self.log_output.append(f"\n✗ 渲染失败，退出码: {code}")


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.metasv_path = self.find_metasv()
        self.init_ui()

    def find_metasv(self):
        """查找 MetaSV 可执行文件"""
        # Windows 路径
        default_path_win = Path(__file__).parent.parent / "target" / "release" / "metasv.exe"
        if default_path_win.exists():
            return str(default_path_win)

        # macOS/Linux 路径
        default_path_unix = Path(__file__).parent.parent / "target" / "release" / "metasv"
        if default_path_unix.exists():
            return str(default_path_unix)

        # 提示用户选择
        QMessageBox.information(
            None,
            "选择 MetaSV",
            "请选择 MetaSV 可执行文件 (Windows: metasv.exe, macOS/Linux: metasv)"
        )
        file_path, _ = QFileDialog.getOpenFileName(None, "选择 MetaSV 可执行文件")
        return file_path if file_path else None

    def init_ui(self):
        self.setWindowTitle("MetaSV GUI - 歌声合成训练工具")
        self.setGeometry(100, 100, 1000, 700)

        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # 标题
        title = QLabel("MetaSV 图形界面")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 显示 MetaSV 路径
        if self.metasv_path:
            path_label = QLabel(f"MetaSV 路径: {self.metasv_path}")
            path_label.setStyleSheet("color: green;")
            layout.addWidget(path_label)
        else:
            path_label = QLabel("未找到 MetaSV 可执行文件！")
            path_label.setStyleSheet("color: red;")
            layout.addWidget(path_label)

        # 选项卡
        tabs = QTabWidget()
        tabs.addTab(DatasetTab(self.metasv_path, self), "数据集采集")
        tabs.addTab(TrainTab(self.metasv_path, self), "模型训练")
        tabs.addTab(ExportTab(self.metasv_path, self), "声库导出")
        tabs.addTab(RenderTab(self.metasv_path, self), "歌声渲染")

        layout.addWidget(tabs)

        central_widget.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用 Fusion 风格，跨平台一致

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
