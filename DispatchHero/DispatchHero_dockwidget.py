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

import os, time, logging

from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import *
from PyQt4.QtCore import QThread, QVariant
from . import utility_functions as uf
from qgis.core import *
import processing

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'spatial_decision_dockwidget_base_extra.ui'))

# global variables

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
        self.openingRoads = []

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

        # assigning the layer with roadnetwork
        for layer in self.iface.legendInterface().layers():
            if layer.name() == u'bridges':
                self.bridgesLayer = layer
            elif layer.name() == u'roads':
                self.roadsLayer = layer

    def showBridges(self, bridgeTime):

        # setup vairables
        bridge_ids = bridgeTime[0]
        bridge_time = bridgeTime[1]

        # creating query for the open bridges
        query = """"id" = '{}'""".format(bridge_ids[0])
        if len(bridge_ids) > 1:
            for b in bridge_ids[1:]:
                query += """ or "id" = '{}'""".format(b)

        # adding the open bridges to the log
        for b in bridge_ids:
            log = '{}: {}'.format(bridge_time[11:], b[:12])
            self.bridgesList.addItem(log)

        # creating a selection of open bridges, and all bridges
        selection = self.bridgesLayer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        features = self.bridgesLayer.getFeatures()

        # start editting the layers
        self.bridgesLayer.startEditing()
        self.roadsLayer.startEditing()

        # now first close the bridges that were previously open
        if len(self.openingRoads) == 0:
            pass
        else:
            query = """"sid" = {}""".format(self.openingRoads[0])
            if len(self.openingRoads) > 1:
                for road in self.openingRoads[1:]:
                    query += """ or "sid" = '{}'""".format(road)
            road_selection = self.roadsLayer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
            for road in road_selection:
                self.roadsLayer.changeAttributeValue(road.id(), 1, 1)

        # cleaning the list, for next open bridges
        self.openingRoads = []

        # close all bridges to open correct ones
        for feature in features:
            self.bridgesLayer.changeAttributeValue(feature.id(), 2, 'closed')

        # go through open bridges and update existing road network for availability
        for feature in selection:
            self.bridgesLayer.changeAttributeValue(feature.id(), 2, 'open')
            sid = feature.attributes()[0]
            self.openingRoads.append(int(sid))

            # updating the road network
            closing_roads = self.roadsLayer.getFeatures(QgsFeatureRequest().setFilterExpression('"sid" = {}'.format(sid)))
            for road in closing_roads:
                self.roadsLayer.changeAttributeValue(road.id(), 1, 0)

        # committing the changes to the layers
        self.bridgesLayer.commitChanges()
        self.roadsLayer.commitChanges()

    def startCounter(self):
        # prepare the thread of the timed even or long loop
        new_file = QtGui.QFileDialog.getOpenFileName(self, "", os.path.dirname(os.path.abspath(__file__)))
        fh = open(new_file, 'r')
        self.bridgesGenerator = uf.BridgeParser(fh)
        self.bridgesGenerator.parse()
        self.timerThread = TimedEvent(self.iface.mainWindow(), self, self.bridgesGenerator.generator())
        self.timerThread.timerFinished.connect(self.concludeCounter)
        self.timerThread.timerError.connect(self.cancelCounter)
        self.timerThread.displayBridges.connect(self.showBridges)
        self.timerThread.start()
        # from here the timer is running in the background on a separate thread. user can continue working on QGIS.
        self.startCounterButton.setDisabled(True)
        self.stopCounterButton.setDisabled(False)

    def cancelCounter(self):
        # triggered if the user clicks the cancel button
        
        # resetting the roads to available again
        self.roadsLayer.startEditing()
        for feature in self.roadsLayer.getFeatures(QgsFeatureRequest().setFilterExpression('"available" = 0')):
            self.roadsLayer.changeAttributeValue(feature.id(), 1, 1)
        self.roadsLayer.commitChanges()

        # stop the thread
        self.timerThread.stop()
        try:
            self.timerThread.timerFinished.disconnect(self.concludeCounter)
            self.timerThread.timerError.disconnect(self.cancelCounter)
            self.timerThread.displayBridges.disconnect(self.showBridges)
        except:
            pass
        self.timerThread = None
        self.startCounterButton.setDisabled(False)
        self.stopCounterButton.setDisabled(True)
        self.iface.messageBar().pushMessage("Info", "Simulation canceled", level=0, duration=8)

    def concludeCounter(self, result):
        # clean up timer thread stuff

        # resetting the roads to available again
        self.roadsLayer.startEditing()
        for feature in self.roadsLayer.getFeatures(QgsFeatureRequest().setFilterExpression('"available" = 0')):
            self.roadsLayer.changeAttributeValue(feature.id(), 1, 1)
        self.roadsLayer.commitChanges()

        # stop the thread
        self.timerThread.stop()
        try:
            self.timerThread.timerFinished.disconnect(self.concludeCounter)
            self.timerThread.timerError.disconnect(self.cancelCounter)
            self.timerThread.displayBridges.disconnect(self.showBridges)
        except:
            pass
        self.timerThread = None
        self.startCounterButton.setDisabled(False)
        self.stopCounterButton.setDisabled(True)
        # do something with the results
        self.iface.messageBar().pushMessage("Info", "Simulation finished", level=0, duration=8)


class TimedEvent(QtCore.QThread):
    timerFinished = QtCore.pyqtSignal(list)
    timerProgress = QtCore.pyqtSignal(int)
    timerError = QtCore.pyqtSignal()
    displayBridges = QtCore.pyqtSignal(tuple)

    def __init__(self, parentThread, parentObject, bridges):
        QtCore.QThread.__init__(self, parentThread)
        self.parent = parentObject
        self.bridges = bridges
        self.running = False

    def run(self):
        self.running = True
        progress = 0
        recorded = []
        for bridgeTime in self.bridges:
            jump = 20
            recorded.append(jump)
            
            self.displayBridges.emit(bridgeTime)

            time.sleep(jump)
            progress += jump
            self.timerProgress.emit(progress)
            if not self.running:
                return
        self.timerFinished.emit(recorded)

    def stop(self):
        self.running = False
        self.exit()


class TimedVesselEvent(QtCore.QThread):
    timerFinished = QtCore.pyqtSignal(list)
    timerProgress = QtCore.pyqtSignal(int)
    timerError = QtCore.pyqtSignal()

    def __init__(self, parentThread, parentObject, bridges):
        QtCore.QThread.__init__(self, parentThread)
        self.parent = parentObject
        self.bridges = bridges
        self.running = False

    def run(self):
        self.running = True
        progress = 0
        recorded = []
        for bridgeTime in self.bridges:
            jump = 10
            recorded.append(jump)
            time.sleep(jump)
            progress += jump
            self.timerProgress.emit(progress)
            if not self.running:
                return
        self.timerFinished.emit(recorded)

    def stop(self):
        self.running = False
        self.exit()