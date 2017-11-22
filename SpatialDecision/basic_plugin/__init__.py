# -*- coding: utf-8 -*-
"""
/***************************************************************************
 basic_plugin
                                 A QGIS plugin
 basic plugin setup
                             -------------------
        begin                : 2017-11-22
        copyright            : (C) 2017 by Group 7
        email                : pim.o.klaassen@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load basic_plugin class from file basic_plugin.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .basic plugin import basic_plugin
    return basic_plugin(iface)
