# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\updateclass.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import psycopg2
from config import config
from messagebox import messageBox
from addclass import Ui_ChooseStudents

class Ui_UpdateClass(object):

    def __init__(self, main):
        self.main = main
        self.index = None
        Dialog = QtWidgets.QDialog()
        self.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()


    def fillData(self):
        self.comboBox_2.clear()
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("SELECT nazwa_przedmiotu FROM przedmioty ORDER BY nazwa_przedmiotu")
            rows = cur.fetchall()
            for row in rows:
                self.comboBox_2.addItem(row[0])
            if(self.comboBox.count() == 0):
                cur.execute("SELECT CONCAT_WS(' ', imie, nazwisko) FROM uzytkownicy WHERE rola = 'Nauczyciel' ORDER BY id_uzytkownika")
                rows = cur.fetchall()
                for row in rows:
                    self.comboBox.addItem(row[0])
            cur.close()
        except (Exception, psycopg2.DatabaseError) as e:
            print("Błąd połączenia z bazą danych", e)
        finally:
            if conn is not None:
                conn.close()
        self.getClassData() # first init
        self.main.getClasses()

    def getClassData(self):
        conn = None 
        try:
            if(self.index != None):
                self.comboBox_2.setCurrentIndex(self.index)
            class_name = self.comboBox_2.currentText()    
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            query = f"SELECT id_przedmiotu FROM przedmioty WHERE nazwa_przedmiotu = '{class_name}'"
            cur.execute(query)
            self.class_id = cur.fetchone()[0]
            query = f"SELECT nazwa_przedmiotu, skrot_przedmiotu, CONCAT_WS(' ', imie, nazwisko) FROM przedmioty JOIN uzytkownicy ON przedmioty.id_nauczyciela = uzytkownicy.id_uzytkownika WHERE id_przedmiotu = {self.class_id}"
            cur.execute(query)
            rows = cur.fetchall() 
            for row in rows:
                self.lineEdit_2.setText(row[0])
                self.lineEdit.setText(row[1])
                self.comboBox.setCurrentText(row[2])
            query = f"SELECT id_uzytkownika FROM uzytkownicy_przedmioty WHERE id_przedmiotu = {self.class_id}"
            cur.execute(query)
            self.user_list = [x[0] for x in cur.fetchall()]
            self.label_6.setText("Wybrano " + str(len(self.user_list)) + " uczniów")
            cur.close()
        except TypeError:
            pass
        except (psycopg2.DatabaseError) as e:
            print("Błąd połączenia z bazą danych", e)
            conn.close()

    def showUserPicker(self):
        self.pickerOpened = True
        picker = Ui_ChooseStudents()
        picker.preselectCheckBoxes(self.user_list)
        picker.show()
        self.user_list = picker.selected
        self.label_6.setText("Wybrano " + str(len(self.user_list)) + " uczniów")
    
    def update(self):
        conn = None
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        if(self.pickerOpened): # nie ma sensu kasować id jeśli nie zmieniono uczniów
            cur.execute(f"DELETE FROM uzytkownicy_przedmioty WHERE id_przedmiotu = {self.class_id}")
            for user in self.user_list:
                cur.execute(f"INSERT INTO uzytkownicy_przedmioty (id_uzytkownika, id_przedmiotu) VALUES ({user}, {self.class_id})")
        cur.execute(f"UPDATE przedmioty SET nazwa_przedmiotu = '{self.lineEdit_2.text()}', skrot_przedmiotu = '{self.lineEdit.text()}', id_nauczyciela = (SELECT id_uzytkownika FROM uzytkownicy WHERE CONCAT_WS(' ', imie, nazwisko) = '{self.comboBox.currentText()}') WHERE id_przedmiotu = {self.class_id}")
        conn.commit()
        cur.close()
        self.comboBox_2.setCurrentText(self.lineEdit_2.text())
        self.index = self.comboBox_2.currentIndex()
        self.fillData()
        messageBox("Sukces", QtWidgets.QMessageBox.Information, "Zaktualizowano przedmiot")

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(473, 470)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 451, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 60, 451, 381))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_9 = QtWidgets.QLabel(self.widget)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.comboBox_2 = QtWidgets.QComboBox(self.widget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.verticalLayout.addWidget(self.comboBox_2)
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setMaxLength(50)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setMaxLength(10)
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        # Mój kod

        self.fillData() # first init
        self.pickerOpened = False
        self.comboBox_2.currentTextChanged.connect(self.getClassData)
        self.pushButton_2.clicked.connect(self.showUserPicker)
        self.pushButton.clicked.connect(self.update)


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dodawanie użytkownika"))
        self.label.setText(_translate("Dialog", "Zmiana właściwości klasy"))
        self.label_9.setText(_translate("Dialog", "Wybierz klasę"))
        self.label_7.setText(_translate("Dialog", "Pełna nazwa klasy"))
        self.label_5.setText(_translate("Dialog", "Skrót klasy"))
        self.label_8.setText(_translate("Dialog", "Nauczyciel"))
        #self.label_6.setText(_translate("Dialog", "Wybrano 0 uczniów"))
        self.pushButton_2.setText(_translate("Dialog", "Wybierz uczniów"))
        self.pushButton.setText(_translate("Dialog", "Zmień klasę"))