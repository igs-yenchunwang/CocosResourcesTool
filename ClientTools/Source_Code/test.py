import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('按鈕新增標籤範例')
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.button = QPushButton('新增標籤')
        self.button.clicked.connect(self.add_label)

        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def add_label(self):
        lay = QVBoxLayout()
        label = QLabel('這是一個新標籤')
        
        lay.addWidget(label)
        self.layout.addLayout(lay)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
