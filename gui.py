import sys
import subprocess
import re
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
    QHBoxLayout, QVBoxLayout, QGridLayout
)
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# -------------------------------
# ⏱️ 后台线程类：运行 main.py
# -------------------------------
class AnalysisWorker(QThread):
    finished = pyqtSignal(str)     # 分析成功后输出结果
    error = pyqtSignal(str)        # 分析失败后输出错误

    def __init__(self, company_name):
        super().__init__()
        self.company_name = company_name

    def run(self):
        try:
            python_exec = sys.executable
            base_dir = os.path.dirname(os.path.abspath(__file__))
            result = subprocess.run(
                [python_exec, "main.py", self.company_name],
                capture_output=True,
                text=True,
                check=True,
                cwd=base_dir,
            )
            self.finished.emit(result.stdout)
        except subprocess.CalledProcessError as e:
            self.error.emit(f"执行失败：\n{e.stderr}")
        except FileNotFoundError:
            self.error.emit("未找到 main.py，请确保它与 gui.py 位于同一文件夹")

# -------------------------------
# 🎨 GUI 主界面类
# -------------------------------
class ESGApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ESG 智能分析平台")
        self.setFixedSize(900, 700)
        self.worker = None

        # 加载背景图
        self.background = QPixmap("background.jpeg")

        # 输入框和按钮
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("请输入公司名称或代码")
        self.input_line.setMinimumHeight(35)
        self.input_line.setStyleSheet("font-size: 16px;")

        self.button = QPushButton("开始分析")
        self.button.setMinimumHeight(35)
        self.button.clicked.connect(self.run_analysis)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(self.button)

        # 得分标签
        self.env_score = QLabel("环境得分: -")
        self.soc_score = QLabel("社会得分: -")
        self.gov_score = QLabel("治理得分: -")
        self.esg_score = QLabel("综合得分: -")
        self.rating = QLabel("评级: -")

        for label in [self.env_score, self.soc_score, self.gov_score, self.esg_score, self.rating]:
            label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")

        scores_layout = QGridLayout()
        scores_layout.addWidget(self.env_score, 0, 0)
        scores_layout.addWidget(self.soc_score, 0, 1)
        scores_layout.addWidget(self.gov_score, 1, 0)
        scores_layout.addWidget(self.esg_score, 1, 1)
        scores_layout.addWidget(self.rating, 2, 0)

        # ESG评价与建议
        self.eval_output = QTextEdit()
        self.eval_output.setReadOnly(True)
        self.eval_output.setPlaceholderText("【ESG评价】")
        self.eval_output.setStyleSheet("font-size: 14px; color: black; background-color: rgba(255, 255, 255, 180);")

        self.advice_output = QTextEdit()
        self.advice_output.setReadOnly(True)
        self.advice_output.setPlaceholderText("【投资建议】")
        self.advice_output.setStyleSheet("font-size: 14px; color: black; background-color: rgba(255, 255, 255, 180);")

        text_layout = QVBoxLayout()
        text_layout.addWidget(QLabel("【ESG评价】"))
        text_layout.addWidget(self.eval_output)
        text_layout.addWidget(QLabel("【投资建议】"))
        text_layout.addWidget(self.advice_output)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(scores_layout)
        main_layout.addLayout(text_layout)
        self.setLayout(main_layout)

    # 🎨 背景图自动缩放绘制
    def paintEvent(self, event):
        painter = QPainter(self)
        scaled_bg = self.background.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        painter.drawPixmap(0, 0, scaled_bg)

    def run_analysis(self):
        company = self.input_line.text().strip()
        if not company:
            self.eval_output.setPlainText("⚠️ 请输入公司名称！")
            self.advice_output.clear()
            return

        self.button.setEnabled(False)
        self.eval_output.setPlainText("分析中，请稍候……")
        self.advice_output.clear()

        self.worker = AnalysisWorker(company)
        self.worker.finished.connect(self.on_analysis_done)
        self.worker.error.connect(self.on_analysis_error)
        self.worker.start()

    def on_analysis_done(self, output):
        self.button.setEnabled(True)
        self.parse_output(output)

    def on_analysis_error(self, error_msg):
        self.button.setEnabled(True)
        self.eval_output.setPlainText(error_msg)
        self.advice_output.clear()

    def parse_output(self, text):
        def extract(pattern, default="N/A"):
            match = re.search(pattern, text, re.S)
            return match.group(1).strip() if match else default

        self.env_score.setText(f"环境得分: {extract(r'环境得分[:：]\s*([\d.]+)')}")
        self.soc_score.setText(f"社会得分: {extract(r'社会得分[:：]\s*([\d.]+)')}")
        self.gov_score.setText(f"治理得分: {extract(r'治理得分[:：]\s*([\d.]+)')}")
        self.esg_score.setText(f"综合得分: {extract(r'综合ESG得分[:：]\s*([\d.]+)')}")
        self.rating.setText(f"评级: {extract(r'评级[:：]?\s*([A-Z+-]+)')}")

        esg_eval = extract(r"【ESG评价】[:：]?\s*\n?(.*?)(?=【投资建议】)", "未找到 ESG 评价内容")
        advice = extract(r"【投资建议】[:：]?\s*\n?(.*)", "未找到投资建议内容")

        self.eval_output.setPlainText(esg_eval)
        self.advice_output.setPlainText(advice)

# 程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ESGApp()
    window.show()
    sys.exit(app.exec())
