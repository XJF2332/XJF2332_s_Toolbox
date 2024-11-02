import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QSlider, QPushButton, QHBoxLayout, QLineEdit
from PySide6.QtCore import Qt

class TimeCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("时间计算器")
        self.setGeometry(100, 100, 400, 300)

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        self.sport_slider, self.sport_label = self.create_slider_with_label("云运动次数", 0, 22)
        self.read_slider, self.read_label = self.create_slider_with_label("云阅读次数", 0, 26)
        self.teach_slider, self.teach_label = self.create_slider_with_label("云支教次数", 0, 17)
        self.learn_slider, self.learn_label = self.create_slider_with_label("云研学次数", 0, 19)

        self.calculate_button = QPushButton("计算时长")
        self.calculate_button.setStyleSheet("font-size: 18px; padding: 10px;")
        self.calculate_button.clicked.connect(self.calculate_time)

        self.result_line_edit = QLineEdit()
        self.result_line_edit.setReadOnly(True)
        self.result_line_edit.setStyleSheet("font-size: 18px;")

        self.layout.addWidget(self.sport_label)
        self.layout.addWidget(self.sport_slider)
        self.layout.addWidget(self.read_label)
        self.layout.addWidget(self.read_slider)
        self.layout.addWidget(self.teach_label)
        self.layout.addWidget(self.teach_slider)
        self.layout.addWidget(self.learn_label)
        self.layout.addWidget(self.learn_slider)
        self.layout.addWidget(self.calculate_button)
        self.layout.addWidget(self.result_line_edit)

        self.central_widget.setLayout(self.layout)

    def create_slider_with_label(self, label, min_value, max_value):
        layout = QHBoxLayout()
        slider_label = QLabel(f"{label}: 0")
        slider_label.setStyleSheet("font-size: 18px;")
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_value)
        slider.setMaximum(max_value)
        slider.valueChanged.connect(lambda value, label=slider_label: label.setText(f"{label.text().split(':')[0]}: {value}"))
        layout.addWidget(slider_label)
        layout.addWidget(slider)
        self.layout.addLayout(layout)
        return slider, slider_label

    def calculate_time(self):
        sport = self.sport_slider.value()
        read = self.read_slider.value()
        teach = self.teach_slider.value()
        learn = self.learn_slider.value()

        if sport > 15:
            time_sport = 0.5 * 15 + 0.33 * (sport - 15)
        else:
            time_sport = 0.5 * sport

        if read > 7:
            time_read = 0.5 * 7 + 0.33 * (read - 7)
        else:
            time_read = 0.5 * read

        if teach > 5:
            time_teach = 0.75 * 5 + 0.5 * (teach - 5)
        else:
            time_teach = 0.75 * teach

        if learn > 2:
            time_learn = 0.75 * 2 + 0.5 * (learn - 2)
        else:
            time_learn = 0.75 * learn

        total = round(time_sport + time_learn + time_teach + time_read, 2)
        total_str = f"{total} 小时"
        self.result_line_edit.setText(total_str)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimeCalculator()
    window.show()
    sys.exit(app.exec())
