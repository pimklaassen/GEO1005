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

import os, time, logging, math
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import QCursor, QPixmap, QColor
from PyQt4.QtCore import QThread, QVariant
from . import utility_functions as uf
from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.core import *
import processing
from qgis.networkanalysis import *
from . import globvars

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'DispatchHero_dockwidget_base.ui'))

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

        #set up variables
        global Polygon
        Polygon = False
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.openingRoads = []
        self.states = {}
        self.speed = 1

        # setup Decisions interface
        self.Add_message.clicked.connect(self.add_message_alert)

        self.Route1.clicked.connect(self.select_route_1)
        self.Route2.clicked.connect(self.select_route_2)
        self.Route3.clicked.connect(self.select_route_3)

        self.Add_truck.clicked.connect(self.add_truck_instance)
        self.Delete_truck.clicked.connect(self.delete_truck_instance)

        self.Auto_ON.clicked.connect(self.autoOn)
        self.Auto_OFF.clicked.connect(self.autoOff)

        self.Stop.clicked.connect(self.cancelSelection)

        self.Help.clicked.connect(self.request_help)

        # set up GUI operation signals
        self.importDataButton.clicked.connect(self.importData)

        self.drawPolygonButton.clicked.connect(self.drawPolygon)

        self.startCounterButton.clicked.connect(self.startCounter)
        self.stopCounterButton.clicked.connect(self.cancelCounter)
        self.spinBox.setMaximum(20)
        self.spinBox.setMinimum(0)
        self.spinBox.setValue(5)

        self.startCounterButton.setDisabled(True)
        self.stopCounterButton.setDisabled(True)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def setSpeed(self):
        self.speed = 1 * self.spinBox.value()

    def drawPolygon(self, LayerPoint = (-1,-1)):
        global Polygon
        if Polygon == False:
            Polygon = True
        else:
            Polygon = False
        global polygonlist
        polygonlist = []

