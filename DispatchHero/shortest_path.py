# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NearestFeature
                                 A QGIS plugin
 Selects the nearest feature.
                              -------------------
        begin                : 2014-10-15
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Peter Wells for Lutra Consulting
        email                : info@lutraconsulting.co.uk
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
from qgis.gui import QgsMapTool
from qgis.core import QgsMapLayer, QgsMapToPixel, QgsFeature, QgsFeatureRequest, QgsGeometry
from PyQt4.QtGui import QCursor, QPixmap
from PyQt4.QtCore import Qt
#from DispatchHero_dockwidget import DispatchHeroDockWidget to be fixed


class NearestFeatureMapTool(QgsMapTool):
    def __init__(self, canvas):

        super(QgsMapTool, self).__init__(canvas)
        self.canvas = canvas
        self.cursor = QCursor(Qt.CrossCursor)

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
        print DispatchHero.Polygon
        polygonlist = []
        if Polygon == True:
            for layer in self.canvas.layers():
                if layer.name() == 'Rotterdam roads':
                    LayerPoint = self.toLayerCoordinates(layer, mouseEvent.pos())
                    polygonlist.append(LayerPoint)
                    print polygonlist

        if Polygon == False:
            layerData = []
            for layer in self.canvas.layers():
                if layer.type() != QgsMapLayer.VectorLayer:
                    # Ignore this layer as it's not a vector
                    continue

                if not layer.name() == 'Rotterdam roads':
                    #Ignore as it is not part of the layer with the graph
                    continue

                if layer.featureCount() == 0:
                    # There are no features - skip
                    continue

                layer.removeSelection()

                # Determine the location of the click in real-world coords
                layerPoint = self.toLayerCoordinates(layer, mouseEvent.pos())
                print layerPoint
                shortestDistance = float("inf")
                closestFeatureId = -1

                # Loop through all features in the layer
                for f in layer.getFeatures():
                    dist = f.geometry().distance(QgsGeometry.fromPoint(layerPoint))
                    if dist < shortestDistance:
                        shortestDistance = dist
                        closestFeatureId = f.id()

                info = (layer, closestFeatureId, shortestDistance)
                layerData.append(info)

            if not len(layerData) > 0:
                # Looks like no vector layers were found - do nothing
                return

            # Sort the layer information by shortest distance
            layerData.sort(key=lambda element: element[2])
            print layerData
            # Select the closest feature
            layerWithClosestFeature, closestFeatureId, shortestDistance = layerData[0]
            layerWithClosestFeature.select(closestFeatureId)

    def getCanvasLayers(iface, geom='all', provider='all'):
        """Return list of valid QgsVectorLayer in QgsMapCanvas, with specific geometry type and/or data provider"""
        layers_list = []
        for layer in iface.mapCanvas().layers():
            add_layer = False
            if layer.isValid() and layer.type() == QgsMapLayer.VectorLayer:
                if layer.hasGeometryType() and (geom is 'all' or layer.geometryType() in geom):
                    if provider is 'all' or layer.dataProvider().name() in provider:
                        add_layer = True
            if add_layer:
                layers_list.append(layer)
        print "layer list", layers_list
        return layers_list
