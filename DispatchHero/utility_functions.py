#----------------------------------------------------#
#      Class for parsing the bridges is timeSlots    #
#----------------------------------------------------#

from PyQt4 import QtGui, QtCore
from qgis.core import *
# from qgis.networkanalysis import *

# from pyspatialite import dbapi2 as sqlite
# import psycopg2 as pgsql
# import numpy as np
# import math
# import os.path


class BridgeParser():

	def __init__(self, openFileObject):
		self.file = openFileObject
		self.timeSlots = []
		self.timeDict = {}

	def parse(self):
		self.fh = self.file.readlines()
		self.file.close()

		for line in self.fh:
			dictObject = eval(line.strip())
			openingTime = dictObject['open']
			if not openingTime in self.timeSlots:
				self.timeSlots.append(openingTime)
				self.timeDict[openingTime] = []

		for openingTime in self.timeSlots:
			for line in self.fh:
				dictObject = eval(line.strip())
				if dictObject['open'] == openingTime:
					self.timeDict[openingTime].append(dictObject['id'])

	def generator(self):
		for time in self.timeSlots:
			yield self.timeDict[time], time


def makeUndirectedGraph(network_layer, points=list):
    graph = None
    tied_points = []
    if network_layer:
        director = QgsLineVectorLayerDirector(network_layer, -1, '', '', '', 3)
        properter = QgsDistanceArcProperter()
        director.addProperter(properter)
        builder = QgsGraphBuilder(network_layer.crs())
        tied_points = director.makeGraph(builder, points)
        graph = builder.graph()
    return graph, tied_points

    
def calculateRouteDijkstra(graph, tied_points, origin, destination, impedance=0):
    points = []
    if tied_points:
        try:
            from_point = tied_points[origin]
            to_point = tied_points[destination]
        except:
            return points

        # analyse graph
        if graph:
            from_id = graph.findVertex(from_point)
            to_id = graph.findVertex(to_point)

            (tree, cost) = QgsGraphAnalyzer.dijkstra(graph, from_id, impedance)

            if tree[to_id] == -1:
                pass
            else:
                curPos = to_id
                while curPos != from_id:
                    points.append(graph.vertex(graph.arc(tree[curPos]).inVertex()).point())
                    curPos = graph.arc(tree[curPos]).outVertex()

                points.append(from_point)
                points.reverse()

    return points