#################################################################################################################

    def request_help(self):
        self.Message_display.clear()
        self.Message_display.addItem("----------------------------------")
        self.Message_display.addItem("Station full")
        self.Message_display.addItem("----------------------------------")

    def autoOn(self):
        self.Message_display.clear()
        self.Message_display.addItem("----------------------------------")
        self.Message_display.addItem("AutoDispatch ON")
        self.Message_display.addItem("----------------------------------")

    def autoOff(self):
        self.Message_display.clear()
        self.Message_display.addItem("----------------------------------")
        self.Message_display.addItem("AutoDispatch OFF")
        self.Message_display.addItem("----------------------------------")

    def cancelSelection(self):
        self.Message_display.clear()
        car = self.Trucks_in_route.currentItem().text()
        name = "car" + car + ".txt"
        file = open(name, 'r')
        with file:
            for line in file:
                self.Message_display.addItem(line)

        file = open(name, 'a')
        self.Message_display.addItem("----------------------------------")
        file.write("----------------------------------\n")
        Truck = self.Trucks_in_route.currentItem().text()
        self.Message_display.addItem(Truck)
        file.write(Truck + "\n")
        self.Message_display.addItem("Cancel route\n")
        file.write("Cancel route\n")
        self.Message_display.addItem("----------------------------------")
        file.write("----------------------------------\n")
        self.In_station_list.addItem(Truck)
        self.Trucks_in_route.takeItem(self.Trucks_in_route.currentRow())
        pass

    def addlist_routes(self):
        self.Routes.addItem(self.Route_name.text())
        self.Route_name.setText('')
        self.Route_name.setFocus()
        pass

    def add_message_alert(self):
        self.Message_display.clear()
        car = self.Trucks_in_route.currentItem().text()
        name = "car"+ car + ".txt"
        file = open(name,'r')
        with file:
            for line in file:
                self.Message_display.addItem(line)

        file = open(name, 'a')
        self.Message_display.addItem("----------------------------------")
        file.write("----------------------------------\n")
        Truck = self.Trucks_in_route.currentItem().text()
        self.Message_display.addItem(Truck)
        file.write(Truck+"\n")
        self.Message_display.addItem(self.Route_message.text())
        file.write(self.Route_message.text()+ "\n")
        self.Message_display.addItem("----------------------------------")
        file.write("----------------------------------\n")
        self.Route_message.setText('')
        self.Route_message.setFocus()
        file.close
        pass

    def select_route_1(self):
        if self.Reassign.isChecked() == True:
            self.Message_display.clear()
            Truck = self.Trucks_in_route.currentItem().text()
            name = "car" + Truck + ".txt"
            file = open(name, 'w')
            self.Message_display.addItem("----------------------------------")
            self.Message_display.addItem(Truck)
            self.Message_display.addItem("Reassigned route 1")
            self.Message_display.addItem("----------------------------------")
            file.write("----------------------------------\n")
            file.write(Truck + "\n")
            file.write("Reassigned route 1\n")
            file.write("----------------------------------\n")
        else:
            self.Message_display.clear()
            Truck = self.In_station_list.currentItem().text()
            name = "car" + Truck + ".txt"
            file = open(name, 'w')
            self.Message_display.addItem("----------------------------------")
            self.Trucks_in_route.addItem(Truck)
            self.Message_display.addItem(Truck)
            self.Message_display.addItem("Follow route 1")
            self.Message_display.addItem("----------------------------------")
            file.write("----------------------------------\n")
            file.write(Truck + "\n")
            file.write("Follow route 1\n")
            file.write("----------------------------------\n")
            self.In_station_list.takeItem(self.In_station_list.currentRow())
        pass

    def select_route_2(self):
        if self.Reassign.isChecked() == True:
            self.Message_display.clear()
            Truck = self.Trucks_in_route.currentItem().text()
            name = "car" + Truck + ".txt"
            file = open(name, 'w')
            self.Message_display.addItem("----------------------------------")
            self.Message_display.addItem(Truck)
            self.Message_display.addItem("Reassigned route 2")
            self.Message_display.addItem("----------------------------------")
            file.write("----------------------------------\n")
            file.write(Truck + "\n")
            file.write("Reassigned route 2\n")
            file.write("----------------------------------\n")
        else:
            self.Message_display.clear()
            Truck = self.In_station_list.currentItem().text()
            name = "car" + Truck + ".txt"
            file = open(name, 'w')
            self.Message_display.addItem("----------------------------------")
            self.Trucks_in_route.addItem(Truck)
            self.Message_display.addItem(Truck)
            self.Message_display.addItem("Follow route 2")
            self.Message_display.addItem("----------------------------------")
            file.write("----------------------------------\n")
            file.write(Truck + "\n")
            file.write("Follow route 2\n")
            file.write("----------------------------------\n")
            self.In_station_list.takeItem(self.In_station_list.currentRow())
        pass

    def select_route_3(self):
        if self.Reassign.isChecked() == True:
            self.Message_display.clear()
            Truck = self.Trucks_in_route.currentItem().text()
            name = "car" + Truck + ".txt"
            file = open(name, 'w')
            self.Message_display.addItem("----------------------------------")
            self.Message_display.addItem(Truck)
            self.Message_display.addItem("Reassigned route 3")
            self.Message_display.addItem("----------------------------------")
            file.write("----------------------------------\n")
            file.write(Truck + "\n")
            file.write("Reassigned route 3\n")
            file.write("----------------------------------\n")
        else:
            self.Message_display.clear()
            Truck = self.In_station_list.currentItem().text()
            name = "car" + Truck + ".txt"
            file = open(name, 'w')
            self.Message_display.addItem("----------------------------------")
            self.Trucks_in_route.addItem(Truck)
            self.Message_display.addItem(Truck)
            self.Message_display.addItem("Follow route 3")
            self.Message_display.addItem("----------------------------------")
            file.write("----------------------------------\n")
            file.write(Truck + "\n")
            file.write("Follow route 3\n")
            file.write("----------------------------------\n")
            self.In_station_list.takeItem(self.In_station_list.currentRow())
        pass

    def add_truck_instance(self):
        self.In_station_list.addItem(self.Truck_text.text())
        self.Truck_text.setText('')

    def delete_truck_instance(self):
        self.In_station_list.takeItem(self.In_station_list.currentRow())
        pass

