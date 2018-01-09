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

import os, threading, time

from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import *
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'spatial_decision_dockwidget_base_extra.ui'))

## added map tools
from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.core import QgsMapLayer, QgsMapToPixel, QgsFeature, QgsFeatureRequest, QgsGeometry, QgsPoint
from PyQt4.QtGui import QCursor, QPixmap, QColor
from PyQt4.QtCore import Qt
#for the shortest path calculations
from qgis.networkanalysis import *


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


