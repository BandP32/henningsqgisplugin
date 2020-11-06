# -*- coding: utf-8 -*-
"""
 **********************************************************************************************************************
    henningsPlugin     A QGIS 3 plugin

 ----------------------------------------------------------------------------------------------------------------------
        programming:
        copyright:
        email:
 ----------------------------------------------------------------------------------------------------------------------

 **********************************************************************************************************************
 *  This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public *
 *  License as published by the Free Software Foundation; either version 2 of the License or (at your option) any     *
 *  later version.                                                                                                    *
 **********************************************************************************************************************
"""

def classFactory(iface):
    from .henningsPlugin import PluginHenning
    return PluginHenning(iface)
