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

# QT and QGIS imports
from PyQt5 import uic
from PyQt5.QtWidgets import *
from qgis.utils import iface

# misc. imports
import os							                    # access files, folders etc
from functools import partial		                    # signal-connect to a function with arguments

# internal imports
from .henningPlugin_validator import PathValidator      # subclass of QValidator to check paths of line edit fields
from .henningPlugin_processor import Worker             # QThread Worker class to get the processing done


"""This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer"""
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'henningsPlugin.ui'))

class DialogAndFunctions(QDialog, FORM_CLASS):
    """Constructor"""
    def __init__(self, parent=None):
        # Load QT-Designer file (ui) with FORM_CLASS. Using self.setupUi()makes every QT element popular -------------
        super(DialogAndFunctions, self).__init__(parent)
        self.setupUi(self)
        
        # Variables ---------------------------------------------------------------------------------------------------
        self.inputDir = None    # input path
        self.outputDir = None   # output path

        # Init list widget
        self.listWidget.addItem("Willkommen zu Hennings Plugin!")
        self.listWidget.addItem("Bitte Input- und Output-Ordner eingeben. Anschließend auf \"Start Prozessierung\" klicken")
        self.listWidget.scrollToBottom()

        # Initialize progress bar ------------------------------------------------------------------------------------
        self.progressBar.setValue(0)    # set value to 0 %

        # Initialize the path validator ------------------------------------------------------------------------------
        self.pathValidator = PathValidator()                    # Invoke QValidator Subclass to check for paths
        self.lineEditInputDir.setValidator(self.pathValidator)  # Set validator of lineeditobject
        self.lineEditOutputDir.setValidator(self.pathValidator) # Set validator of lineeditobject

        # Connect QT elements with functions -------------------------------------------------------------------------
        self.startButton.clicked.connect(self.startProcessing)       # Connect Start Prozessierung-Button with method startProcessing
        self.buttonBox.accepted.connect(self.ok)                     # Connect OK-Button with method ok
        self.buttonBox.rejected.connect(self.cancel)                 # Connect Cancel-Button with method cancel
        self.buttonInputDir.clicked.connect(partial(self.chooseDirectory, self.buttonInputDir, self.lineEditInputDir))       # Connect Input Directory Button with chooseDirectory method
        self.buttonOutputDir.clicked.connect(partial(self.chooseDirectory, self.buttonOutputDir, self.lineEditOutputDir))    # Connect Output Directory Button with chooseDirectory method
        self.lineEditInputDir.textChanged.connect(partial(self.checkPath, self.lineEditInputDir))     # Connect lineEdit with checkPath method
        self.lineEditOutputDir.textChanged.connect(partial(self.checkPath, self.lineEditOutputDir))   # Connect lineEdit with checkPath method

        # Set initial button states -----------------------------------------------------------------------------------
        self.buttonBox.button(0x00000400).setEnabled(False)         # disable OK-Button
        self.buttonBox.button(0x00400000).setEnabled(False)         # disable Cancel-Button
        self.startButton.setEnabled(False)                          # disable Start Prozessierung-Button

    """One of the content elements was edited: font color depends on existence of path """
    def checkPath(self, lineEdit):
        color = "Black" if lineEdit.hasAcceptableInput() else "Red"     # check input / output paths and color them accordingly
        lineEdit.setStyleSheet("font:9pt \"Arial\";color:%s" % color)   # apply the style to the lineEdit object

        # Enable Start Prozessierung-Button if all paths exist
        if self.lineEditInputDir.hasAcceptableInput() and self.lineEditOutputDir.hasAcceptableInput():
            self.startButton.setEnabled(True)                   # enable Prozessierung-Button
            self.inputDir = self.lineEditInputDir.text()        # set inputDir var from current lineEdit-text
            self.outputDir = self.lineEditOutputDir.text()      # set outputDir var from current lineEdit-text
        else:
            self.startButton.setEnabled(False)                   # disable Prozessierung-Button

    """...-button clicked: user may select another path """
    def chooseDirectory(self, pushButton, lineEdit):
        alterPath = pushButton.text()
        path = QFileDialog.getExistingDirectory(None, "Verzeichnis wählen", alterPath, \
                                                QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

        lineEdit.setStyleSheet("color:Black")
        lineEdit.setText(unicode(path))

    """Worker-Thread sends a dictionary: refresh Messages, Log, Progress Bar and Button-states """
    def refreshMessagingButtonsProgress(self, dct_):

        # button handling
        if dct_['okButtonEnabled'] == True:
            self.buttonBox.button(0x00000400).setEnabled(True)    # enable OK-Button as soon as processing is finished
        if dct_['okButtonEnabled'] == False:
            self.buttonBox.button(0x00000400).setEnabled(False)
        if dct_['cancelButtonEnabled'] == True:
            self.buttonBox.button(0x00400000).setEnabled(True)      # enable Cancel-Button
        if dct_['cancelButtonEnabled'] == False:
            self.buttonBox.button(0x00400000).setEnabled(False)     # disable Cancel-Button

        # message handling here:
        if dct_['message']:
            self.listWidget.addItem(dct_['message'])
            self.listWidget.scrollToBottom()
            pass

        # Set progress bar
        self.progressBar.setValue(dct_['count'])

        # insert logging handling here
        if dct_['log'] == True:
            #log(self.v['logFile'], dct_['plugin'], dct_['level'], dct_['message'])
            pass

        # insert handling if process was a success:
        if dct_['level'] == 'SUC':
            iface.messageBar().pushSuccess("Hennings Plugin", dct_['message'])

        dct_.clear()  # empty the dict

        return


    """Start Prozessierung-button clicked: start the Worker-thread and collect signals from thread """
    def startProcessing(self):
        self.listWidget.addItem("Prozessierung startet...")
        self.startButton.setEnabled(False)                      # Start Prozessierung-Button

        # Initialize worker thread ------------------------------------------------------------------------------------
        self.job = Worker(self.inputDir, self.outputDir)
        self.job.dctMessages.connect(self.refreshMessagingButtonsProgress)  # Connect the signal dictionary

        self.job.start()    # Start the worker thread

        return


    """Cancel button clicked: quit processing thread and close window """
    def cancel(self):
        try:
            self.job.terminate()
            iface.messageBar().pushWarning("Hennings Plugin", "Prozessierung Abgebrochen")
        except:
            pass

        self.close()    # close window

    """OK button clicked: close window """
    def ok(self):
        self.close()    # close window
