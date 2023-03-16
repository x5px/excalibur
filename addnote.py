# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/addnote.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import psycopg2
from config import config

class Ui_AddNote(object):

    def __init__(self, class_shortcut):
        self.refresh = False
        self.class_shortcut = class_shortcut
        self.params = config()
        self.Dialog = QtWidgets.QDialog()
        self.setupUi(self.Dialog)
        self.Dialog.show()
        self.Dialog.exec()


    def fillComboBoxes(self):
        self.label_5.setText("Przedmiot: " + self.class_shortcut)

        try:
            conn = psycopg2.connect(**self.params)
            cur = conn.cursor()                     # tworzenie kursora do bazy

            query = f"SELECT id_przedmiotu FROM przedmioty WHERE skrot_przedmiotu = \'{self.class_shortcut}\'"
            cur.execute(query)
            class_id = cur.fetchone()[0]

            query = f"SELECT CONCAT_WS(' ', imie, nazwisko)  FROM uzytkownicy_przedmioty INNER JOIN uzytkownicy ON uzytkownicy_przedmioty.id_uzytkownika = uzytkownicy.id_uzytkownika WHERE uzytkownicy_przedmioty.id_przedmiotu = {class_id}" # pobierz nazwy uczniów
            cur.execute(query)
            user_names = cur.fetchall()

            query = f"SELECT skrot_sprawdzianu FROM sprawdziany INNER JOIN przedmioty ON sprawdziany.id_przedmiotu=przedmioty.id_przedmiotu WHERE sprawdziany.id_przedmiotu = {class_id}" # pobierz nazwy sprawdzianów
            cur.execute(query)
            test_names = cur.fetchall()

            test_names = [x[0] for x in test_names] # usuwamy tuple
            user_names = [x[0] for x in user_names]

            for i in range(0, len(test_names)):
                self.comboBox.addItem(test_names[i])
            for i in range(0, len(user_names)):
                self.comboBox_2.addItem(user_names[i])
                

        except (Exception, psycopg2.DatabaseError) as err:
            print(f"Błąd połączenia z bazą: {err}")
            return False
        finally:
            if conn is not None:
                conn.close()                        # zamknięcie konektora do bazy

    def addResultsToDB(self):
        test_name = self.comboBox.currentText()
        student_name = self.comboBox_2.currentText()
        grade = self.comboBox_3.currentText()
        value = self.comboBox_4.currentText()
        # Add the results to the database
        try:
            conn = psycopg2.connect(**self.params)
            cur = conn.cursor()                     # tworzenie kursora do bazy
            # Get id of the test
            query = f"SELECT id_sprawdzianu FROM sprawdziany WHERE skrot_sprawdzianu = \'{test_name}\'"
            cur.execute(query)
            test_id = cur.fetchone()[0]
            # Get id of the student
            query = f"SELECT id_uzytkownika FROM uzytkownicy WHERE CONCAT_WS(' ', imie, nazwisko) = \'{student_name}\'"
            cur.execute(query)
            student_id = cur.fetchone()[0]

            query = f"INSERT INTO oceny(id_ucznia, id_sprawdzianu, ocena, wartosc) VALUES({student_id}, {test_id}, \'{grade}\', \'{value}\')"
            cur.execute(query)
            conn.commit()
            self.refresh = True
            #self.Dialog.close() # zamknij okno
        except (Exception, psycopg2.DatabaseError) as err:
            print(f"Błąd połączenia z bazą: {err}")
            return False
        finally:
            if conn is not None:
                conn.close()                        # zamknięcie konektora do bazy


    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(460, 326)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(120, 10, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(20, 290, 401, 17))
        self.label_5.setObjectName("label_5")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(6, 62, 441, 191))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout.addWidget(self.comboBox_2, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.comboBox_3 = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.gridLayout.addWidget(self.comboBox_3, 2, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
        self.comboBox_4 = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.gridLayout.addWidget(self.comboBox_4, 3, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 4, 0, 1, 2)


        # Mój kod

        self.fillComboBoxes()
        self.pushButton.clicked.connect(self.addResultsToDB)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dodawanie oceny"))
        self.label.setText(_translate("Dialog", "Dodawanie oceny"))
        self.label_2.setText(_translate("Dialog", "Sprawdzian"))
        self.label_3.setText(_translate("Dialog", "Uczeń"))
        self.label_4.setText(_translate("Dialog", "Ocena"))
        self.comboBox_3.setItemText(0, _translate("Dialog", "1"))
        self.comboBox_3.setItemText(1, _translate("Dialog", "1+"))
        self.comboBox_3.setItemText(2, _translate("Dialog", "2-"))
        self.comboBox_3.setItemText(3, _translate("Dialog", "2"))
        self.comboBox_3.setItemText(4, _translate("Dialog", "2+"))
        self.comboBox_3.setItemText(5, _translate("Dialog", "3-"))
        self.comboBox_3.setItemText(6, _translate("Dialog", "3"))
        self.comboBox_3.setItemText(7, _translate("Dialog", "3+"))
        self.comboBox_3.setItemText(8, _translate("Dialog", "4-"))
        self.comboBox_3.setItemText(9, _translate("Dialog", "4"))
        self.comboBox_3.setItemText(10, _translate("Dialog", "4+"))
        self.comboBox_3.setItemText(11, _translate("Dialog", "5-"))
        self.comboBox_3.setItemText(12, _translate("Dialog", "5"))
        self.comboBox_3.setItemText(13, _translate("Dialog", "5+"))
        self.comboBox_3.setItemText(14, _translate("Dialog", "6-"))
        self.comboBox_3.setItemText(15, _translate("Dialog", "6"))
        self.label_6.setText(_translate("Dialog", "Wartość oceny"))
        self.comboBox_4.setItemText(0, _translate("Dialog", "Zwykła"))
        self.comboBox_4.setItemText(1, _translate("Dialog", "Semestralna"))
        self.comboBox_4.setItemText(2, _translate("Dialog", "Końcowa"))
        self.pushButton.setText(_translate("Dialog", "Dodaj ocenę"))

