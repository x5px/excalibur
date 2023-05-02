# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\login.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import hashlib
import psycopg2
from functools import lru_cache

from config import config
from iforgot import Ui_IForgot
from validate import validateEmail
from messagebox import messageBox

class Ui_LoginWindow(object):

    def __init__(self, main):
        
        self.isDBOkay = self.checkDBConnection()
        if not self.isDBOkay:
            messageBox("Błąd połączenia z bazą danych", QtWidgets.QMessageBox.Critical, "Błąd połączenia z bazą danych", "Nie udało się połączyć z bazą danych. Sprawdź konfigurację database.ini. Jeżeli uruchamiasz Excalibura po raz pierwszy, uruchom najpierw setup.py")
            exit()
        else:
            self.main = main
            Form = QtWidgets.QWidget()
            self.Form = Form
            self.setupUi(Form)
            self.clear_show()

    @lru_cache(maxsize=1)
    def checkDBConnection(self):
        conn = None
        try:
            params = config()
        except Exception:
            return False
        try:
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM uzytkownicy")
            result = cur.fetchone()
            if result[0] > 0:
                return True
            else:
                return False
        except (Exception, psycopg2.DatabaseError) as e:
            return False
        finally:
            if conn is not None:
                conn.close()

    def clear_show(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.Form.show()

    def checkLoginData(self, email, haslo):
        conn = None
        try:
            params = config()                       # wczytujemy paramtery połaczenia z bazą
            conn = psycopg2.connect(**params)       # łączenie z bazą
            cur = conn.cursor()                     # tworzenie kursora do bazy
            query = f"SELECT haslo FROM uzytkownicy WHERE email = \'{email}\'" # query
            cur.execute(query)
            result = cur.fetchone()[0]
        except (Exception, psycopg2.DatabaseError) as err:
            print(f"Błąd połączenia z bazą: {err}")
            return False
        finally:
            if conn is not None:
                conn.close()                        # zamknięcie konektora do bazy
        
        if result == haslo:
            return True

    def login(self):
        email = self.lineEdit.text().lower()
        haslo = self.lineEdit_2.text()
        if len(email) == 0 or len(haslo) == 0:
            messageBox("Logowanie nie powiodło się", QtWidgets.QMessageBox.Warning, "Wpisz adres e-mail i hasło.")
        elif not validateEmail(email):
            messageBox("Logowanie nie powiodło się", QtWidgets.QMessageBox.Warning, "Niewłaściwy email. Adres musi zawierać znaki @ i .")
        else:
            haslo_md5 = hashlib.md5(haslo.encode('utf-8')).hexdigest()
            if(self.checkLoginData(email, haslo_md5)):
                messageBox("Logowanie powiodło się!", QtWidgets.QMessageBox.Information, "Zostałeś zalogowany.")
                self.Form.close()
                self.main.params = config()
                self.main.show_main(email)
            else:
                messageBox("Logowanie nie powiodło się", QtWidgets.QMessageBox.Warning, "Adres e-mail lub hasło jest nieprawidłowe.")

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(562, 393)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 0, 81, 81))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("images/logo.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(160, 100, 271, 241))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/login.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setIconSize(QtCore.QSize(20, 20))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(0, 80, 601, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(390, 10, 164, 65))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setItalic(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(0, 370, 781, 19))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setItalic(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setItalic(True)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)

        # Mój kod

        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(Ui_IForgot)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Logowanie"))
        self.label_3.setText(_translate("Form", "Adres e-mail"))
        self.label_5.setText(_translate("Form", "Hasło"))
        self.pushButton.setText(_translate("Form", "Zaloguj"))
        self.pushButton.setShortcut(_translate("Form", "Return"))
        self.pushButton_2.setText(_translate("Form", "Zapomniałeś hasła?"))
        self.label_6.setText(_translate("Form", f"Excalibur v.{self.main.currentVersion}"))
        self.label_2.setText(_translate("Form", "Logowanie"))
        self.label_4.setText(_translate("Form", "Zaloguj się do dziennika."))
        self.label_7.setText(_translate("Form", "made by Jakub Rutkowski"))
