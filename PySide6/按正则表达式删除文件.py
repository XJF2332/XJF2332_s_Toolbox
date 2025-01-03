import os
import re
import send2trash
from PySide6 import QtWidgets, QtCore

def find_files(directory, regex_pattern):
    directory = directory.replace("/", os.sep)
    pattern = re.compile(regex_pattern)
    matching_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if pattern.search(file):
                matching_files.append(os.path.join(root, file))
    return matching_files

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件移动助手")
        self.layout = QtWidgets.QVBoxLayout(self)

        # 目录选择
        self.directory_layout = QtWidgets.QHBoxLayout()
        self.directory_label = QtWidgets.QLabel("目录路径:")
        self.directory_edit = QtWidgets.QLineEdit()
        self.directory_button = QtWidgets.QPushButton("选择目录")
        self.directory_button.clicked.connect(self.choose_directory)
        self.directory_layout.addWidget(self.directory_label)
        self.directory_layout.addWidget(self.directory_edit)
        self.directory_layout.addWidget(self.directory_button)
        self.layout.addLayout(self.directory_layout)

        # 正则表达式输入
        self.regex_layout = QtWidgets.QHBoxLayout()
        self.regex_label = QtWidgets.QLabel("正则表达式:")
        self.regex_edit = QtWidgets.QLineEdit()
        self.regex_edit.setText(".+")
        self.regex_layout.addWidget(self.regex_label)
        self.regex_layout.addWidget(self.regex_edit)
        self.layout.addLayout(self.regex_layout)

        # 文件列表
        self.file_list = QtWidgets.QListWidget()
        self.layout.addWidget(self.file_list)

        # 确认按钮
        self.confirm_button = QtWidgets.QPushButton("移动到回收站")
        self.confirm_button.clicked.connect(self.move_to_trash)
        self.layout.addWidget(self.confirm_button)

        # 信号连接
        self.directory_edit.textChanged.connect(self.update_file_list)
        self.regex_edit.textChanged.connect(self.update_file_list)

        # 初始化当前目录和正则表达式
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.directory_edit.setText(self.current_directory)
        self.current_regex_pattern = ".+"

        # 初始文件列表更新
        self.update_file_list()

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
                padding: 7px;
            }
            QPushButton:hover {
                border-radius: 5px;
                background-color: #267bcf;
            }
            QPushButton:pressed {
                border-radius: 5px;
                background-color: #123d69;
                padding: 6px 9px;
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
            QLineEdit {
                color: #333333;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                font-size: 10pt;
                padding: 5px;
            }
            QScrollBar:vertical {
                width: 10px;
                background-color: #F0F0F0;
            }
            QScrollBar:horizontal {
                height: 10px;
                background-color: #F0F0F0;
            }    
            QScrollBar::groove {
                background-color: #E0E0E0;
                border-radius: 3px;
            }
            QScrollBar::handle {
                background-color: #184e83;
                min-height: 20px;
                border-radius: 3px;
            }
            QScrollBar::handle:hover {
                background-color: #267bcf;
            }
            QScrollBar::handle:pressed {
                background-color: #123d69;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                height: 0px;
                background: none;
            }
            QScrollBar::add-page, QScrollBar::sub-page {
                background: none;
            }
            QListWidget {
                background-color: #FAFAFA;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                font-size: 11pt;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #CCCCCC;            
            }
            QListWidget::item:selected {
                background-color: #184e83;
                color: white;
                
            }
        """)

    def choose_directory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "选择目录", self.current_directory)
        if directory:
            self.current_directory = directory
            self.directory_edit.setText(self.current_directory)
            self.update_file_list()

    def update_file_list(self):
        directory = self.directory_edit.text()
        regex_pattern = self.regex_edit.text()

        if not directory:
            directory = os.path.dirname(os.path.abspath(__file__))
            self.directory_edit.setText(directory)

        if not regex_pattern:
            regex_pattern = ".+"
            self.regex_edit.setText(regex_pattern)

        try:
            files = find_files(directory, regex_pattern)
            self.file_list.clear()
            self.file_list.addItems(files)
        except re.error as e:
            QtWidgets.QMessageBox.warning(self, "正则表达式错误", f"正则表达式无效: {e}")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "错误", f"无法查找文件: {e}")

    def move_to_trash(self):
        files = [self.file_list.item(i).text() for i in range(self.file_list.count())]
        if not files:
            QtWidgets.QMessageBox.information(self, "提示", "没有文件可供移动。")
            return

        reply = QtWidgets.QMessageBox.question(self, "确认移动", "确定将这些文件移动到回收站？",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            for file in files:
                try:
                    send2trash.send2trash(file)
                except Exception as e:
                    QtWidgets.QMessageBox.warning(self, "错误", f"无法移动文件 {file}: {e}")
            self.update_file_list()
            QtWidgets.QMessageBox.information(self, "完成", "文件已移动到回收站。")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()