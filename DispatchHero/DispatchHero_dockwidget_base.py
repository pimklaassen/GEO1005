# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DispatchHero_dockwidget_base.ui'
#
# Created: Fri Dec 15 10:26:02 2017
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1096, 847)
        self.Map = QtGui.QFrame(Form)
        self.Map.setGeometry(QtCore.QRect(0, 0, 761, 601))
        self.Map.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Map.setFrameShadow(QtGui.QFrame.Raised)
        self.Map.setLineWidth(10)
        self.Map.setMidLineWidth(2)
        self.Map.setObjectName(_fromUtf8("Map"))
        self.verticalScrollBar = QtGui.QScrollBar(self.Map)
        self.verticalScrollBar.setGeometry(QtCore.QRect(740, 0, 16, 601))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName(_fromUtf8("verticalScrollBar"))
        self.horizontalScrollBar = QtGui.QScrollBar(self.Map)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(0, 590, 741, 16))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName(_fromUtf8("horizontalScrollBar"))
        self.label = QtGui.QLabel(self.Map)
        self.label.setGeometry(QtCore.QRect(0, 0, 741, 591))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/Dispatch/Mapa.jpg")))
        self.label.setObjectName(_fromUtf8("label"))
        self.toolButton = QtGui.QToolButton(self.Map)
        self.toolButton.setGeometry(QtCore.QRect(0, 90, 27, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.toolButton.setFont(font)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.toolButton_2 = QtGui.QToolButton(self.Map)
        self.toolButton_2.setGeometry(QtCore.QRect(0, 110, 27, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.toolButton_2.setFont(font)
        self.toolButton_2.setObjectName(_fromUtf8("toolButton_2"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(580, 610, 93, 28))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(670, 610, 93, 28))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(790, 640, 93, 28))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(950, 640, 93, 28))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.tableWidget = QtGui.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(820, 20, 211, 191))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(5)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.treeWidget = QtGui.QTreeWidget(Form)
        self.treeWidget.setGeometry(QtCore.QRect(790, 670, 256, 161))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.treeWidget.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Bookman Old Style"))
        self.treeWidget.setFont(font)
        self.treeWidget.setAcceptDrops(False)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        self.tableWidget_2 = QtGui.QTableWidget(Form)
        self.tableWidget_2.setGeometry(QtCore.QRect(840, 240, 181, 171))
        self.tableWidget_2.setObjectName(_fromUtf8("tableWidget_2"))
        self.tableWidget_2.setColumnCount(1)
        self.tableWidget_2.setRowCount(5)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(6)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        self.textEdit = QtGui.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(60, 650, 491, 161))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.dateTimeEdit = QtGui.QDateTimeEdit(Form)
        self.dateTimeEdit.setGeometry(QtCore.QRect(360, 620, 194, 22))
        self.dateTimeEdit.setObjectName(_fromUtf8("dateTimeEdit"))
        self.textEdit_2 = QtGui.QTextEdit(Form)
        self.textEdit_2.setGeometry(QtCore.QRect(610, 650, 61, 31))
        self.textEdit_2.setObjectName(_fromUtf8("textEdit_2"))
        self.textEdit_3 = QtGui.QTextEdit(Form)
        self.textEdit_3.setGeometry(QtCore.QRect(670, 650, 61, 31))
        self.textEdit_3.setObjectName(_fromUtf8("textEdit_3"))
        self.lcdNumber = QtGui.QLCDNumber(Form)
        self.lcdNumber.setGeometry(QtCore.QRect(610, 680, 61, 23))
        self.lcdNumber.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcdNumber.setProperty("intValue", 11)
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.lcdNumber_2 = QtGui.QLCDNumber(Form)
        self.lcdNumber_2.setGeometry(QtCore.QRect(670, 680, 61, 23))
        self.lcdNumber_2.setSmallDecimalPoint(False)
        self.lcdNumber_2.setDigitCount(5)
        self.lcdNumber_2.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcdNumber_2.setProperty("intValue", 19)
        self.lcdNumber_2.setObjectName(_fromUtf8("lcdNumber_2"))
        self.pushButton_6 = QtGui.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(450, 810, 93, 28))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(850, 550, 161, 61))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8(":/Dispatch/dispatch.jpg")))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.toolButton.setText(_translate("Form", "+", None))
        self.toolButton_2.setText(_translate("Form", "-", None))
        self.pushButton.setText(_translate("Form", "Auto ON", None))
        self.pushButton_2.setText(_translate("Form", "Auto OFF", None))
        self.pushButton_3.setText(_translate("Form", "Previous", None))
        self.pushButton_4.setText(_translate("Form", "Next", None))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "Autospuit", None))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("Form", "Tankautospuit", None))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("Form", "Autoladder", None))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("Form", "New Row", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Truck status", None))
        self.treeWidget.headerItem().setText(0, _translate("Form", "Routes", None))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("Form", "Route 1", None))
        self.treeWidget.topLevelItem(1).setText(0, _translate("Form", "Route 2", None))
        self.treeWidget.topLevelItem(2).setText(0, _translate("Form", "Route 3", None))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        item = self.tableWidget_2.verticalHeaderItem(0)
        item.setText(_translate("Form", "Station #1", None))
        item = self.tableWidget_2.verticalHeaderItem(1)
        item.setText(_translate("Form", "Station #2", None))
        item = self.tableWidget_2.verticalHeaderItem(2)
        item.setText(_translate("Form", "Station #3", None))
        item = self.tableWidget_2.verticalHeaderItem(3)
        item.setText(_translate("Form", "Station #4", None))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Other dispatchers", None))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.5pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Progress:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"> -Calling                                                  05/11/2017  19:35:12</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"> -Truck out                                               05/11/2017 19:35:07</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\"> -Bridge open                         05/11/2017   19:35:02</span></p></body></html>", None))
        self.textEdit_2.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.5pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Sent</span></p></body></html>", None))
        self.textEdit_3.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.5pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Need</span></p></body></html>", None))
        self.pushButton_6.setText(_translate("Form", "Add", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

