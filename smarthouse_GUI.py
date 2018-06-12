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

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPalette
from PyQt5.QtWidgets import QApplication, qApp
from qroundprogressbar import QRoundProgressBar






class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'smarthouse'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 800
        self.initUI()
        self.days = 0


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # creo font bold per label title
        myFont = QtGui.QFont()
        myFont.setBold(True)

        myTitle = QtGui.QFont()
        myTitle.setBold(True)
        myTitle.setPointSize(18)

        # label titolo
        title_label = QLabel('SmartHouse', self)
        title_label.move(300, 10)
        title_label.setFont(myTitle)

        # choose days
        choose_days_label = QLabel('Choose days to test: ', self)
        choose_days_label.move(330, 50)

        # COMBO BOX per la selezione dei giorni
        self.cb = QComboBox(self)
        self.cb.addItems(["1", "2", "3", "4", "5"])
        # self.cb.setCurrentIndex(0)
        self.cb.currentIndexChanged.connect(self.set_days)
        self.cb.setGeometry(360,80,60,30) # x, y, width, height


        choose_dataset_label = QLabel('Choose a Dataset:', self)
        choose_dataset_label.move(340, 120)


        # bottoni per scegliere il dataset
        button1 = QPushButton('Dataset A', self)
        button1.move(290, 150)
        button1.clicked.connect(lambda: self.on_button(1))

        button2 = QPushButton('Dataset B', self)
        button2.move(410, 150)
        button2.clicked.connect(lambda: self.on_button(2))


        # RESULTS
        self.truth_label = QLabel('Ground truth:', self)
        self.truth_label.move(20, 180)
        self.truth_label.setFont(myFont)
        self.truth_label.hide()

        self.truth_states_label = QLabel(self)
        self.truth_states_label.move(20, 200)

        self.pred_label = QLabel('Predicted: ', self)
        self.pred_label.move(20,320)
        self.pred_label.setFont(myFont)
        self.pred_label.hide()

        self.pred_states_label = QLabel(self)
        self.pred_states_label.move(20, 340)


        self.accuracy_label = QLabel('Accuracy: ', self)
        self.accuracy_label.move(20, 490)
        self.accuracy_label.setFont(myFont)
        self.accuracy_label.hide()

        self.accuracy_value_label = QLabel(self)
        self.accuracy_value_label.move(20, 510)

        self.progress = QRoundProgressBar(self)
        self.progress.setBarStyle(QRoundProgressBar.BarStyle.PIE) # DONUT, LINE

        # style accordingly via palette
        palette = QPalette()
        brush = QBrush(QColor(50,205,50))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush)

        self.progress.setPalette(palette)
        self.progress.setGeometry(20, 550, 150, 150)  # x, y, width, height

        self.progress.hide()


        self.show()



    def set_days(self, i):
        # print("Items in the list are :")
        # for count in range(self.cb.count()):
        #     print(self.cb.itemText(count))
        # print("Current index", i, "selection changed ", self.cb.currentText())

        self.days = i+1




    def show_results(self, list_truth, list_pred, accuracy):
        self.truth_label.show()

        self.truth_states_label.setText(str(list_truth))
        self.truth_states_label.adjustSize()

        self.pred_label.show()

        self.pred_states_label.setText(str(list_pred))
        self.pred_states_label.adjustSize()

        self.accuracy_label.show()

        self.accuracy_value_label.setText(str(accuracy) + " %")
        self.accuracy_value_label.adjustSize()

        self.progress.setValue(accuracy)
        qApp.processEvents()
        self.progress.show()



    def hide_results(self):
        self.truth_label.hide()
        self.pred_label.hide()
        self.truth_states_label.hide()
        self.pred_states_label.hide()
        self.accuracy_label.hide()
        self.progress.hide()





    def on_button(self, n):

        # controllo se è il primo avvio
        first_start = True
        # se non è il primo avvio nascondo tutte le label dei risultati
        if not first_start:
            self.hide_results()

        # se non ho selezionato giorni di default imposto 1
        if (self.days==0):
            self.days=1


        list_pred, pred, list_truth, n_states, accuracy = calculate(n,self.days)


        self.show_results(list_truth, list_pred, accuracy)

        first_start = False

        print("DAYS: {}".format(self.days))






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
