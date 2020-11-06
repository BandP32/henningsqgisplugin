# -*- coding: utf-8 -*-
"""
 **********************************************************************************************************************
	henningsPlugin  	A QGIS 3 plugin

 ----------------------------------------------------------------------------------------------------------------------
		copyright:
		email:
 ----------------------------------------------------------------------------------------------------------------------

 **********************************************************************************************************************
 *  This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public *
 *  License as published by the Free Software Foundation; either version 2 of the License or (at your option) any     *
 *  later version.                                                                                                    *
 **********************************************************************************************************************
"""

from PyQt5 import uic
from PyQt5.QtGui import QValidator
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from qgis.utils import iface
import os							# access files
import json							# load JSON as a dictionary
from glob import glob				# access files with wildcards
from functools import partial		# signal-connect to a function with arguments
from .henningPlugin_validator import PathValidator

"""This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer"""
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'henningsPlugin.ui'))

class DialogAndFunctions(QDialog, FORM_CLASS):
    """Constructor"""
    def __init__(self, parent=None):
        # Load QT-Designer file (ui) with FORM_CLASS. Using self.setupUi()makes eveery QT element popular -------------
        super(DialogAndFunctions, self).__init__(parent)
        self.setupUi(self)
        
        # Variables ---------------------------------------------------------------------------------------------------

        # Initialize the path validator
        self.pathValidator = PathValidator()                    # Invoke QValidator Subclass to check for paths
        self.lineEditInputDir.setValidator(self.pathValidator)  # Set validator of line edit fields
        self.lineEditOutputDir.setValidator(self.pathValidator)

        # Connect QT elements with functions ----------------------------------------------------------------------
        self.buttonBox.accepted.connect(self.startProcessing)       # OK-Button
        self.buttonBox.rejected.connect(self.cancel)                # Cancel-Button
        self.buttonInputDir.clicked.connect(partial(self.chooseDirectory, self.buttonInputDir, self.lineEditInputDir))           # Input Directory Button
        self.buttonOutputDir.clicked.connect(partial(self.chooseDirectory, self.buttonOutputDir, self.lineEditOutputDir))        # Output Directory Button
        self.lineEditInputDir.textChanged.connect(partial(self.checkPath, self.lineEditInputDir))
        self.lineEditOutputDir.textChanged.connect(partial(self.checkPath, self.lineEditOutputDir))

        # Set initial button states -----------------------------------------------------------------------------------
        self.buttonBox.button(0x00000400).setEnabled(False)     # OK-Button
        self.buttonBox.button(0x00400000).setEnabled(True)      # Cancel-Button

    """One of the content elements was edited: font color depents on existence of path and on changes made """
    def checkPath(self, lineEdit):
        lineEdit.setValidator(self.pathValidator)
        color = "Black" if lineEdit.hasAcceptableInput() else "Red"
        lineEdit.setStyleSheet("font:9pt \"Arial\";color:%s" % color)
        # Enable OK-Button if all paths exist
        if self.lineEditInputDir.hasAcceptableInput() and self.lineEditOutputDir.hasAcceptableInput():
            self.buttonBox.button(0x00000400).setEnabled(True)  # enable OK-Button

    """...-button clicked: user may select another path """
    def chooseDirectory(self, pushButton, lineEdit):
        alterPath = pushButton.text()
        path = QFileDialog.getExistingDirectory(None, "Verzeichnis wählen", alterPath, \
                                                QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

        lineEdit.setStyleSheet("color:Black")
        lineEdit.setText(unicode(path))

    """OK button clicked: store elements in the property file and quit plugin """
    def startProcessing(self):
        iface.messageBar().pushMessage("Hennings Plugin", "Prozessierung startet...")
        self.buttonBox.button(0x00000400).setEnabled(False)     # OK-Button


    """Cancel button clicked: quit without storing """
    def cancel(self):
        iface.messageBar().pushWarning("Hennings Plugin", "Prozessierung Abgebrochen")
        self.close()
