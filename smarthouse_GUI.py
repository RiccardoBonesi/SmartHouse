from PyQt5 import QtGui, QtCore, QtWidgets

from main import *
from preprocessing import *
import sys

from PyQt5.QtWidgets import *


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
        choose_days_label.move(230, 70)

        # COMBO BOX per la selezione dei giorni
        self.cb_days = QComboBox(self)
        self.cb_days.addItems(["Test #1", "Test #2", "Test #3", "Test #4", "Test #5","Test #6","Test #7","Test #8",
                               "Test #9","Test #10"])
        # self.cb.setCurrentIndex(0)
        self.cb_days.currentIndexChanged.connect(self.set_days)
        self.cb_days.setGeometry(230,100,140,30) # x, y, width, height


        # choose method
        choose_method_label = QLabel('Choose method: ', self)
        choose_method_label.move(440, 70)

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

        self.pred_label = QLabel('Predicted: ', self)
        self.pred_label.move(20,370)
        self.pred_label.setFont(myFont)
        self.pred_label.hide()


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

        list_truth = list(map(lambda v: f'{v}' if v < 10 else str(v), list_truth))
        list_pred = list(map(lambda v: f'{v}' if v < 10 else str(v), list_pred))

        for i in range(len(list_truth)):
            if list_truth[i] == list_pred[i]:
                list_truth[i] = list_pred[i] = f"<font face='mono' color='green'>&nbsp;{list_truth[i]}</font>"
            else:
                list_truth[i] = f"<font face='mono' color='red'>&nbsp;{list_truth[i]}</font>"
                list_pred[i] = f"<font face='mono' color='red'>&nbsp;{list_pred[i]}</font>"



        sample_rows = ["".join(list_truth[x: x + 5]) for x in range(0, len(list_truth), 5)]
        sample_text = "".join(sample_rows)

        predicted_rows = ["".join(list_pred[x: x + 5]) for x in range(0, len(list_pred), 5)]
        predicted_text = "".join(predicted_rows)


        self.sample_textbrowser.setText( sample_text)
        self.predicted_textbrowser.setText( predicted_text)




    def show_results(self, list_truth, list_pred, accuracy):
        self.show_lists(list_truth, list_pred)
        self.results_groupbox.show()

        self.accuracy_label.show()

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
        self.accuracy_value_label.hide()


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


        self.show_results(list_truth, list_pred, accuracy)

        first_start = False

        print("DAYS: {}".format(self.days))






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
