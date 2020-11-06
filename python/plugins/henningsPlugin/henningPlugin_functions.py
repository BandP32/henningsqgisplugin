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
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from qgis.utils import iface
import os							# access files
import json							# load JSON as a dictionary
from glob import glob				# access files with wildcards
from functools import partial		# signal-connect to a function with arguments

"""This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer"""
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'henningsPlugin.ui'))

class DialogAndFunctions(QDialog, FORM_CLASS):
    """Constructor"""
    def __init__(self, parent=None):
        # Load QT-Designer file (ui) with FORM_CLASS. Using self.setupUi()makes eveery QT element popular -------------
        super(DialogAndFunctions, self).__init__(parent)
        self.setupUi(self)
        
        # Variables ---------------------------------------------------------------------------------------------------
        self.propFile = QSettings().value("propFile")					# property flle
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)	# scaleable grid
        self.qtElemente = {}											# QT-elements & properties
        zeile = 0
        
        # Exceptions in viewing and editing
        self.noFiles = ['aks.json']										# files that should not be handled like files
        self.uneditible = ['gitToke', 'gitUrl_']						# keys that should not be editable
        self.dontshow = ['sendErr', 'sendFro', 'sendTo_']               # keys that should be hidden

        if os.path.exists(self.propFile) and os.access(self.propFile, os.W_OK):
            # Read variables and comments from property file ----------------------------------------------------------
            try:
                with open(self.propFile, 'r') as f: self.var, self.rem = json.load(f)
                f.close()
            except IOError:
                iface.messageBar().pushCritical("Plugin Einstellungen", "Zugriffsfehler der Properties-Datei")


            # Adjust window size to properties content and show property filename in title ----------------------------
            maxWidth = 7 * (len(max(self.var.values(), key=len)) + len(max(self.rem.values(), key=len))) + 60
            maxHeight = 30 * len(self.var) + 60
            #self.resize(QSize(maxWidth, maxHeight))
            self.setWindowTitle("Hennings Plugin")
            
            # Apply QT-Frame, Grid-Layout und QT elements in an array -------------------------------------------------
            for key in sorted(self.var.keys()):
                if key not in self.dontshow:
                    print(key)
                    val = self.var[key]
                    kommentar = self.rem[key]
                    self.qtElemente[key] = [QLabel(), QLineEdit()]

                    # First column (fieldname)
                    self.qtElemente[key][0].setAlignment(Qt.AlignRight)
                    self.qtElemente[key][0].setStyleSheet("font:9pt \"Arial\";font-weight:bold;margin-right:4px")
                    self.qtElemente[key][0].setText(unicode(kommentar))
                    self.gridLayout.addWidget(self.qtElemente[key][0], zeile, 0)

                    # Second column (content is editable)
                    self.qtElemente[key][1].setAlignment(Qt.AlignLeft)
                    color = "Grey" if key in self.uneditible \
                                   else ("Red" if ('/' in val or '\\' in val) and not os.path.exists(val) \
                                         and os.path.basename(val) not in self.noFiles \
                                   else "Black")
                    self.qtElemente[key][1].setStyleSheet("font:9pt \"Arial\";color:%s" % color)
                    self.qtElemente[key][1].setText(unicode(val))
                    if key not in self.uneditible:
                        self.qtElemente[key][1].textChanged.connect(partial(self.checkPath, key))
                    else:
                        self.qtElemente[key][1].setReadOnly(True)
                    self.gridLayout.addWidget(self.qtElemente[key][1], zeile, 1)

                    # Third column (button for path/file selection, if content is a path)
                    if key[-4:] in ['Path', 'File', 'Gpkg', 'Json'] and os.path.basename(val) not in self.noFiles:
                        self.qtElemente[key].append(QPushButton())
                        self.qtElemente[key][2].setStyleSheet("font:\"Arial Black\"")
                        self.qtElemente[key][2].setText("...")
                        self.qtElemente[key][2].setMaximumSize(QSize(30, 30))
                        self.qtElemente[key][2].clicked.connect(partial(self.pfadAendern, key))
                        self.gridLayout.addWidget(self.qtElemente[key][2], zeile, 2)

                    zeile += 1
            
            # Connect QT elements with functions ----------------------------------------------------------------------
            self.buttonBox.accepted.connect(self.okVerlassen)
            self.buttonBox.rejected.connect(self.cancelVerlassen)
            self.applyButton.clicked.connect(self.speichern)
            self.applyButton.setEnabled(False)
        
        else:
            fehlerAnzeige = QLabel()
            fehlerAnzeige.setAlignment(Qt.AlignCenter)
            fehlerAnzeige.setStyleSheet("font:11pt \"Arial Black\";color:Crimson")
            fehlerAnzeige.setText("Probleme mit der Properties-Datei:\n%s\n\n" \
                                   "Plugin kann daher nicht ausgeführt werden." % self.propFile)
            self.gridLayout.addWidget(fehlerAnzeige, 0, 0)
            self.applyButton.setEnabled(False)


    """One of the content elements was edited: font color depents on existence of path and on changes made """
    def checkPath(self, key):
        path = self.qtElemente[key][1].text()
        color = "Red" if ('/' in path or '\\' in path) and not os.path.exists(path) \
                          and os.path.basename(self.var[key]) not in self.noFiles else "Black"
        self.qtElemente[key][1].setStyleSheet("font:9pt \"Arial\";color:%s" % color)
        self.applyButton.setEnabled(True)


    """...-button clicked: user may select another file or path """
    def pfadAendern(self, key):
        alterPfad = self.qtElemente[key][1].text()
        if key[-4:] in ['File', 'Gpkg', 'Json']:
            pfad = QFileDialog.getOpenFileName(None, "Datei wählen", alterPfad)[0]
        elif 'Path' in key:
            pfad = QFileDialog.getExistingDirectory(None, "Verzeichnis wählen", alterPfad, \
                                                    QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        else:
            pfad = ""
        if pfad:
            self.qtElemente[key][1].setStyleSheet("color:Black")
            self.qtElemente[key][1].setText(unicode(pfad))
            self.applyButton.setEnabled(True)


    """Save button clicked: store elements in the property file """
    def speichern(self):
        try:
            # refresh property dictionary
            self.var = {key: (self.qtElemente[key][1].text() if key not in self.dontshow
                                                        else self.var[key]) for key, value in self.var.items()}

            # write to property file
            with open(self.propFile, 'w') as f: json.dump([self.var, self.rem], f, indent=4, sort_keys=True)
            f.close()
            
            # set property environment variable
            QSettings().setValue("props", self.var)
            
            # disable save button
            self.applyButton.setEnabled(False)
        except IOError:
            iface.messageBar().pushCritical("Plugin Einstellungen", "Zugriffsfehler der Properties-Datei")
        
        iface.messageBar().pushSuccess("Plugin Einstellungen", "Änderungen wurden gespeichert")


    """OK button clicked: store elements in the property file and quit plugin """
    def okVerlassen(self):
        if self.applyButton.isEnabled():
            self.speichern()
        self.close()


    """Cancel button clicked: quit without storing """
    def cancelVerlassen(self):
        if self.applyButton.isEnabled():
            iface.messageBar().pushWarning("Plugin Einstellungen", "Änderungen wurden nicht gespeichert")
        self.close()
