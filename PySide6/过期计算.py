from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
from PySide6.QtCore import QDate
import sys

class ExpiryCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口的标题和初始大小
        self.setWindowTitle('保质期计算器')
        self.setGeometry(100, 100, 300, 200)

        # 垂直布局
        layout = QVBoxLayout()

        # 生产日期输入框
        self.prod_date_input = QLineEdit(self)
        self.prod_date_input.setPlaceholderText('生产日期 (YYYYMMDD)')
        layout.addWidget(self.prod_date_input)

        # 保质期输入框
        self.expiry_input = QLineEdit(self)
        self.expiry_input.setPlaceholderText('保质期')
        layout.addWidget(self.expiry_input)

        # 保质期单位下拉菜单
        self.expiry_unit = QComboBox(self)
        self.expiry_unit.addItems(['日', '月', '年'])
        layout.addWidget(self.expiry_unit)

        # 计算按钮
        self.calculate_button = QPushButton('计算剩余保质期', self)
        self.calculate_button.clicked.connect(self.calculate_expiry)
        layout.addWidget(self.calculate_button)

        # 设置布局
        self.setLayout(layout)

    def calculate_expiry(self):
        # 获取用户输入
        prod_date_str = self.prod_date_input.text()
        expiry = int(self.expiry_input.text())
        expiry_unit = self.expiry_unit.currentText()

        # 检查输入是否有效
        if len(prod_date_str) != 8 or not prod_date_str.isdigit():
            QMessageBox.warning(self, '错误', '请输入有效的生产日期！')
            return

        # 将字符串转换为日期
        prod_date = QDate(int(prod_date_str[:4]), int(prod_date_str[4:6]), int(prod_date_str[6:]))

        # 计算剩余保质期
        today = QDate.currentDate()
        if expiry_unit == '日':
            remaining_days = today.daysTo(prod_date.addDays(expiry))
        elif expiry_unit == '月':
            remaining_days = today.daysTo(prod_date.addMonths(expiry))
        elif expiry_unit == '年':
            remaining_days = today.daysTo(prod_date.addYears(expiry))

        # 检查是否过期
        if remaining_days < 0:
            QMessageBox.warning(self, '注意', '食物已过期！')
        else:
            QMessageBox.information(self, '剩余保质期', f'剩余保质期：{remaining_days}天')

# 创建应用程序和窗口实例
app = QApplication(sys.argv)
expiry_calculator = ExpiryCalculator()
expiry_calculator.show()
# 运行应用程序
sys.exit(app.exec())