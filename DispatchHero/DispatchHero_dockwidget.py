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
from . import utility_functions as uf

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
        self.stopCounterButton.clicked.connect(self.cancelCounter)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def importData(self, filename=''):
        new_file = QtGui.QFileDialog.getOpenFileName(self, "", os.path.dirname(os.path.abspath(__file__)))
        if new_file:
            self.iface.addProject(unicode(new_file))

    def startCounter(self):
        # prepare the thread of the timed even or long loop
        new_file = QtGui.QFileDialog.getOpenFileName(self, "", os.path.dirname(os.path.abspath(__file__)))
        fh = open(new_file, 'r')
        self.bridgesGenerator = uf.BridgeParser(fh)
        self.bridgesGenerator.parse()
        self.timerThread = TimedEvent(self.iface.mainWindow(), self, self.bridgesGenerator.generator())
        self.timerThread.timerFinished.connect(self.concludeCounter)
        self.timerThread.timerError.connect(self.cancelCounter)
        self.timerThread.start()
        # from here the timer is running in the background on a separate thread. user can continue working on QGIS.
        self.startCounterButton.setDisabled(True)
        self.stopCounterButton.setDisabled(False)

    def cancelCounter(self):
        # triggered if the user clicks the cancel button
        self.timerThread.stop()
        try:
            self.timerThread.timerFinished.disconnect(self.concludeCounter)
            self.timerThread.timerError.disconnect(self.cancelCounter)
        except:
            pass
        self.timerThread = None
        self.startCounterButton.setDisabled(False)
        self.stopCounterButton.setDisabled(True)

    def concludeCounter(self, result):
        # clean up timer thread stuff
        self.timerThread.stop()
        try:
            self.timerThread.timerFinished.disconnect(self.concludeCounter)
            self.timerThread.timerError.disconnect(self.cancelCounter)
        except:
            pass
        self.timerThread = None
        self.startCounterButton.setDisabled(False)
        self.stopCounterButton.setDisabled(True)
        # do something with the results
        self.iface.messageBar().pushMessage("Info", "The counter results: %s" % result, level=0, duration=5)


class TimedEvent(QtCore.QThread):
    timerFinished = QtCore.pyqtSignal(list)
    timerProgress = QtCore.pyqtSignal(int)
    timerError = QtCore.pyqtSignal()

    def __init__(self, parentThread, parentObject, bridges):
        QtCore.QThread.__init__(self, parentThread) 
        self.parent = parentObject
        self.bridges = bridges
        self.running = False

    def run(self):
        # set the process running
        self.running = True
        #
        progress = 0
        recorded = []
        for bridge in self.bridges:
            jump = 3
            recorded.append(jump)
            print bridge
            # wait for the number of seconds/5 (just to speed it up)
            time.sleep(jump)
            progress += jump
            self.timerProgress.emit(progress)
            # if it has been cancelled, stop the process
            if not self.running:
                return
        self.timerFinished.emit(recorded)

    def stop(self):
        self.running = False
        self.exit()