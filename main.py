# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\main.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
import hashlib
import psycopg2
from config import config
import re
from iforgot import Ui_IForgot
from PyQt5.QtWidgets import QTableWidgetItem

class LoginWindow(object):

    def __init__(self):
        Form = QtWidgets.QWidget()
        self.Form = Form
        self.setupUi(Form)
        self.Form.show()
    
    def clear_show(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.Form.show()

    def messageBox(self, title, icon, text, infoText="", detailText=""):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(icon)
        msg.setText(text)
        msg.setInformativeText(infoText)
        msg.setWindowTitle(title)
        msg.setDetailedText(detailText)
        msg.exec_()

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

        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        email = self.lineEdit.text().lower()
        haslo = self.lineEdit_2.text()
        if len(email) == 0 or len(haslo) == 0:
            self.messageBox("Logowanie nie powiodło się", QtWidgets.QMessageBox.Warning, "Wpisz adres e-mail i hasło.")
        elif not re.fullmatch(email_regex, email):
            self.messageBox("Logowanie nie powiodło się", QtWidgets.QMessageBox.Warning, "Niewłaściwy email. Adres musi zawierać znaki @ i .")
        else:
            haslo_md5 = hashlib.md5(haslo.encode('utf-8')).hexdigest()
            if(self.checkLoginData(email, haslo_md5)):
                self.messageBox("Logowanie powiodło się!", QtWidgets.QMessageBox.Information, "Zostałeś zalogowany.")
                self.Form.close()
                global main
                main.show(email)
            else:
                self.messageBox("Logowanie nie powiodło się", QtWidgets.QMessageBox.Warning, "Adres e-mail lub hasło jest nieprawidłowe.")
    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(589, 358)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(290, -10, 301, 91))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 0, 81, 81))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(".\\ui\\../login.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(180, 100, 251, 241))
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

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # Mój kod

        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(Ui_IForgot)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Logowanie"))
        self.label_2.setText(_translate("Form", "Dziennik - Logowanie"))
        self.label_3.setText(_translate("Form", "Adres e-mail"))
        self.label_5.setText(_translate("Form", "Hasło"))
        self.pushButton.setText(_translate("Form", "Zaloguj"))
        self.pushButton_2.setText(_translate("Form", "Zapomniałeś hasła?"))

class Ui_MainWindow(object):

    def __init__(self):
        MainWindow = QtWidgets.QMainWindow()
        self.MainWindow = MainWindow
        self.setupUi(MainWindow)
        self.db = QtSql.QSqlDatabase.addDatabase('QPSQL')
        self.params = config()
        self.db.setHostName(self.params['host'])
        self.db.setDatabaseName(self.params['database'])
        self.db.setUserName(self.params['user'])
        self.db.setPassword(self.params['password'])
    
    def show(self, email):
        self.MainWindow.show()
        self.getUserInfo(email)

    def getUserInfo(self, email):
        conn = None
        try:                    # wczytujemy paramtery połaczenia z bazą
            conn = psycopg2.connect(**self.params)       # łączenie z bazą
            cur = conn.cursor()                     # tworzenie kursora do bazy
            query = f"SELECT id_uzytkownika, imie, nazwisko, rola FROM uzytkownicy WHERE email = \'{email}\'" # query
            cur.execute(query)
            result = cur.fetchone()
        except (Exception, psycopg2.DatabaseError) as err:
            print(f"Błąd połączenia z bazą: {err}")
            return False
        finally:
            if conn is not None:
                conn.close()                        # zamknięcie konektora do bazy
        self.user_id = result[0]
        self.user_name = result[1]
        self.user_surname = result[2]
        self.user_role = result[3]
        self.label_2.setText(f"Witaj, {self.user_name} {self.user_surname} | Rola: {self.user_role}")
        self.getClasses()

    def getClasses(self):
        conn = None
        try:
            conn = psycopg2.connect(**self.params)       # łączenie z bazą
            cur = conn.cursor()                     # tworzenie kursora do bazy
            query = f"SELECT skrot_przedmiotu FROM przedmioty INNER JOIN uzytkownicy ON przedmioty.id_nauczyciela = uzytkownicy.id_uzytkownika WHERE id_nauczyciela = {self.user_id} " # query
            cur.execute(query)
            results = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as err:
            print(f"Błąd połączenia z bazą: {err}")
            return False
        finally:
            if conn is not None:
                conn.close()                        # zamknięcie konektora do bazy
        
        for i in results:
            self.comboBox.addItem(i[0])

    def getClassData(self):
        self.tableWidget.clear()
        status = self.db.open()
        if status == False:
            pass
        else:
            class_shortcut = self.comboBox.currentText()
            # Pobierz nazwy sprawdzianów i uczniów
            conn = None
            try:
                conn = psycopg2.connect(**self.params)       # łączenie z bazą
                cur = conn.cursor()                     # tworzenie kursora do bazy

                #todo: refactor do executemany(), na razie zostaje w ten sposób dla przejrzystości

                query = f"SELECT id_przedmiotu FROM przedmioty WHERE skrot_przedmiotu = \'{class_shortcut}\'" # pobierz ID klasy
                cur.execute(query)
                class_id = cur.fetchone()[0]

                query = f"SELECT skrot_sprawdzianu FROM sprawdziany INNER JOIN przedmioty ON sprawdziany.id_przedmiotu=przedmioty.id_przedmiotu WHERE sprawdziany.id_przedmiotu = {class_id}" # pobierz nazwy sprawdzianów
                cur.execute(query)
                cols_name = cur.fetchall()

                query = f"SELECT CONCAT_WS(' ', imie, nazwisko)  FROM uzytkownicy_przedmioty INNER JOIN uzytkownicy ON uzytkownicy_przedmioty.id_uzytkownika = uzytkownicy.id_uzytkownika WHERE uzytkownicy_przedmioty.id_przedmiotu = {class_id}" # pobierz nazwy uczniów
                cur.execute(query)
                rows_name = cur.fetchall()
            except (Exception, psycopg2.DatabaseError) as err:
                print(f"Błąd połączenia z bazą: {err}")
                return False
            finally:
                if conn is not None:
                    conn.close()                        # zamknięcie konektora do bazy

            self.tableWidget.setColumnCount(len(cols_name))
            row = 0
            sql = f"SELECT ocena FROM oceny INNER JOIN sprawdziany ON sprawdziany.id_sprawdzianu = oceny.id_sprawdzianu WHERE id_przedmiotu = {class_id}"
            query = QtSql.QSqlQuery(sql)
            while query.next():
                self.tableWidget.insertRow(row)
                self.tableWidget.setRowCount(row+1)
                for i in range(0, len(rows_name)):
                    self.tableWidget.setItem(row, i, QtWidgets.QTableWidgetItem(str(query.value(i))))
                row = row + 1
            self.tableWidget.setHorizontalHeaderLabels([x[0] for x in cols_name])
            self.tableWidget.setVerticalHeaderLabels([x[0] for x in rows_name])

    def logout(self):
        self.MainWindow.hide()
        global login
        login.clear_show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(530, 0, 261, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 40, 781, 501))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(78)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 131, 21))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setGeometry(QtCore.QRect(0, 0, 121, 22))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuPlik = QtWidgets.QMenu(self.menubar)
        self.menuPlik.setObjectName("menuPlik")
        self.menuNauczyciel = QtWidgets.QMenu(self.menubar)
        self.menuNauczyciel.setObjectName("menuNauczyciel")
        self.menuAdmin = QtWidgets.QMenu(self.menubar)
        self.menuAdmin.setObjectName("menuAdmin")
        self.menuUcze = QtWidgets.QMenu(self.menubar)
        self.menuUcze.setObjectName("menuUcze")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionWyloguj_si = QtWidgets.QAction(MainWindow)
        self.actionWyloguj_si.setObjectName("actionWyloguj_si")
        self.actionZamknij_program = QtWidgets.QAction(MainWindow)
        self.actionZamknij_program.setObjectName("actionZamknij_program")
        self.actionDodaj_u_ytkownika = QtWidgets.QAction(MainWindow)
        self.actionDodaj_u_ytkownika.setObjectName("actionDodaj_u_ytkownika")
        self.actionDodaj_klas = QtWidgets.QAction(MainWindow)
        self.actionDodaj_klas.setObjectName("actionDodaj_klas")
        self.actionDodaj_sprawdzian = QtWidgets.QAction(MainWindow)
        self.actionDodaj_sprawdzian.setObjectName("actionDodaj_sprawdzian")
        self.actionDodaj_ocen = QtWidgets.QAction(MainWindow)
        self.actionDodaj_ocen.setObjectName("actionDodaj_ocen")
        self.actionDodaj_wiele_ocen = QtWidgets.QAction(MainWindow)
        self.actionDodaj_wiele_ocen.setObjectName("actionDodaj_wiele_ocen")
        self.actionZmie_oceny = QtWidgets.QAction(MainWindow)
        self.actionZmie_oceny.setObjectName("actionZmie_oceny")
        self.actionDodaj_oceny = QtWidgets.QAction(MainWindow)
        self.actionDodaj_oceny.setObjectName("actionDodaj_oceny")
        self.actionDodaj_wiele_ocen_2 = QtWidgets.QAction(MainWindow)
        self.actionDodaj_wiele_ocen_2.setObjectName("actionDodaj_wiele_ocen_2")
        self.actionZmie_oceny_2 = QtWidgets.QAction(MainWindow)
        self.actionZmie_oceny_2.setObjectName("actionZmie_oceny_2")
        self.actionZmie_w_a_ciwo_ci_u_ytkownika = QtWidgets.QAction(MainWindow)
        self.actionZmie_w_a_ciwo_ci_u_ytkownika.setObjectName("actionZmie_w_a_ciwo_ci_u_ytkownika")
        self.actionDodaj_klas_2 = QtWidgets.QAction(MainWindow)
        self.actionDodaj_klas_2.setObjectName("actionDodaj_klas_2")
        self.actionZmie_w_a_ciwo_ci_klasy = QtWidgets.QAction(MainWindow)
        self.actionZmie_w_a_ciwo_ci_klasy.setObjectName("actionZmie_w_a_ciwo_ci_klasy")
        self.menuPlik.addAction(self.actionWyloguj_si)
        self.menuPlik.addAction(self.actionZamknij_program)
        self.menuNauczyciel.addAction(self.actionDodaj_sprawdzian)
        self.menuNauczyciel.addSeparator()
        self.menuNauczyciel.addAction(self.actionDodaj_oceny)
        self.menuNauczyciel.addAction(self.actionDodaj_wiele_ocen_2)
        self.menuNauczyciel.addSeparator()
        self.menuNauczyciel.addAction(self.actionZmie_oceny_2)
        self.menuAdmin.addAction(self.actionDodaj_u_ytkownika)
        self.menuAdmin.addAction(self.actionZmie_w_a_ciwo_ci_u_ytkownika)
        self.menuAdmin.addSeparator()
        self.menuAdmin.addAction(self.actionDodaj_klas_2)
        self.menuAdmin.addAction(self.actionZmie_w_a_ciwo_ci_klasy)
        self.menubar.addAction(self.menuPlik.menuAction())
        self.menubar.addAction(self.menuUcze.menuAction())
        self.menubar.addAction(self.menuNauczyciel.menuAction())
        self.menubar.addAction(self.menuAdmin.menuAction())

        # Mój kod

        self.actionWyloguj_si.triggered.connect(self.logout)
        self.actionZamknij_program.triggered.connect(app.closeAllWindows)
        self.comboBox.currentTextChanged.connect(self.getClassData)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dziennik"))
        self.label.setText(_translate("MainWindow", "Klasa:"))
        self.label_2.setText(_translate("MainWindow", "Witaj, username ! | Rola: role"))
        self.menuPlik.setTitle(_translate("MainWindow", "Plik"))
        self.menuNauczyciel.setTitle(_translate("MainWindow", "Nauczyciel"))
        self.menuAdmin.setTitle(_translate("MainWindow", "Admin"))
        self.menuUcze.setTitle(_translate("MainWindow", "Uczeń"))
        self.actionWyloguj_si.setText(_translate("MainWindow", "Wyloguj się"))
        self.actionZamknij_program.setText(_translate("MainWindow", "Zamknij program"))
        self.actionZamknij_program.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionDodaj_u_ytkownika.setText(_translate("MainWindow", "Dodaj użytkownika"))
        self.actionDodaj_klas.setText(_translate("MainWindow", "Dodaj klasę"))
        self.actionDodaj_sprawdzian.setText(_translate("MainWindow", "Dodaj sprawdzian"))
        self.actionDodaj_ocen.setText(_translate("MainWindow", "Dodaj ocenę"))
        self.actionDodaj_wiele_ocen.setText(_translate("MainWindow", "Dodaj wiele ocen"))
        self.actionZmie_oceny.setText(_translate("MainWindow", "Zmień oceny"))
        self.actionDodaj_oceny.setText(_translate("MainWindow", "Dodaj ocenę"))
        self.actionDodaj_wiele_ocen_2.setText(_translate("MainWindow", "Dodaj wiele ocen"))
        self.actionZmie_oceny_2.setText(_translate("MainWindow", "Zmień oceny"))
        self.actionZmie_w_a_ciwo_ci_u_ytkownika.setText(_translate("MainWindow", "Zmień właściwości użytkownika"))
        self.actionDodaj_klas_2.setText(_translate("MainWindow", "Dodaj klasę"))
        self.actionZmie_w_a_ciwo_ci_klasy.setText(_translate("MainWindow", "Zmień właściwości klasy"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = LoginWindow()
    main = Ui_MainWindow()
    sys.exit(app.exec_())

