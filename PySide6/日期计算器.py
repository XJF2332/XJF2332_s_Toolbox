import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QDateEdit, QSpinBox
from PySide6.QtCore import QDate
import datetime

class DateCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('日期计算器')

        # 设置窗口的初始大小
        self.resize(400, 200)

        # 创建布局
        layout = QVBoxLayout()

        # 创建日期输入
        self.dateEdit = QDateEdit(self)
        self.dateEdit.setDisplayFormat('yyyy-MM-dd')
        self.dateEdit.setDate(QDate.currentDate())
        self.dateEdit.setStyleSheet("font-size: 20pt;")  # 设置字体大小
        layout.addWidget(self.dateEdit)

        # 创建天数输入
        self.daysSpinBox = QSpinBox(self)
        self.daysSpinBox.setMinimum(-10000)
        self.daysSpinBox.setMaximum(10000)
        self.daysSpinBox.setStyleSheet("font-size: 20pt;")  # 设置字体大小
        layout.addWidget(self.daysSpinBox)

        # 创建计算按钮
        self.calculateButton = QPushButton('计算日期', self)
        self.calculateButton.clicked.connect(self.calculate_date)
        self.calculateButton.setStyleSheet("font-size: 20pt;")  # 设置字体大小
        layout.addWidget(self.calculateButton)

        # 创建结果标签
        self.resultLabel = QLabel('结果:', self)
        self.resultLabel.setStyleSheet("font-size: 20pt;")  # 设置字体大小
        layout.addWidget(self.resultLabel)

        self.setLayout(layout)

    def calculate_date(self):
        # 获取用户输入的日期和天数
        input_date = self.dateEdit.date().toPython()
        days = self.daysSpinBox.value()

        # 计算新日期
        new_date = input_date + datetime.timedelta(days=days)
        self.resultLabel.setText(f'结果: {new_date.strftime("%Y-%m-%d")}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = DateCalculator()
    calculator.show()
    sys.exit(app.exec())
