import os
from PIL import Image
import send2trash
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QCheckBox, QSlider, QLabel, \
    QProgressBar, QHBoxLayout
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QFont


# 定义一个函数来处理单个文件的转换和删除
def process_file(img_name, directory, del_confirm, quality, transparency_trans, preserve_metadata, overwrite):
    with Image.open(os.path.join(directory, img_name)) as img:
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            if transparency_trans:
                print(f'{img_name} 含有透明度，但由于自定义设置仍然进行转换')
            else:
                print(f'跳过 {img_name} ，因为它含有透明度')
                return

        # 生成新的文件路径
        new_file_path = os.path.join(directory, img_name.replace('.png', '.jpg'))

        # 检查文件是否存在
        if os.path.exists(new_file_path) and not overwrite:
            print(f'跳过已存在的文件: {new_file_path}')
            return

        if preserve_metadata:
            metadata = img.info
            img = img.convert('RGB')
            img.save(new_file_path, 'JPEG', quality=quality, metadata=metadata)
            print(f'成功转换 {img_name} 为 {new_file_path}')
        else:
            img = img.convert('RGB')
            img.save(new_file_path, 'JPEG', quality=quality)
            print(f'成功转换 {img_name} 为 {new_file_path}')

        if del_confirm:
            send2trash.send2trash(os.path.join(directory, img_name))
            print(f'已将 {img_name} 发送到回收站')
        else:
            print(f'保留原文件：{img_name}')


class ConversionWorker(QThread):
    progress_signal = Signal(int)

    def __init__(self, directory, del_confirm, quality, transparency_trans, preserve_metadata, recursive, overwrite):
        super().__init__()
        self.directory = directory.replace('/', '\\')
        self.del_confirm = del_confirm
        self.quality = quality
        self.transparency_trans = transparency_trans
        self.preserve_metadata = preserve_metadata
        self.recursive = recursive
        self.overwrite = overwrite
        if self.recursive:
            self.png_files = []
            for root, dirs, files in os.walk(self.directory):
                for f in files:
                    if f.endswith('.png'):
                        self.png_files.append(os.path.join(root, f))
        else:
            self.png_files = [f for f in os.listdir(directory) if f.endswith('.png')]
        self.total = len(self.png_files)
        self.count = 0

    def run(self):
        for full_path in self.png_files:
            process_file(full_path, self.directory, self.del_confirm, self.quality, self.transparency_trans,
                         self.preserve_metadata, self.overwrite)
            self.count += 1
            self.progress_signal.emit(self.count)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口字体
        font = QFont("Arial", 10)
        self.setFont(font)

        # 创建控件
        self.dir_button = QPushButton('选择目录')
        self.dir_label = QLabel('未选择目录')

        self.del_checkbox = QCheckBox('删除原始PNG文件')
        self.trans_checkbox = QCheckBox('转换含有透明度的图像')
        self.metadata_checkbox = QCheckBox('保留元数据')
        self.recursive_checkbox = QCheckBox('递归查找子目录')
        self.overwrite_checkbox = QCheckBox('覆盖已存在的文件')

        self.quality_label = QLabel('质量: 100')
        self.quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.quality_slider.setRange(1, 100)
        self.quality_slider.setValue(100)

        self.start_button = QPushButton('开始转换')

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        # 布局
        layout = QVBoxLayout()
        layout.setSpacing(10)  # 设置控件之间的间距

        # 添加选择目录部分
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(self.dir_button)
        dir_layout.addWidget(self.dir_label)
        layout.addLayout(dir_layout)

        # 添加选项部分
        options_layout = QVBoxLayout()
        options_layout.addWidget(self.del_checkbox)
        options_layout.addWidget(self.trans_checkbox)
        options_layout.addWidget(self.metadata_checkbox)
        options_layout.addWidget(self.recursive_checkbox)
        options_layout.addWidget(self.overwrite_checkbox)
        layout.addLayout(options_layout)

        # 添加质量设置部分
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(self.quality_label)
        quality_layout.addWidget(self.quality_slider)
        layout.addLayout(quality_layout)

        # 添加开始按钮和进度条
        layout.addWidget(self.start_button)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

        # 信号连接
        self.dir_button.clicked.connect(self.choose_directory)
        self.quality_slider.valueChanged.connect(self.update_quality_label)
        self.start_button.clicked.connect(self.start_conversion)

        self.directory = ''
        self.del_confirm = False
        self.transparency_trans = False
        self.preserve_metadata = True
        self.quality = 100
        self.recursive = False
        self.overwrite = False

        self.setStyleSheet("""
            QSlider::groove:horizontal{
                height: 10px;
                left: 0px;
                right: 0px;
                border-radius:3px;
                background-color: #E0E0E0;
            }
            QSlider::sub-page:horizontal{
                border-radius:3px;
                background-color: #184e83;
            }
            QSlider::handle:horizontal{
                width: 10px;
                height: 10px;
                border-radius: 3px;
                background-color: #FFFFFF;
                margin: -5px 0;
            }
            QWidget {
                background-color: #F0F0F0;
            }
            QPushButton {
                border-radius: 5px;
                background-color: #184e83;
                color: white;
                border: none;
                padding: 5px 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                border-radius: 5px;
                background-color: #184e83;
            }
            QCheckBox {
                color: #333333;
                font-size: 10pt;
            }
            QLabel {
                color: #333333;
                font-size: 10pt;
            }
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

        # 设置窗口标题和固定大小
        self.setWindowTitle('PNG to JPG Converter')

    def choose_directory(self):
        dir_name = QFileDialog.getExistingDirectory(self, '选择目录')
        if dir_name:
            self.directory = dir_name
            self.dir_label.setText(self.directory)

    def update_quality_label(self):
        value = self.quality_slider.value()
        self.quality_label.setText(f'质量: {value}')
        self.quality = value

    def start_conversion(self):
        if not self.directory:
            print('未选择目录')
            return

        self.del_confirm = self.del_checkbox.isChecked()
        self.transparency_trans = self.trans_checkbox.isChecked()
        self.preserve_metadata = self.metadata_checkbox.isChecked()
        self.recursive = self.recursive_checkbox.isChecked()
        self.overwrite = self.overwrite_checkbox.isChecked()
        self.quality = self.quality_slider.value()

        # 获取所有PNG文件
        if self.recursive:
            png_files = []
            for root, dirs, files in os.walk(self.directory):
                for f in files:
                    if f.endswith('.png'):
                        png_files.append(os.path.join(root, f))
        else:
            png_files = [f for f in os.listdir(self.directory) if f.endswith('.png')]
        total = len(png_files)
        if total == 0:
            print('没有找到PNG文件')
            return

        # 设置进度条最大值
        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(0)

        # 启动工作线程
        self.worker = ConversionWorker(self.directory, self.del_confirm, self.quality, self.transparency_trans,
                                       self.preserve_metadata, self.recursive, self.overwrite)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()