###################################################################################################

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

        for br in self.bridgesLayer.getFeatures():
            attrs = br.attributes()
            br = attrs[1]
            tr = attrs[2]
            self.states[br] = tr
        
        self.resetLayers()
        self.startCounterButton.setDisabled(False)

    def resetLayers(self):
        self.bridgesLayer.startEditing()
        for br in self.bridgesLayer.getFeatures():
            attrs = br.attributes()
            self.bridgesLayer.changeAttributeValue(br.id(), 2, 'closed')
        self.bridgesLayer.commitChanges()

        self.roadsLayer.startEditing()
        query = '"available" = 0'
        for br in self.roadsLayer.getFeatures(QgsFeatureRequest().setFilterExpression(query)):
            attrs = br.attributes()
            self.roadsLayer.changeAttributeValue(br.id(), 1, 1)
        self.roadsLayer.commitChanges()

    def logVessels(self, vesselTime):
        obj = vesselTime[0]

        # set conditional to ship
        if obj['speed'] <= 5:
            return
        if obj['length'] < 80:
            return

        # condition passed, assign the bridge
        pending_bridge = 'Erasmusbrug'\
        if (obj['brige'] == 'erasmus')\
        else 'GRT02_9de96a85-078b-4954-82ad-3bec2e22a75b'

        # selecting the bridge
        query_bridge = """"id" = '{}'""".format(pending_bridge)
        features = self.bridgesLayer.getFeatures(QgsFeatureRequest().setFilterExpression(query_bridge))

        # iterate through selection
        for feat in features:
            status = feat.attributes()[2]
            bridge_road = feat.attributes()[0]

            # check if bridge is open, if so, return (because already red)
            if status == 'open':
                return

            # now change the layers
            self.bridgesLayer.startEditing()
            self.bridgesLayer.changeAttributeValue(feat.id(), 2, 'pending')
            self.bridgesLayer.commitChanges()

            # and for the roads
            query = '"sid" = {}'.format(bridge_road)
            self.roadsLayer.startEditing()
            for road in self.roadsLayer.getFeatures(QgsFeatureRequest().setFilterExpression(query)):
                self.roadsLayer.changeAttributeValue(road.id(), 1, 2)
            self.roadsLayer.commitChanges()

        self.pendingList = []
        self.pendingList.append(obj['name'])

        log = '{} will open for {}'.format(pending_bridge, obj['name'])
        self.trucksList.addItem(log)

    def showBridges(self, bridgeTime):

        # setup vairables
        bridge_ids = bridgeTime[0]
        bridge_time = bridgeTime[1]

        # creating query for the open bridges
        query_init = """"id" = '{}'""".format(bridge_ids[0])
        if len(bridge_ids) > 1:
            for b in bridge_ids[1:]:
                query_init += """ or "id" = '{}'""".format(b)

        # adding the open bridges to the log
        for b in bridge_ids:
            log = '{}: {}'.format(bridge_time[11:], b[:12])
            self.bridgesList.addItem(log)

        # creating a selection of open bridges, and all bridges
        selection = self.bridgesLayer.getFeatures(QgsFeatureRequest().setFilterExpression(query_init))
        features = self.bridgesLayer.getFeatures()

        # start editting the layers
        self.bridgesLayer.startEditing()
        self.roadsLayer.startEditing()

        # now first close the roads that were previously open
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

        # go through previous open roads, to detect change
        new = []

        for feature in selection:
            sid = feature.attributes()[0]
            new.append(sid)

        check = []

        if len(self.openingRoads) != len(new):
            globvars.changes = True
        else:
            for sid_1, sid_2 in zip(self.openingRoads, new):
                if sid_1 == int(sid_2):
                    check.append(True)
                else:
                    check.append(False)

            print check, self.openingRoads, new

            if not all(check):
                globvars.changes = True
            else:
                globvars.changes = False

        # make new generator object
        selection = self.bridgesLayer.getFeatures(QgsFeatureRequest().setFilterExpression(query_init))

        # cleaning the list, for next open bridges
        self.openingRoads = []

        # close all bridges to open correct ones
        for feature in features:
            if feature.attributes()[2] == 'pending':
                continue
            self.bridgesLayer.changeAttributeValue(feature.id(), 2, 'closed')
            self.states[feature.attributes()[2]] = 'closed'

        # go through open bridges and update existing road network for availability
        for feature in selection:
            self.bridgesLayer.changeAttributeValue(feature.id(), 2, 'open')
            self.states[feature.attributes()[2]] = 'open'
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
        self.setSpeed()
        new_file = QtGui.QFileDialog.getOpenFileName(self, "", os.path.dirname(os.path.abspath(__file__)))
        fh = open(new_file, 'r')
        self.bridgesGenerator = uf.BridgeParser(fh)
        self.bridgesGenerator.parse()
        self.timerThread = TimedEvent(self.iface.mainWindow(), self, self.bridgesGenerator.generator())
        self.timerThread.timerFinished.connect(self.concludeCounter)
        self.timerThread.timerError.connect(self.cancelCounter)
        self.timerThread.displayBridges.connect(self.showBridges)

        new_file = QtGui.QFileDialog.getOpenFileName(self, "", os.path.dirname(os.path.abspath(__file__)))
        fh = open(new_file, 'r')
        self.vesselGenerator = uf.vesselParser(fh)
        self.vesselGenerator.parse()
        self.vesselThread = TimedVesselEvent(self.iface.mainWindow(), self, self.vesselGenerator.generator())
        self.vesselThread.timerFinished.connect(self.concludeCounter)
        self.vesselThread.timerError.connect(self.cancelCounter)
        self.vesselThread.displayVessels.connect(self.logVessels)

        self.timerThread.start()
        self.vesselThread.start()
        # from here the timer is running in the background on a separate thread. user can continue working on QGIS.
        self.startCounterButton.setDisabled(True)
        self.stopCounterButton.setDisabled(False)
        self.spinBox.setDisabled(True)

    def cancelCounter(self):
        # triggered if the user clicks the cancel button
        
        # resetting the roads to available again
        self.roadsLayer.startEditing()
        for feature in self.roadsLayer.getFeatures(QgsFeatureRequest().setFilterExpression('"available" = 0')):
            self.roadsLayer.changeAttributeValue(feature.id(), 1, 1)
        self.roadsLayer.commitChanges()

        # stop the thread
        self.timerThread.stop()
        self.vesselThread.stop()
        try:
            self.timerThread.timerFinished.disconnect(self.concludeCounter)
            self.timerThread.timerError.disconnect(self.cancelCounter)
            self.timerThread.displayBridges.disconnect(self.showBridges)

            self.vesselThread.timerFinished.disconnect(self.concludeCounter)
            self.vesselThread.timerError.disconnect(self.cancelCounter)
            self.vesselThread.displayVessels.diconnect(self.logVessels)
        except:
            pass
        self.timerThread = None
        self.startCounterButton.setDisabled(False)
        self.stopCounterButton.setDisabled(True)
        self.resetLayers()
        self.bridgesList.clear()
        self.trucksList.clear()
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
        self.vesselThread.stop()
        try:
            self.timerThread.timerFinished.disconnect(self.concludeCounter)
            self.timerThread.timerError.disconnect(self.cancelCounter)
            self.timerThread.displayBridges.disconnect(self.showBridges)

            self.vesselThread.timerFinished.disconnect(self.concludeCounter)
            self.vesselThread.timerError.disconnect(self.cancelCounter)
            self.vesselThread.displayVessels.diconnect(self.logVessels)
        except:
            pass
        self.timerThread = None
        self.startCounterButton.setDisabled(False)
        self.stopCounterButton.setDisabled(True)
        self.spinBox.setDisabled(False)
        self.resetLayers()
        self.bridgesList.clear()
        self.trucksList.clear()
        # do something with the results
        self.iface.messageBar().pushMessage("Info", "Simulation finished", level=0, duration=8)


