import os
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox, \
    QVBoxLayout, QWidget, QCheckBox, QTextEdit, QDialog, QDialogButtonBox, QHBoxLayout, QSizePolicy, QProgressBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PIL import Image

class ImageDialog(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("图片确认")
        layout = QVBoxLayout()
        label = QLabel()
        pixmap = QPixmap(image_path)
        if pixmap.width() > 800 or pixmap.height() > 600:
            pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
        layout.addWidget(label)
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Discard)
        button_box.button(QDialogButtonBox.Save).setText("保留")
        button_box.button(QDialogButtonBox.Discard).setText("忽略")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图片筛选工具")

        layout = QVBoxLayout()

        # 选择图片目录
        self.folder_label = QLabel("图片目录:")
        layout.addWidget(self.folder_label)
        self.folder_edit = QLineEdit()
        layout.addWidget(self.folder_edit)
        self.folder_button = QPushButton("选择目录")
        self.folder_button.clicked.connect(self.select_folder)
        layout.addWidget(self.folder_button)

        # 设置宽度阈值
        self.width_label = QLabel("宽度阈值 (像素):")
        layout.addWidget(self.width_label)
        self.width_edit = QLineEdit("1500")
        layout.addWidget(self.width_edit)

        # 设置高度阈值
        self.height_label = QLabel("高度阈值 (像素):")
        layout.addWidget(self.height_label)
        self.height_edit = QLineEdit("1500")
        layout.addWidget(self.height_edit)

        # 设置大小阈值
        self.size_label = QLabel("大小阈值 (KB):")
        layout.addWidget(self.size_label)
        self.size_edit = QLineEdit("700")
        layout.addWidget(self.size_edit)

        # 是否递归搜索子目录
        self.recursive_checkbox = QCheckBox("递归搜索子目录")
        layout.addWidget(self.recursive_checkbox)

        # 是否保留透明图片
        self.keep_transparency_checkbox = QCheckBox("保留含有透明度的图片")
        layout.addWidget(self.keep_transparency_checkbox)

        # 选择保存路径
        self.save_label = QLabel("保存路径:")
        layout.addWidget(self.save_label)
        self.save_edit = QLineEdit()
        layout.addWidget(self.save_edit)
        self.save_button = QPushButton("选择文件")
        self.save_button.clicked.connect(self.select_save_file)
        layout.addWidget(self.save_button)

        # 筛选进度条
        self.progress_bar_layout = QHBoxLayout()
        self.progress_label = QLabel("筛选进度:")
        self.progress_bar = QProgressBar()
        self.progress_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.progress_bar_layout.addWidget(self.progress_label)
        self.progress_bar_layout.addWidget(self.progress_bar)
        layout.addLayout(self.progress_bar_layout)

        # 开始筛选按钮
        self.start_button = QPushButton("开始筛选")
        self.start_button.clicked.connect(self.start_filtering)
        layout.addWidget(self.start_button)

        # 日志显示区域
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setStyleSheet("""
            QProgressBar {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                background-color: #E0E0E0;
                color: #000000;
                border-style: none;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #184e83;
                border-radius: 5px;
            }
        """)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择图片目录")
        if folder:
            self.folder_edit.setText(folder)

    def select_save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "选择保存文件", "", "文本文件 (*.txt)")
        if file_name:
            self.save_edit.setText(file_name)

    def start_filtering(self):
        folder = self.folder_edit.text()
        if not folder:
            QMessageBox.warning(self, "错误", "请选择图片目录。")
            return

        save_path = self.save_edit.text()
        if not save_path:
            QMessageBox.warning(self, "错误", "请选择保存路径。")
            return

        try:
            width_threshold = int(self.width_edit.text())
            height_threshold = int(self.height_edit.text())
            size_threshold = int(self.size_edit.text())
        except ValueError:
            QMessageBox.warning(self, "错误", "阈值必须是整数。")
            return

        recursive = self.recursive_checkbox.isChecked()
        keep_transparency = self.keep_transparency_checkbox.isChecked()

        # 筛选图片
        image_files = self.get_image_files(folder, recursive)
        total_images = len(image_files)
        self.progress_bar.setRange(0, total_images)
        self.progress_bar.setValue(0)

        filtered_image_files = []
        for index, img_path in enumerate(image_files):
            self.progress_bar.setValue(index + 1)
            try:
                with Image.open(img_path) as img:
                    width, height = img.size
                    if width < width_threshold or height < height_threshold:
                        # 检查是否是长图
                        aspect_ratio = width / height
                        if 1 / 2.5 < aspect_ratio < 2.5:
                            filtered_image_files.append(img_path)
                        else:
                            # 弹出对话框
                            dialog = ImageDialog(img_path, self)
                            result = dialog.exec()
                            if result == QDialog.Accepted:
                                filtered_image_files.append(img_path)
                            else:
                                self.log_text.append(f"{img_path} 是长图，已忽略。")
                        # 检查透明度
                        if not keep_transparency:
                            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                                filtered_image_files.remove(img_path)
                                self.log_text.append(f"{img_path} 包含透明度，已丢弃。")
            except Exception as e:
                self.log_text.append(f"无法打开文件 {img_path}: {e}")

        # 保存结果
        with open(save_path, 'w', encoding='utf-8') as f:
            for img in filtered_image_files:
                f.write(img + '\n')

        self.log_text.append(f"筛选完成，共找到 {len(filtered_image_files)} 张图片。结果已保存到 {save_path}")

    def get_image_files(self, folder, recursive):
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')
        image_files = []

        if recursive:
            for root, _, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path.lower().endswith(image_extensions) and not file_path.lower().endswith('.gif'):
                        if os.path.getsize(file_path) < 700 * 1024:
                            image_files.append(file_path.replace('/', '\\'))
        else:
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                if os.path.isfile(file_path) and file_path.lower().endswith(image_extensions) and not file_path.lower().endswith('.gif'):
                    if os.path.getsize(file_path) < 700 * 1024:
                        image_files.append(file_path.replace('/', '\\'))

        return image_files

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()