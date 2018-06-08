# from PyQt5.uic.properties import QtGui
from PyQt5 import QtGui

from main import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from epics import PV

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


    # def show_matrix(self, data):
    #     # self.data = np.array(self.data).reshape(2048, 2048).astype(np.int32)
    #
    #     qimage = QtGui.QImage(data, data.shape[0], data.shape[1], QtGui.QImage.Format_RGB32)
    #     img = PrintImage(QPixmap(qimage))
    #     print('ciao')


    # NON FUNZIONA
    def show_matrix(self, data):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create widget
        label = QLabel(self)
        qimage = QtGui.QImage(data, data.shape[0], data.shape[1], QtGui.QImage.Format_RGB32)
        pixmap = QPixmap(qimage)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        self.show()



    def on_button(self, n):
        # predizione sul dataset n
        # calculate è la funzione di main.py
        startProb, transProb, obsProb = calculate(n)

        # self.show_matrix(transProb)

        print(startProb)


class PrintImage(QWidget):
    def __init__(self, pixmap, parent=None):
        QWidget.__init__(self, parent=parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

