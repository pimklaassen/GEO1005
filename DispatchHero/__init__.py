# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DispatchHero
                                 A QGIS plugin
 This plugin dispatches firetrucks
                             -------------------
        begin                : 2017-12-13
        copyright            : (C) 2017 by TU Delft
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
    """Load DispatchHero class from file DispatchHero.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    # 
    from .DispatchHero import DispatchHero
    return DispatchHero(iface)
