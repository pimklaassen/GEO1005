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

import os, threading, time, math

from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import *
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'spatial_decision_dockwidget_base_extra.ui'))

## added map tools
from qgis.gui import QgsMapTool, QgsRubberBand, QgsVertexMarker
from qgis.core import QgsMapLayer, QgsMapToPixel, QgsFeature, QgsFeatureRequest, QgsGeometry, QgsPoint
from PyQt4.QtGui import QCursor, QPixmap, QColor
from PyQt4.QtCore import Qt
#for the shortest path calculations
from qgis.networkanalysis import *
#shortest path
from . import utility_functions as uf


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

        #setup variables
        self.iface = iface
        self.canvas = self.iface.mapCanvas()

        # set up GUI operation signals
        self.importDataButton.clicked.connect(self.importData)

        #self.calcShortestPath.clicked.connect(self.getCanvasLayers)
        self.drawPolygonButton.clicked.connect(self.drawPolygon)

        #set up variables
        global Polygon
        Polygon = False

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def importData(self, filename=''):
        new_file = QtGui.QFileDialog.getOpenFileName(self, "", os.path.dirname(os.path.abspath(__file__)))
        if new_file:
            self.iface.addProject(unicode(new_file))
        return new_file

    def drawPolygon(self, LayerPoint = (-1,-1)):
        global Polygon
        if Polygon == False:
            Polygon = True
        else:
            Polygon = False
        global polygonlist
        polygonlist = []

class NearestFeatureMapTool(QgsMapTool):
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
        self.changes = True  #to be set by the thread when data read changes!!!
        self.origin_init = False
        #clean the canvas - !!! to be fixed !!!

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
        for layer in self.canvas.layers():
            if layer.name() == 'Rotterdam roads':
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
                    self.rubberBandPolyline.setColor(QColor(255, 0, 0))
                    self.rubberBandPolyline.setWidth(10)
                if len(polygonlist)>2:
                    self.canvas.scene().removeItem(self.rubberBandPolyline)
                    points = polygonlist
                    ptstoadd = []
                    for point in points:
                        ptstoadd.append(QgsPoint(point[0], point[1]))
                    self.rubberBandPolygon.setToGeometry(QgsGeometry.fromPolygon([ptstoadd]), None)
                    self.rubberBandPolygon.setBorderColor(QColor(255,0,0))
                    self.rubberBandPolygon.setWidth(10)

        if Polygon == False:
            # Determine the location of the click in real-world coords
            self.destination = self.toLayerCoordinates(self.activelayer, mouseEvent.pos())

            #shortest path algorythm
            if self.changes == True:
                self.buildNetwork()
                self.changes = False
            if self.graph and self.tied_points:
                self.calculateRoute()
            return

    def buildNetwork(self):
        for layer in self.canvas.layers():
            if layer.name() == 'Rotterdam roads':
                self.network_layer = layer
        for layer in self.canvas.layers():
            if layer.name() == 'graph tie points':
                self.sourcepoint_layer = layer
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
            if self.origin_init == False:
                for point in self.tied_points:
                    sqrdist = (point[0]-self.firestation_coord[0])**2 + (point[1]-self.firestation_coord[1])**2
                    if sqrdist < shortestdistance:
                        shortestdistance = sqrdist
                        self.closestpoint_start = point
            self.origin_index = self.tied_points.index(self.closestpoint_start)
            self.origin_init = True
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
                print self.eucl_distance
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
                                via_point_coord = (round(crosspoint.attribute('X'), 1), round(crosspoint.attribute('Y'), 0))
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
                #display the alternative route layers
                    if display_indicator == 2:
                        self.rubberBandPath2.setToGeometry(QgsGeometry.fromPolyline(ptstoadd), None)
                        self.rubberBandPath2.setColor(QColor(51, 102, 0))
                        self.rubberBandPath2.setWidth(3)
                    if display_indicator == 3:
                        self.rubberBandPath3.setToGeometry(QgsGeometry.fromPolyline(ptstoadd), None)
                        self.rubberBandPath3.setColor(QColor(102, 51, 0))
                        self.rubberBandPath3.setWidth(3)
                    display_indicator +=1
        return path, alt_path[2], alt_path[3]