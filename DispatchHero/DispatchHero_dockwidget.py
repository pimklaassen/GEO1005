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

import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal

import os, threading, time

from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtCore import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'DispatchHero_dockwidget_base.ui'))

from qgis.utils import iface

## added map tools
from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.core import QgsMapLayer, QgsMapToPixel, QgsFeature, QgsFeatureRequest, QgsGeometry, QgsPoint
from PyQt4.QtGui import QCursor, QPixmap, QColor
from PyQt4.QtCore import Qt
#for the shortest path calculations
from qgis.networkanalysis import *




class DispatchHeroDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(DispatchHeroDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # setup global variables
        self.iface = iface
        self.canvas = self.iface.mapCanvas()

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

        # self.calcShortestPath.clicked.connect(self.getCanvasLayers)
        self.drawPolygonButton.clicked.connect(self.drawPolygon)

        # set up variables
        global Polygon
        Polygon = False

    # iface needs to be set up. Make sure this works globally

    # here we will be mapping our signals

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
            # here we will be putting functionality on the signals. We can do this by using modules.

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def request_help(self):
        self.Message_display.clear()
        self.Message_display.addItem("----------------------------------")
        self.Message_display.addItem("Station full")
        if self.Station1.isChecked() == True and self.Station_1_status.value()<100:
            self.Message_display.addItem("Request help")
            self.Message_display.addItem("Station 1")
            self.Message_display.addItem("----------------------------------")
        elif self.Station2.isChecked() == True and self.Station_2_status.value()<100:
            self.Message_display.addItem("Request help")
            self.Message_display.addItem("Station 2")
            self.Message_display.addItem("----------------------------------")
        elif self.Station3.isChecked() == True and self.Station_3_status.value()<100:
            self.Message_display.addItem("Request help")
            self.Message_display.addItem("Station 3")
            self.Message_display.addItem("----------------------------------")
        elif self.Station4.isChecked() == True and self.Station_4_status.value()<100:
            self.Message_display.addItem("Request help")
            self.Message_display.addItem("Station 4")
            self.Message_display.addItem("----------------------------------")
        else:
            self.Message_display.addItem("Station not available")
            self.Message_display.addItem("----------------------------------")

    def autoOn(self):
        self.Message_display.clear()
        self.Message_display.addItem("----------------------------------")
        self.Message_display.addItem("Autodispatch ON")
        self.Message_display.addItem("----------------------------------")
        pass

    def autoOff(self):
        self.Message_display.clear()
        self.Message_display.addItem("----------------------------------")
        self.Message_display.addItem("Autodispatch OFF")
        self.Message_display.addItem("----------------------------------")
        file.close
        pass

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
        file.close
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
            file.close
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
            file.close
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
            file.close
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
            file.close
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
            file.close
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
            file.close
        pass

    def add_truck_instance(self):
        self.In_station_list.addItem(self.Truck_text.text())
        self.Truck_text.setText('')

    def delete_truck_instance(self):
        self.In_station_list.takeItem(self.In_station_list.currentRow())
        pass

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
            # call a function that displays the polygon (rubberBand)
            # self.reset()
            Polygon = False
        global polygonlist
        polygonlist = []
        print "polygon status", Polygon

class NearestFeatureMapTool(QgsMapTool):
    def __init__(self, canvas):

        super(QgsMapTool, self).__init__(canvas)
        self.canvas = canvas
        self.cursor = QCursor(Qt.CrossCursor)
        self.drawpolygon = False
        self.rubberBand = QgsRubberBand(self.canvas, self.drawpolygon)
        self.rubberBand.setColor(Qt.red)
        self.rubberBand.setWidth(1)
        global activelayer
        for layer in self.canvas.layers():
            if layer.name() == 'Rotterdam roads':
                activelayer = layer

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
        print "detected release"
        print Polygon
        if Polygon == True:
                LayerPoint = self.toLayerCoordinates(activelayer, mouseEvent.pos())
                polygonlist.append(LayerPoint)
                print polygonlist
                if len(polygonlist)==1:
                    pass
                if len(polygonlist)==2:
                    #self.canvas.scene().removeItem(self.rubberBand)
                    self.drawPolygon = False
                    points = polygonlist
                    ptstoadd = []
                    for point in points:
                        ptstoadd.append(QgsPoint(point[0], point[1]))
                        print type(ptstoadd), ptstoadd
                    self.rubberBand.setToGeometry(QgsGeometry.fromPolyline(ptstoadd), None)
                    self.rubberBand.setColor(QColor(255, 0, 0))
                    self.rubberBand.setWidth(2)
                if len(polygonlist)>2:
                    #self.canvas.scene().removeItem(self.rubberBand)
                    self.drawpolygon = True
                    points = polygonlist
                    ptstoadd = []
                    for point in points:
                        print type(point[0]), point[0], point[1]
                        ptstoadd.append(QgsPoint(point[0], point[1]))
                    self.rubberBand.setToGeometry(QgsGeometry.fromPolygon([ptstoadd]), None)
                    self.rubberBand.setColor(QColor(255,0,0))
                    self.rubberBand.setWidth(3)

        if Polygon == False:
            layerData = []
            for layer in self.canvas.layers():
                if layer.type() != QgsMapLayer.VectorLayer:
                    # Ignore this layer as it's not a vector
                    continue

                if not layer.name() == 'Rotterdam roads':
                    #Ignore as it is not part of the layer with the graph
                    continue

                # Determine the location of the click in real-world coords
                layerPoint = self.toLayerCoordinates(layer, mouseEvent.pos())
                print layerPoint

    """
    ###Rubber band tools
    def reset(self):
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(QGis.Polygon)
    """
"""
class RectangleMapTool(QgsMapTool):
  def __init__(self, canvas):
      self.canvas = canvas
      QgsMapToolEmitPoint.__init__(self, self.canvas)
      self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon)
      self.rubberBand.setColor(Qt.red)
      self.rubberBand.setWidth(1)
      self.reset()

  def reset(self):
      self.startPoint = self.endPoint = None
      self.isEmittingPoint = False
      self.rubberBand.reset(QGis.Polygon)

  def canvasPressEvent(self, e):
      self.startPoint = self.toMapCoordinates(e.pos())
      self.endPoint = self.startPoint
      self.isEmittingPoint = True
      self.showRect(self.startPoint, self.endPoint)

  def canvasReleaseEvent(self, e):
      self.isEmittingPoint = False
      r = self.rectangle()
      if r is not None:
        print "Rectangle:", r.xMinimum(), r.yMinimum(), r.xMaximum(), r.yMaximum()

  def canvasMoveEvent(self, e):
      if not self.isEmittingPoint:
        return

      self.endPoint = self.toMapCoordinates(e.pos())
      self.showRect(self.startPoint, self.endPoint)

  def showRect(self, startPoint, endPoint):
      self.rubberBand.reset(QGis.Polygon)
      if startPoint.x() == endPoint.x() or startPoint.y() == endPoint.y():
        return

      point1 = QgsPoint(startPoint.x(), startPoint.y())
      point2 = QgsPoint(startPoint.x(), endPoint.y())
      point3 = QgsPoint(endPoint.x(), endPoint.y())
      point4 = QgsPoint(endPoint.x(), startPoint.y())

      self.rubberBand.addPoint(point1, False)
      self.rubberBand.addPoint(point2, False)
      self.rubberBand.addPoint(point3, False)
      self.rubberBand.addPoint(point4, True)    # true to update canvas
      self.rubberBand.show()

  def rectangle(self):
      if self.startPoint is None or self.endPoint is None:
        return None
      elif self.startPoint.x() == self.endPoint.x() or self.startPoint.y() == self.endPoint.y():
        return None

      return QgsRectangle(self.startPoint, self.endPoint)

  def deactivate(self):
      super(RectangleMapTool, self).deactivate()
      self.emit(SIGNAL("deactivated()"))
"""




