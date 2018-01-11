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

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'DispatchHero_dockwidget_base.ui'))

from qgis.utils import iface
from PyQt4 import QtCore, QtGui



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
        self.Add_Route.clicked.connect(self.addlist_routes)
        self.Delete.clicked.connect(self.delete_routes)

        self.Add_message.clicked.connect(self.add_message_alert)

        self.Truck_station_add.clicked.connect(self.add_station_instance)
        self.Truck_route_add.clicked.connect(self.add_route_instance)

        self.Auto_ON.clicked.connect(self.autoOn)
        self.Auto_OFF.clicked.connect(self.autoOff)

        self.check1.clicked.connect(self.click1)
        self.check2.clicked.connect(self.click2)
        self.check3.clicked.connect(self.click3)
        self.check4.clicked.connect(self.click4)

        self.Stop.clicked.connect(self.cancelSelection)
        self.Accept.clicked.connect(self.dispatch)
        self.Available.

    # iface needs to be set up. Make sure this works globally

    # here we will be mapping our signals

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
            # here we will be putting functionality on the signals. We can do this by using modules.

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def autoOn(self):
        pass

    def autoOff(self):
        pass

    def previous(self):
        pass

    def next(self):
        pass

    def addButton(self):
        pass

    def cancelSelection(self):
        pass

    def drawPolygon(self):
        pass

    def dispatch(self):
        pass

    def setDestination(self):
        pass

    def addlist_routes(self):
        self.Routes.addItem(self.Route_name.text())
        self.Route_name.setText('')
        self.Route_name.setFocus()
        pass

    def delete_routes(self):
        self.Routes.takeItem(self.Routes.currentRow())
        pass

    def show_routes(self):
        pass

    def add_message_alert(self):
        self.Message_display.addItem(self.Route_message.text())
        self.Route_message.setText('')
        self.Route_message.setFocus()
        pass

    def add_station_instance(self):
        self.In_station_list.addItem(self.In_route_list.takeItem(self.In_route_list.currentRow()))
        pass

    def add_route_instance(self):
        self.In_route_list.addItem(self.In_station_list.takeItem(self.In_station_list.currentRow()))
        pass

    def delete_truck_instance(self):
        self.Trucks.removeRow(self.Trucks.currentRow())
        pass

    def click1(self):
        pass

    def click2(self):
        pass

    def click3(self):
        pass

    def click4(self):
        pass





