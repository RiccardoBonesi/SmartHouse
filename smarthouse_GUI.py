from main import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'smarthouse'
        self.left = 100
        self.top = 100
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button1 = QPushButton('Dataset A', self)
        button1.move(10, 10)
        button1.clicked.connect(lambda: self.on_button(1))

        button2 = QPushButton('Dataset B', self)
        button2.move(10, 80)
        button2.clicked.connect(lambda: self.on_button(2))

        self.show()


    # def show_matrix(self, frame):



    def on_button(self, n):
        # predizione sul dataset n
        # calculate è la funzione di main.py
        startProb, transProb, obsProb = calculate(n)

        # self.show_matrix(transProb)

        print(startProb)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())