# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/addclass.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from messagebox import messageBox

class Ui_ChooseStudents(object):

    def __init__(self, main):
        self.main = main
        self.selected = []
        Dialog = QtWidgets.QDialog()
        self.Dialog = Dialog
        self.setupUi(self.Dialog)

    def show(self):
        self.Dialog.show()
        self.Dialog.exec_()

    def updateLabel(self):
        self.num = 0
        for i in range(0, self.tableWidget.rowCount()):
            if(self.tableWidget.cellWidget(i, 1).isChecked()):
                self.num += 1
        self.label.setText("Wybrano " + str(self.num) + " uczniów")
    
    def saveChanges(self):
        if(self.num == 0):
            messageBox("Błąd", QtWidgets.QMessageBox.Warning, "Nie można dodać klasy", "Nie wybrano żadnych uczniów")
        else:
            for i in range(0, self.tableWidget.rowCount()):
                if(self.tableWidget.cellWidget(i, 1).isChecked()):
                    self.selected.append(self.rows[i][0])
            self.Dialog.close()
    
    def preselectCheckBoxes(self, user_list):
        for i in range(0, len(user_list)):
            for j in range(0, self.tableWidget.rowCount()):
                if(self.rows[j][0] == user_list[i]):
                    self.tableWidget.cellWidget(j, 1).setChecked(True)

    def fillData(self):
        self.tableWidget.setColumnCount(2)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setHorizontalHeaderLabels(["Uczeń", "Dodaj?"])
        self.rows = self.main.db.fetchall("SELECT id_uzytkownika, CONCAT_WS(' ', imie, nazwisko) FROM uzytkownicy WHERE rola = 'Uczeń'")
        self.tableWidget.setRowCount(len(self.rows))
        checkboxes = []
        for i in range(len(self.rows)):
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(self.rows[i][1]))
            checkboxes.append(QtWidgets.QCheckBox())
            self.tableWidget.setCellWidget(i, 1, checkboxes[i])
            self.tableWidget.resizeColumnsToContents()

        for i in range(0, len(checkboxes)):
            checkboxes[i].stateChanged.connect(self.updateLabel)
            

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(534, 601)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(190, 560, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(160, 10, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(10, 80, 511, 471))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 60, 181, 17))
        font = QtGui.QFont()
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # Mój kod

        Dialog.setStyleSheet("QCheckBox{ text-align: center; margin-left:50%; margin-right:50%; }")
        self.fillData()

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.saveChanges) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Wybierz uczniów"))
        self.label.setText(_translate("Dialog", "Wybrano 0 uczniów"))


class Ui_AddClass(object):

    def __init__(self, main):
        self.main = main
        Dialog = QtWidgets.QDialog()
        self.selected = []
        self.Dialog = Dialog
        self.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()

    def chooseStudents(self):
        picker = Ui_ChooseStudents(self.main)
        picker.show()
        self.selected = picker.selected
        self.label_6.setText("Wybrano " + str(len(self.selected)) + " uczniów")

    def saveChanges(self):
        if(len(self.selected) == 0 or self.lineEdit.text == '' or self.lineEdit_2.text() == ''):
            messageBox("Błąd", QtWidgets.QMessageBox.Warning, "Nie można dodać przedmiotu", "Nie podano nazwy lub skrótu klasy lub nie wybrano żadnych uczniów")
        else:
            id_nauczyciela = self.rows[self.comboBox.currentIndex()][0]
            already_exists = bool(self.main.db.fetchone(f"SELECT COUNT(*) FROM przedmioty WHERE skrot_przedmiotu = '{self.lineEdit.text()}' OR nazwa_przedmiotu = '{self.lineEdit_2.text()}'"))
            if(already_exists):
                messageBox("Błąd", QtWidgets.QMessageBox.Warning, "Nie można dodać przedmiotu", "Przedmiot o podanej nazwie lub skrócie już istnieje")
            else:
                id_przedmiotu = self.main.db.execute(f"INSERT INTO przedmioty (skrot_przedmiotu, nazwa_przedmiotu, id_nauczyciela) VALUES ('{self.lineEdit.text()}', '{self.lineEdit_2.text()}', {id_nauczyciela}) RETURNING id_przedmiotu", True)
                for i in self.selected:
                    self.main.db.execute(f"INSERT INTO uzytkownicy_przedmioty (id_uzytkownika, id_przedmiotu) VALUES ({i}, {id_przedmiotu[0]})")
                messageBox("Sukces", QtWidgets.QMessageBox.Information, "Dodano przedmiot", "Przedmiot został dodany do bazy danych.")
                self.Dialog.close()
                self.main.getClasses()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(471, 379)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 451, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(6, 52, 461, 301))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setMaxLength(50)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setMaxLength(10)
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.comboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        # Mój kod

        self.pushButton.clicked.connect(self.saveChanges)
        self.pushButton_2.clicked.connect(self.chooseStudents)

        self.teacher_ids = []

        self.rows = self.main.db.fetchall("SELECT id_uzytkownika, CONCAT_WS(' ', imie, nazwisko) FROM uzytkownicy WHERE rola = 'Nauczyciel' ORDER BY id_uzytkownika")
        for row in self.rows:
            self.comboBox.addItem(str(row[1]))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dodawanie użytkownika"))
        self.label.setText(_translate("Dialog", "Dodawanie klasy"))
        self.label_7.setText(_translate("Dialog", "Pełna nazwa klasy"))
        self.label_5.setText(_translate("Dialog", "Skrót klasy"))
        self.label_8.setText(_translate("Dialog", "Nauczyciel"))
        self.label_6.setText(_translate("Dialog", "Wybrano 0 uczniów"))
        self.pushButton_2.setText(_translate("Dialog", "Wybierz uczniów"))
        self.pushButton.setText(_translate("Dialog", "Dodaj klasę"))
