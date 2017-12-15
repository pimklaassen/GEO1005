# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DispatchHero_dockwidget_base.ui'
#
# Created: Thu Dec 14 15:44:10 2017
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

class Ui_DispatchHeroDockWidgetBase(object):
    def setupUi(self, DispatchHeroDockWidgetBase):
        DispatchHeroDockWidgetBase.setObjectName(_fromUtf8("DispatchHeroDockWidgetBase"))
        DispatchHeroDockWidgetBase.resize(1342, 857)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setGeometry(QtCore.QRect(850, 550, 161, 61))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8(":/Dispatch/dispatch.jpg")))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.textEdit_2 = QtGui.QTextEdit(self.dockWidgetContents)
        self.textEdit_2.setGeometry(QtCore.QRect(610, 650, 61, 31))
        self.textEdit_2.setObjectName(_fromUtf8("textEdit_2"))
        self.lcdNumber_2 = QtGui.QLCDNumber(self.dockWidgetContents)
        self.lcdNumber_2.setGeometry(QtCore.QRect(670, 680, 61, 23))
        self.lcdNumber_2.setSmallDecimalPoint(False)
        self.lcdNumber_2.setDigitCount(5)
        self.lcdNumber_2.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcdNumber_2.setProperty("intValue", 19)
        self.lcdNumber_2.setObjectName(_fromUtf8("lcdNumber_2"))
        self.tableWidget = QtGui.QTableWidget(self.dockWidgetContents)
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
        self.tableWidget_2 = QtGui.QTableWidget(self.dockWidgetContents)
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
        self.treeWidget = QtGui.QTreeWidget(self.dockWidgetContents)
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
        self.pushButton = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton.setGeometry(QtCore.QRect(580, 610, 93, 28))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_3 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_3.setGeometry(QtCore.QRect(790, 640, 93, 28))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_4.setGeometry(QtCore.QRect(950, 640, 93, 28))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.textEdit = QtGui.QTextEdit(self.dockWidgetContents)
        self.textEdit.setGeometry(QtCore.QRect(60, 650, 491, 161))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.textEdit_3 = QtGui.QTextEdit(self.dockWidgetContents)
        self.textEdit_3.setGeometry(QtCore.QRect(670, 650, 61, 31))
        self.textEdit_3.setObjectName(_fromUtf8("textEdit_3"))
        self.Map = QtGui.QFrame(self.dockWidgetContents)
        self.Map.setGeometry(QtCore.QRect(0, 0, 756, 606))
        self.Map.setFrameShape(QtGui.QFrame.StyledPanel)
        self.Map.setFrameShadow(QtGui.QFrame.Raised)
        self.Map.setLineWidth(10)
        self.Map.setMidLineWidth(2)
        self.Map.setObjectName(_fromUtf8("Map"))
        self.verticalScrollBar_2 = QtGui.QScrollBar(self.Map)
        self.verticalScrollBar_2.setGeometry(QtCore.QRect(740, 0, 16, 601))
        self.verticalScrollBar_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar_2.setObjectName(_fromUtf8("verticalScrollBar_2"))
        self.horizontalScrollBar_2 = QtGui.QScrollBar(self.Map)
        self.horizontalScrollBar_2.setGeometry(QtCore.QRect(0, 590, 741, 16))
        self.horizontalScrollBar_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar_2.setObjectName(_fromUtf8("horizontalScrollBar_2"))
        self.label_3 = QtGui.QLabel(self.Map)
        self.label_3.setGeometry(QtCore.QRect(0, 0, 741, 591))
        self.label_3.setText(_fromUtf8(""))
        self.label_3.setPixmap(QtGui.QPixmap(_fromUtf8(":/Dispatch/Mapa.jpg")))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.toolButton_3 = QtGui.QToolButton(self.Map)
        self.toolButton_3.setGeometry(QtCore.QRect(0, 90, 27, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.toolButton_3.setFont(font)
        self.toolButton_3.setObjectName(_fromUtf8("toolButton_3"))
        self.toolButton_4 = QtGui.QToolButton(self.Map)
        self.toolButton_4.setGeometry(QtCore.QRect(0, 110, 27, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.toolButton_4.setFont(font)
        self.toolButton_4.setObjectName(_fromUtf8("toolButton_4"))
        self.Compass_2 = QwtCompass(self.Map)
        self.Compass_2.setGeometry(QtCore.QRect(0, 0, 71, 71))
        self.Compass_2.setLineWidth(4)
        self.Compass_2.setObjectName(_fromUtf8("Compass_2"))
        self.dateTimeEdit = QtGui.QDateTimeEdit(self.dockWidgetContents)
        self.dateTimeEdit.setGeometry(QtCore.QRect(360, 620, 194, 22))
        self.dateTimeEdit.setObjectName(_fromUtf8("dateTimeEdit"))
        self.pushButton_2 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_2.setGeometry(QtCore.QRect(670, 610, 93, 28))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.lcdNumber = QtGui.QLCDNumber(self.dockWidgetContents)
        self.lcdNumber.setGeometry(QtCore.QRect(610, 680, 61, 23))
        self.lcdNumber.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcdNumber.setProperty("intValue", 11)
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.pushButton_6 = QtGui.QPushButton(self.dockWidgetContents)
        self.pushButton_6.setGeometry(QtCore.QRect(450, 810, 93, 28))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        DispatchHeroDockWidgetBase.setWidget(self.dockWidgetContents)

        self.retranslateUi(DispatchHeroDockWidgetBase)
        QtCore.QMetaObject.connectSlotsByName(DispatchHeroDockWidgetBase)

    def retranslateUi(self, DispatchHeroDockWidgetBase):
        DispatchHeroDockWidgetBase.setWindowTitle(_translate("DispatchHeroDockWidgetBase", "Dispatch hero", None))
        self.textEdit_2.setHtml(_translate("DispatchHeroDockWidgetBase", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.5pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Sent</span></p></body></html>", None))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("DispatchHeroDockWidgetBase", "Autospuit", None))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("DispatchHeroDockWidgetBase", "Tankautospuit", None))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("DispatchHeroDockWidgetBase", "Autoladder", None))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("DispatchHeroDockWidgetBase", "New Row", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("DispatchHeroDockWidgetBase", "Truck status", None))
        item = self.tableWidget_2.verticalHeaderItem(0)
        item.setText(_translate("DispatchHeroDockWidgetBase", "Station #1", None))
        item = self.tableWidget_2.verticalHeaderItem(1)
        item.setText(_translate("DispatchHeroDockWidgetBase", "Station #2", None))
        item = self.tableWidget_2.verticalHeaderItem(2)
        item.setText(_translate("DispatchHeroDockWidgetBase", "Station #3", None))
        item = self.tableWidget_2.verticalHeaderItem(3)
        item.setText(_translate("DispatchHeroDockWidgetBase", "Station #4", None))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("DispatchHeroDockWidgetBase", "Other dispatchers", None))
        self.treeWidget.headerItem().setText(0, _translate("DispatchHeroDockWidgetBase", "Routes", None))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("DispatchHeroDockWidgetBase", "Route 1", None))
        self.treeWidget.topLevelItem(1).setText(0, _translate("DispatchHeroDockWidgetBase", "Route 2", None))
        self.treeWidget.topLevelItem(2).setText(0, _translate("DispatchHeroDockWidgetBase", "Route 3", None))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(_translate("DispatchHeroDockWidgetBase", "Auto ON", None))
        self.pushButton_3.setText(_translate("DispatchHeroDockWidgetBase", "Previous", None))
        self.pushButton_4.setText(_translate("DispatchHeroDockWidgetBase", "Next", None))
        self.textEdit.setHtml(_translate("DispatchHeroDockWidgetBase", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.5pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Progress:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">    -Calling                                                  05/11/2017    19:35:12</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">    -Truck out                                               05/11/2017    19:35:07</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">    -Bridge open                              05/11/2017     19:35:02</span></p></body></html>", None))
        self.textEdit_3.setHtml(_translate("DispatchHeroDockWidgetBase", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.5pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Need</span></p></body></html>", None))
        self.toolButton_3.setText(_translate("DispatchHeroDockWidgetBase", "+", None))
        self.toolButton_4.setText(_translate("DispatchHeroDockWidgetBase", "-", None))
        self.pushButton_2.setText(_translate("DispatchHeroDockWidgetBase", "Auto OFF", None))
        self.pushButton_6.setText(_translate("DispatchHeroDockWidgetBase", "Add", None))

from qwt_compass import QwtCompass
import Resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DispatchHeroDockWidgetBase = QtGui.QDockWidget()
    ui = Ui_DispatchHeroDockWidgetBase()
    ui.setupUi(DispatchHeroDockWidgetBase)
    DispatchHeroDockWidgetBase.show()
    sys.exit(app.exec_())

