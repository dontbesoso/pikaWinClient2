from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QLineEdit)
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import re

from rejestracja import rejestracja

class logownik(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowStaysOnTopHint)
        self.interface()


    def interface(self):
        self.etykietaName = QLabel("Logowanie czesu pracy", self)
        self.etykietaName.setStyleSheet("padding: 5px;")

        self.inputCard = QLineEdit()
        self.inputCard.setEchoMode(QLineEdit.Password)
        self.inputCard.returnPressed.connect(self.onSubmit)
        self.inputCard.setStyleSheet("padding: 5px;")
        self.etykietaOperacja = QLabel("Przyłóż kartę do czytnika, aby zalogować \nobecność na stanowisku pracy.", self)
        self.etykietaOperacja.setStyleSheet("border: 1px solid black; padding: 5px; font-weight: bold")

        ukladOkna = QGridLayout()
        ukladOkna.setAlignment(Qt.AlignTop)
        ukladOkna.addWidget(self.etykietaName, 0, 0)
        ukladOkna.addWidget(self.inputCard, 1, 0)
        ukladOkna.addWidget(self.etykietaOperacja, 2, 0)
        self.setLayout(ukladOkna)

        self.setFixedSize(400, 130)
        self.setWindowTitle("Plum 0.4")

        self.setWindowIcon(QtGui.QIcon("plum.ico"))
        self.show()

    def onSubmit(self):
        inputText = self.inputCard.text()
        pattern = re.compile(r"\b[0]\d{9}\b")

        if pattern.match(inputText):
            rejestracja(inputText)


        self.inputCard.setText('')