class MapTool(QgsMapTool):
    def __init__(self, canvas):
        super(QgsMapTool, self).__init__(canvas)
        self.canvas = canvas
        self.cursor = QCursor(Qt.CrossCursor)
        self.rubberBandPolyline = QgsRubberBand(self.canvas, False)
        self.rubberBandPolygon = QgsRubberBand(self.canvas, True)
        self.rubberBandPath2 = QgsRubberBand(self.canvas, False)
        self.rubberBandPath3 = QgsRubberBand(self.canvas, False)
        self.rubberBandPath1 = QgsRubberBand(self.canvas, False)
        #for the shortest path
        self.graph = QgsGraph()
        self.tied_points = []
        self.firestation_coord = (92619.8,436539)
        globvars.changes = True
        self.init_names = False
        #clean the canvas - !!! to be fixed !!!
        print 'initiated maptool'

    def activate(self):
        self.canvas.setCursor(self.cursor)

    def screenToLayerCoords(self, screenPos, layer):

        transform = self.canvas.getCoordinateTransform()
        canvasPoint = QgsMapToPixel.toMapCoordinates(transform,
                                                     screenPos.x(),
                                                     screenPos.y())

        # Transform if required
        layerEPSG = layer.crs().authid()
        projectEPSG = self.canvas.mapRenderer().destinationCrs().authid()
        if layerEPSG != projectEPSG:
            renderer = self.canvas.mapRenderer()
            layerPoint = renderer.mapToLayerCoordinates(layer,
                                                        canvasPoint)
        else:
            layerPoint = canvasPoint

        # Convert this point (QgsPoint) to a QgsGeometry
        return QgsGeometry.fromPoint(layerPoint)

    def canvasReleaseEvent(self, mouseEvent):
        """
        Each time the mouse is clicked on the map canvas, perform
        the following tasks:
            Loop through all visible vector layers and for each:
                Ensure no features are selected
                Determine the distance of the closes feature in the layer to the mouse click
                Keep track of the layer id and id of the closest feature
            Select the id of the closes feature
        """
        print 'detected release'
        for layer in self.canvas.layers():
            if layer.name() == 'roads':
                self.activelayer = layer
        if Polygon == True:
                LayerPoint = self.toLayerCoordinates(self.activelayer, mouseEvent.pos())
                polygonlist.append(LayerPoint)
                if len(polygonlist)==1:
                    pass
                if len(polygonlist)==2:
                    points = polygonlist
                    ptstoadd = []
                    for point in points:
                        ptstoadd.append(QgsPoint(point[0], point[1]))
                    self.rubberBandPolyline.setToGeometry(QgsGeometry.fromPolyline(ptstoadd), None)
                    self.rubberBandPolyline.setColor(QColor(200, 50, 50))
                    self.rubberBandPolyline.setWidth(10)
                if len(polygonlist)>2:
                    self.canvas.scene().removeItem(self.rubberBandPolyline)
                    points = polygonlist
                    ptstoadd = []
                    for point in points:
                        ptstoadd.append(QgsPoint(point[0], point[1]))
                    self.rubberBandPolygon.setToGeometry(QgsGeometry.fromPolygon([ptstoadd]), None)
                    self.rubberBandPolygon.setBorderColor(QColor(200,50,50))
                    self.rubberBandPolygon.setWidth(10)

        if Polygon == False:
            # Determine the location of the click in real-world coords
            self.destination = self.toLayerCoordinates(self.activelayer, mouseEvent.pos())

            #shortest path algorythm
            if globvars.changes == True:
                print "changes detected, rebuilds network"
                globvars.changes = False
                self.buildNetwork()
            if self.graph and self.tied_points:
                path1, path2, path3 = self.calculateRoute()
            #change the zoom setting
            all_paths = path1 + path2 + path3
            x_max = float("-inf")
            x_min = float("inf")
            y_max = float("-inf")
            y_min = float("inf")
            for coord in all_paths:
                if coord[0] > x_max:
                    x_max = coord[0]
                if coord[0] < x_min:
                    x_min = coord[0]
                if coord[1] > y_max:
                    y_max = coord[1]
                if coord[1] < y_min:
                    y_min = coord[1]
            zoomextent = (x_min, y_min, x_max, y_max)
            #self.adaptzoom(zoomextent)

    """def adaptzoom(self, zoomextent):
        self.canvas.zoomToExtent(QgsRectangle(zoomextent))
        self.canvas.refresh()
        print "frozen canvas?", DispatchHeroDockWidget.canvas.isFrozen()"""

    def buildNetwork(self):
        #the first time the network is built, the layers need to be found basing on their names
        if self.init_names == False:
            for layer in self.canvas.layers():
                if layer.name() == 'roads':
                    self.network_layer_original = layer
            for layer in self.canvas.layers():
                if layer.name() == 'roads copy':
                    self.network_layer = layer
            for layer in self.canvas.layers():
                if layer.name() == 'graph tie points':
                    self.sourcepoint_layer = layer
        #each time the network is built, the open bridges need to be removed from the copy and the bridges which closed added again
        list_to_reset = []
        list_build = []
        for feature in self.network_layer.getFeatures():
            list_to_reset.append(feature.id())
        res1 = self.network_layer.dataProvider().deleteFeatures(list_to_reset)
        for feature in self.network_layer_original.getFeatures(
                QgsFeatureRequest().setFilterExpression('"available" = 1')):
            list_build.append(feature)
        res2, added_points = self.network_layer.dataProvider().addFeatures(list_build)
        if self.network_layer:
            # get the points to be used as origin and destination
            # in this case gets the centroid of the selected features
            self.source_points = []
            for f in self.sourcepoint_layer.getFeatures():
                coord = (f.attribute('X'), f.attribute('Y'))
                self.source_points.append(QgsPoint(coord[0], coord[1]))
            # build the graph including these points
            if len(self.source_points) > 1:
                self.graph, self.tied_points = uf.makeUndirectedGraph(self.network_layer, self.source_points)
                # the tied points are the new source_points on the graph
                if self.graph and self.tied_points:
                    text = "network is built for %s points" % len(self.tied_points)
            shortestdistance = float("inf")
            #here the closest tied_point to the firestation is identified
            if self.init_names == False:
                for point in self.tied_points:
                    sqrdist = (point[0]-self.firestation_coord[0])**2 + (point[1]-self.firestation_coord[1])**2
                    if sqrdist < shortestdistance:
                        shortestdistance = sqrdist
                        self.closestpoint_start = point
            self.origin_index = self.tied_points.index(self.closestpoint_start)
            self.init_names = True
        return

    def calculateRoute(self):
        # origin and destination must be in the set of tied_points
        shortestdistance = float("inf")
        for point in self.tied_points:
            sqrdist = (point[0] - self.destination[0])**2 + (point[1] - self.destination[1])**2
            if sqrdist<shortestdistance:
                shortestdistance = sqrdist
                self.closestpoint_end = point
        self.destination_index = self.tied_points.index(self.closestpoint_end)
        options = len(self.tied_points)
        if options > 1:
            # calculate the shortest path for the given origin and destination
            path = uf.calculateRouteDijkstra(self.graph, self.tied_points, self.origin_index, self.destination_index)
            #display the route
            if len(path) > 1:
                ptstoadd = []
                for point in path:
                    ptstoadd.append(QgsPoint(point[0], point[1]))
                self.rubberBandPath1.setToGeometry(QgsGeometry.fromPolyline(ptstoadd), None)
                self.rubberBandPath1.setColor(QColor(128, 255, 0))
                self.rubberBandPath1.setWidth(3)
            #determine via points for the alternative routings
            if path:
                self.x_diff = self.firestation_coord[0] - self.destination[0]
                self.y_diff = self.firestation_coord[1] - self.destination[1]
                self.eucl_distance = math.sqrt(self.x_diff ** 2 + self.y_diff ** 2)
                if self.eucl_distance < 1000:
                    factor = 2
                elif self.eucl_distance < 3000:
                    factor = 1
                elif self.eucl_distance < 6000:
                    factor = 0.5
                else:
                    factor = 0.25
                new_point1_x = (self.firestation_coord[0]+self.destination[0])/2+self.y_diff*factor
                new_point1_y = (self.firestation_coord[1]+self.destination[1])/2-self.x_diff*factor
                new_point2_x = (self.firestation_coord[0]+self.destination[0])/2-self.y_diff*factor
                new_point2_y = (self.firestation_coord[1]+self.destination[1])/2+self.x_diff*factor
                self.via_points = [(new_point1_x,new_point1_y), (new_point2_x, new_point2_y)]
                #determine the alternative roude node_points which have a crossing
                self.via_tied_points_index = []
                for via in self.via_points:
                    shortestdistance = float("inf")
                    for crosspoint in self.sourcepoint_layer.getFeatures():
                        if crosspoint.attribute('crossing') == 1:
                            sqrdist = (via[0]-crosspoint.attribute('X'))**2 + (via[1]-crosspoint.attribute('Y'))**2
                            if sqrdist < shortestdistance:
                                shortestdistance = sqrdist
                                via_point_coord = (crosspoint.attribute('X'), crosspoint.attribute('Y'))
                    if via_point_coord:
                        lowestdiff = float("inf")
                        for point in self.tied_points:
                            diff = (round(via_point_coord[0],1) - round(point[0],1))**2 + (round(via_point_coord[1],1) - round(point[1],1))**2
                            if diff < lowestdiff:
                                lowestdiff = diff
                                lowestdiff_point = point
                        if lowestdiff_point:
                            via_point_index = self.tied_points.index(lowestdiff_point)
                            self.via_tied_points_index.append(via_point_index)
                #calculate the alternative routes
                display_indicator = 2
                alt_path = dict()
                for via_index in self.via_tied_points_index:
                    alt_path1 = uf.calculateRouteDijkstra(self.graph, self.tied_points, self.origin_index, via_index)
                    alt_path2 = uf.calculateRouteDijkstra(self.graph, self.tied_points, via_index, self.destination_index)
                    if len(alt_path1)>1 and len(alt_path2)>1:
                        alt_path[display_indicator] = alt_path1+alt_path2
                    ptstoadd = []
                    for point in alt_path[display_indicator]:
                        ptstoadd.append(QgsPoint(point[0], point[1]))
                #display the alternative route layers and adapt the zoom
                    if display_indicator == 2:
                        self.rubberBandPath2.setToGeometry(QgsGeometry.fromPolyline(ptstoadd), None)
                        self.rubberBandPath2.setColor(QColor(51, 160, 0))
                        self.rubberBandPath2.setWidth(3)
                    if display_indicator == 3:
                        self.rubberBandPath3.setToGeometry(QgsGeometry.fromPolyline(ptstoadd), None)
                        self.rubberBandPath3.setColor(QColor(102, 51, 0))
                        self.rubberBandPath3.setWidth(3)
                    display_indicator +=1
        return path, alt_path[2], alt_path[3]

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
            jump = 20 / self.parent.speed
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
    displayVessels = QtCore.pyqtSignal(tuple)

    def __init__(self, parentThread, parentObject, vessels):
        QtCore.QThread.__init__(self, parentThread)
        self.parent = parentObject
        self.vessels = vessels
        self.running = False

    def run(self):
        self.running = True
        progress = 0
        recorded = []
        for vesselTime in self.vessels:
            
            jump = vesselTime[1] / self.parent.speed
            recorded.append(jump)
            self.displayVessels.emit(vesselTime)

            time.sleep(jump)
            progress += jump
            self.timerProgress.emit(progress)
            if not self.running:
                return
        self.timerFinished.emit(recorded)

    def stop(self):
        self.running = False
        self.exit()