# from PyQt5.uic.properties import QtGui
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from matplotlib import pyplot

from main import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
 # from PyQt5.QtCore import *
# from epics import PV


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import random

import matplotlib.pyplot as plt
import numpy as np





class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'smarthouse'
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 200
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # creo font bold per label title
        myFont = QtGui.QFont()
        myFont.setBold(True)

        # label titolo
        title = QLabel('SmartHouse',self)
        title.move(150, 10)
        title.setFont(myFont)

        # bottoni per scegliere il dataset
        button1 = QPushButton('Dataset A', self)
        button1.move(20, 50)
        button1.clicked.connect(lambda: self.on_button(1))

        button2 = QPushButton('Dataset B', self)
        button2.move(20, 100)
        button2.clicked.connect(lambda: self.on_button(2))

        self.show()


    # che merda porcodiaz
    def plot_matrix(self, matrix):

        size = 10
        data = np.arange(size * size).reshape((size, size))

        # Limits for the extent
        x_start = 3.0
        x_end = 9.0
        y_start = 6.0
        y_end = 12.0

        # extent = [x_start, x_end, y_start, y_end]

        # The normal figure
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111)
        im = ax.imshow(matrix, extent=matrix, origin='lower', interpolation='None', cmap='viridis')

        # Add the text
        jump_x = (x_end - x_start) / (2.0 * size)
        jump_y = (y_end - y_start) / (2.0 * size)
        x_positions = np.linspace(start=x_start, stop=x_end, num=size, endpoint=False)
        y_positions = np.linspace(start=y_start, stop=y_end, num=size, endpoint=False)

        for y_index, y in enumerate(y_positions):
            for x_index, x in enumerate(x_positions):
                label = data[y_index, x_index]
                text_x = x + jump_x
                text_y = y + jump_y
                ax.text(text_x, text_y, label, color='black', ha='center', va='center')

        # fig.colorbar(im)
        plt.show()





    def on_button(self, n):
        # predizione sul dataset n
        # calculate è la funzione di main.py
        startProb, transProb, obsProb = calculate(n)

        # plt.plot(transProb)
        # plt.show()

        # TODO: per le matrici provare con label dinameiche in una nuova finestra

        self.plot_matrix(transProb)




        print(startProb)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

