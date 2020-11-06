# -*- coding: utf-8 -*-
"""
 **********************************************************************************************************************
 	lglnEinstellungen	A QGIS 3 plugin

						This plugin allows the editing of the settings of the LGLN-Plugins in a dialog window.
						These are mainly path settings and values used in these plugins and stored in a textfile.

 ----------------------------------------------------------------------------------------------------------------------
		copyright:		(C) 2019 by Thorsten Dunker(LGLN)
		email:			thorsten.dunker@lgln.niedersachsen.de
 ----------------------------------------------------------------------------------------------------------------------

 **********************************************************************************************************************
 *  This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public *
 *  License as published by the Free Software Foundation; either version 2 of the License or (at your option) any     *
 *  later version.                                                                                                    *
 **********************************************************************************************************************
"""

from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
import os.path													# access files
from .henningPlugin_functions import DialogAndFunctions		# import the code for the dialog


class PluginHenning:
    """Constructor"""
    def __init__(self, iface):	
        self.iface = iface										# Save reference to the QGIS interface
        self.plugin_dir = os.path.dirname(__file__)				# initialize plugin directory

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr('&PluginHenning')


    """Get the translation for a string using Qt translation API"""
    def tr(self, message):
        return QCoreApplication.translate('PluginHenning', message)


    """Add a toolbar icon to the toolbar."""
    def add_action(self, icon_path, text, callback, enabled_flag=True, add_to_menu=True, add_to_toolbar=True, 
                   status_tip=None, whats_this=None, parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)
        if status_tip is not None:
            action.setStatusTip(status_tip)
        if whats_this is not None:
            action.setWhatsThis(whats_this)
        if add_to_toolbar:
            self.iface.addToolBarIcon(action)					# Adds plugin icon to Plugins toolbar
        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)
        self.actions.append(action)
        return action

        
    """Create the menu entries and toolbar icons inside the QGIS GUI."""
    def initGui(self):
        icon_path = QIcon(self.plugin_dir + "/icon.png")
        self.add_action(icon_path, text=self.tr('PluginHenning'), callback=self.run, parent=self.iface.mainWindow())


    """Removes the plugin menu item and icon from QGIS GUI."""
    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(self.tr('&PluginHenning'), action)
            self.iface.removeToolBarIcon(action)


    """ Call the dialog and use the functionality behind it """
    def run(self):
        self.dlg = DialogAndFunctions()							# dialog object
        self.dlg.show()											# show the dialog
        result = self.dlg.exec_()								# run the dialog event loop
