# from PyQt5.uic.properties import QtGui
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
from matplotlib import pyplot

from main import *
from preprocessing import *
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
        self.left = 700
        self.top = 100
        self.width = 800
        self.height = 600
        self.initUI()
        self.days = 0
        self.method = 0


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
        choose_days_label = QLabel('Choose test: ', self)
        choose_days_label.move(220, 70)

        # COMBO BOX per la selezione dei giorni
        self.cb_days = QComboBox(self)
        self.cb_days.addItems(["1", "2", "3", "4", "5"])
        # self.cb.setCurrentIndex(0)
        self.cb_days.currentIndexChanged.connect(self.set_days)
        self.cb_days.setGeometry(230,100,60,30) # x, y, width, height




        # choose method
        choose_method_label = QLabel('Choose method: ', self)
        choose_method_label.move(450, 70)

        # COMBO BOX per la selezione del metodo
        self.cb_method = QComboBox(self)
        self.cb_method.addItems(["No Time Slice", "Time Slice"])
        # self.cb.setCurrentIndex(0)
        self.cb_method.currentIndexChanged.connect(self.set_method)
        self.cb_method.setGeometry(440, 100, 120, 30)  # x, y, width, height







        choose_dataset_label = QLabel('Choose a Dataset:', self)
        choose_dataset_label.move(340, 140)


        # bottoni per scegliere il dataset
        button1 = QPushButton('Dataset A', self)
        button1.move(290, 170)
        button1.clicked.connect(lambda: self.on_button(1))

        button2 = QPushButton('Dataset B', self)
        button2.move(410, 170)
        button2.clicked.connect(lambda: self.on_button(2))


        # RESULTS
        self.truth_label = QLabel('Ground truth:', self)
        self.truth_label.move(20, 230)
        self.truth_label.setFont(myFont)
        self.truth_label.hide()

        self.truth_states_label = QLabel(self)
        self.truth_states_label.move(20, 250)
        # self.truth_states_label.setGeometry(20, 250, 100, 100)  # x, y, width, height
        # self.truth_states_label.adjustSize()

        self.pred_label = QLabel('Predicted: ', self)
        self.pred_label.move(20,370)
        self.pred_label.setFont(myFont)
        self.pred_label.hide()

        self.pred_states_label = QLabel(self)
        self.pred_states_label.move(20, 390)


        self.accuracy_label = QLabel('Accuracy', self)
        self.accuracy_label.move(630, 265) #20,540
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.accuracy_label.setFont(font)
        self.accuracy_label.hide()



        self.accuracy_value_label = QLabel(self)
        self.accuracy_value_label.move(500, 250) #20, 560

        self.progress = QRoundProgressBar(self)
        self.progress.setBarStyle(QRoundProgressBar.BarStyle.LINE) # DONUT, LINE, PIE

        # style accordingly via palette
        palette = QPalette()
        brush = QBrush(QColor(50,205,50))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush)

        self.progress.setPalette(palette) #(20, 600, 150, 150)
        self.progress.setGeometry(600, 300, 150, 150)  # x, y, width, height

        self.progress.hide()

        self.preproc_label = QLabel('Dataset preprocessing...', self)
        self.preproc_label.move(320, 400)
        self.preproc_label.hide()



        # BOX
        self.results_groupbox = QtWidgets.QGroupBox(self)
        self.results_groupbox.setGeometry(QtCore.QRect(10, 230, 550, 320)) # x, y, width, height
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(60)
        self.results_groupbox.setFont(font)
        self.results_groupbox.setObjectName("results_groupbox")

        self.results_groupbox.hide()

        # Samples
        self.sample_textbrowser = QtWidgets.QTextBrowser(self.results_groupbox)
        self.sample_textbrowser.setGeometry(QtCore.QRect(20, 61, 250, 250)) # x, y, width, height
        self.sample_textbrowser.setObjectName("sample_textbrowser")
        self.sample_label = QtWidgets.QLabel(self.results_groupbox)
        self.sample_label.setGeometry(QtCore.QRect(20, 35, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.sample_label.setFont(font)
        self.sample_label.setObjectName("sample_label")
        self.sample_label.setText("Sample")

        # Predicted
        self.predicted_textbrowser = QtWidgets.QTextBrowser(self.results_groupbox)
        self.predicted_textbrowser.setGeometry(QtCore.QRect(290, 61, 250, 250)) # x, y, width, height
        self.predicted_textbrowser.setObjectName('predicted_textbrowser')
        self.predicted_label = QtWidgets.QLabel(self.results_groupbox)
        self.predicted_label.setGeometry(QtCore.QRect(290, 35, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.predicted_label.setFont(font)
        self.predicted_label.setObjectName("predicted_label")
        self.predicted_label.setText("Predicted")


        # SCROLLBAR SINCRONIZZATE
        self.sample_textbrowser.horizontalScrollBar().valueChanged.connect(
            self.predicted_textbrowser.horizontalScrollBar().setValue)
        self.sample_textbrowser.verticalScrollBar().valueChanged.connect(
            self.predicted_textbrowser.verticalScrollBar().setValue)
        self.predicted_textbrowser.horizontalScrollBar().valueChanged.connect(
            self.sample_textbrowser.horizontalScrollBar().setValue)
        self.predicted_textbrowser.verticalScrollBar().valueChanged.connect(
            self.sample_textbrowser.verticalScrollBar().setValue)



        self.show()



    def set_days(self, i):
        self.days = i+1


    def set_method(self, i):
        self.method = i+1

    def show_lists(self, list_truth, list_pred):


        # for i in range(len(sample)):
        #     if sample[i] == predicted[i]:
        #         sample[i] = predicted[i] = f"<font face='mono' color='green'>&nbsp;{sample[i]}</font>"
        #     else:
        #         sample[i] = f"<font face='mono' color='red'>&nbsp;{sample[i]}</font>"
        #         predicted[i] = f"<font face='mono' color='red'>&nbsp;{predicted[i]}</font>"



        self.sample_textbrowser.setText(list_truth)
        self.predicted_textbrowser.setText(list_pred)





    def show_results(self, list_truth, list_pred, accuracy):
        # self.truth_label.show()
        #
        # self.truth_states_label.setText(str(list_truth))
        # self.truth_states_label.adjustSize()
        #
        # self.pred_label.show()
        #
        # self.pred_states_label.setText(str(list_pred))
        # self.pred_states_label.adjustSize()
        #
        self.accuracy_label.show()
        #
        # self.accuracy_value_label.setText(str(accuracy) + " %")
        # self.accuracy_value_label.adjustSize()

        self.progress.setValue(accuracy)
        qApp.processEvents()
        self.progress.show()


        self.show_lists(list_truth, list_pred)
        self.results_groupbox.show()



    def hide_results(self):
        self.truth_label.hide()
        self.pred_label.hide()
        self.truth_states_label.hide()
        self.pred_states_label.hide()
        self.accuracy_label.hide()
        self.progress.hide()
        self.accuracy_value_label.hide()
        # self.preproc_label.hide()


    def start_preprocessing(self):
        self.hide_results()
        self.preproc_label.show()
        app.processEvents()
        generate_dataset()
        self.preproc_label.hide()






    def on_button(self, dt):

        # controllo se è il primo avvio
        first_start = True
        # se non è il primo avvio nascondo tutte le label dei risultati
        if not first_start:
            self.hide_results()

        # se non ho selezionato giorni di default imposto 1
        if (self.days==0):
            self.days=1

        # se non ho selezionato metto di default 1
        if (self.method==0):
            self.method=1

        list_pred, list_truth, accuracy = calculate(dt,self.days, self.method)

        # rimuove '\n' e '[]'
        list_truth = ' '.join(map(str, list_truth))
        list_pred = ' '.join(map(str, list_pred))


        self.show_results(list_truth, list_pred, accuracy)

        first_start = False

        print("DAYS: {}".format(self.days))






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
