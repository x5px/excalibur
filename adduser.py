# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/adduser.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import re
import hashlib
import psycopg2
from config import config

class Ui_AddUser(object):

    def __init__(self):
        self.Dialog = QtWidgets.QDialog()
        self.setupUi(self.Dialog)
        self.Dialog.show()
        self.Dialog.exec()

    def messageBox(self, title, icon, text, infoText="", detailText=""):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(icon)
        msg.setText(text)
        msg.setInformativeText(infoText)
        msg.setWindowTitle(title)
        msg.setDetailedText(detailText)
        msg.exec_()

    def checkIfEmailExists(self, email):
        try:
            params = config()                       # wczytujemy paramtery połaczenia z bazą
            conn = psycopg2.connect(**params)       # łączenie z bazą
            cur = conn.cursor()                     # tworzenie kursora do bazy
            query = f"SELECT COUNT(*) FROM uzytkownicy WHERE email = \'{email}\'" # query
            cur.execute(query)
            result = cur.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as err:
            print(f"Błąd połączenia z bazą: {err}")
            return False
        finally:
            if conn is not None:
                conn.close()                        # zamknięcie konektora do bazy
        
        return result

    def addUserFunction(self):

        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        email = self.lineEdit.text()
        haslo = self.lineEdit_2.text()
        rola = self.comboBox.currentText()
        if not re.fullmatch(email_regex, email):
            self.messageBox("Błąd", QtWidgets.QMessageBox.Critical, "Nieprawidłowy adres e-mail", "Wpisz poprawny adres e-mail")
            return
        elif self.checkIfEmailExists(email):
            self.messageBox("Błąd", QtWidgets.QMessageBox.Critical, "Adres e-mail jest już zajęty", "Użytkownik o podanym adresie e-mail już istnieje")
        else:
            print(f"Email: {email} | Hasło (plaintext): {haslo} | Hasło (MD5): {hashlib.md5(haslo.encode('utf-8')).hexdigest()} | Rola: {rola}")
            self.messageBox("Sukces", QtWidgets.QMessageBox.Information, "Dodano użytkownika", "Użytkownik został pomyślnie dodany do bazy danych.")


    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(460, 326)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(80, 10, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 50, 441, 261))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.comboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)

        # Mój kod

        self.pushButton.clicked.connect(self.addUserFunction)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dodawanie użytkownika"))
        self.label.setText(_translate("Dialog", "Dodawanie użytkownika"))
        self.label_2.setText(_translate("Dialog", "E-mail"))
        self.label_3.setText(_translate("Dialog", "Hasło"))
        self.label_4.setText(_translate("Dialog", "Rola"))
        self.comboBox.setItemText(0, _translate("Dialog", "Uczeń"))
        self.comboBox.setItemText(1, _translate("Dialog", "Nauczyciel"))
        self.comboBox.setItemText(2, _translate("Dialog", "Admin"))
        self.pushButton.setText(_translate("Dialog", "Dodaj użytkownika"))
