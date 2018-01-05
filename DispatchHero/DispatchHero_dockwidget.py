# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DispatchHeroDockWidget
                                 A QGIS plugin
 This plugin dispatches firetrucks
                             -------------------
        begin                : 2017-12-13
        git sha              : $Format:%H$
        copyright            : (C) 2017 by TU Delft
        email                : pim.o.klaassen@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os, time

from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import *
from PyQt4.QtCore import QThread

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'spatial_decision_dockwidget_base_extra.ui'))


class DispatchHeroDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()
    #custom signals
    updateAttribute = QtCore.pyqtSignal(str)

    def __init__(self, iface, parent=None):
        """Constructor."""
        super(DispatchHeroDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        #setup global variables
        self.iface = iface
        self.canvas = self.iface.mapCanvas()

        # set up GUI operation signals
        self.importDataButton.clicked.connect(self.importData)
        self.startCounterButton.clicked.connect(self.startCounter)
        self.stopCounterButton.clicked.connect(self.stopCounter)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def importData(self, filename=''):
        new_file = QtGui.QFileDialog.getOpenFileName(self, "", os.path.dirname(os.path.abspath(__file__)))
        if new_file:
            self.iface.addProject(unicode(new_file))

    def startCounter(self):
        new_file = QtGui.QFileDialog.getOpenFileName(self, "", os.path.dirname(os.path.abspath(__file__)))
        fh = open(new_file, 'r')
        openings = fh.readlines()
        fh.close()
        self.dataThread = DataThread(openings)
        self.dataThread.start()

    def stopCounter(self):
        self.dataThread.quit()


class DataThread(QThread):

    def __init__(self, openings):
        QThread.__init__(self)
        self.openings = openings

    def __del__(self):
        self.wait()

    def run(self):
        for bridge in self.openings:
            bridge = bridge.split(',')[0]
            self.bridgesList.addItem(bridge)
            self.sleep(5)