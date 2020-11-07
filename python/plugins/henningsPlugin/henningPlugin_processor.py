# -*- coding: utf-8 -*-
"""
 **********************************************************************************************************************
	henningPlugin	A QGIS 3 plugin

 ----------------------------------------------------------------------------------------------------------------------
	copyright:		(C) 2020 by Lars Froehlich
	email:			lars.froehlich@online.de
 ----------------------------------------------------------------------------------------------------------------------

 **********************************************************************************************************************
 *  This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public *
 *  License as published by the Free Software Foundation; either version 2 of the License or (at your option)any      *
 *  later version.                                                                                                    *
 **********************************************************************************************************************
"""

from PyQt5.QtCore import *
import time

"""********************************************************************************************************************
													Class
********************************************************************************************************************"""

###################################################
# Thread-"working"-class:
class Worker(QThread):
    """
    Info:
    A QThread instance represents a thread and provides the means to start()
    a thread, which will then execute the reimplementation of QThread::run().
    The run() implementation is for a thread what the main() entry point is
    for the application.
    """
    # QT-signal-variables for communication from one thread to another
    dctMessages = pyqtSignal(dict)  # Defines a dictionary as pyqt signal variable

    """Constructor"""
    def __init__(self, inputDir, outputDir):
        """Refresh the progress bar from dictionary keys current and sum"""
        super().__init__()      # init QThread

        self.inputDir = inputDir
        self.outputDir = outputDir
        # define additional variables here ------------------------------------------------------------------------------

    """Helper method to send progress refresh to main thread"""
    def refreshProgress(self, _dct):
        progress = int(_dct['current'] / _dct['sum'] * 100)
        if progress > 100:
            progress = 100
        self.dctMessages.emit({"plugin": "henningPlugin", "level": "INF",
                               "message": _dct['message'],
                               "count": progress, 'log': False,
                               "okButtonEnabled": False,
                               "cancelButtonEnabled": True})


    """This method is the thread entry point of QThread"""
    def run(self):

        self.dctMessages.emit(
            {"plugin": "henningPlugin", "level": "INF",
             "message": "INFO: Starte Prozessierung. Input-Ordner: %s   Output-Ordner: %s" % (self.inputDir, self.outputDir),
             "count": 0, 'log': True,
             'okButtonEnabled': False, "cancelButtonEnabled": True})

        #################################
        # EXAMPLE #
        # PUT YOUR SCRIPT HERE
        #################################
        dct = {'sum': 100, 'current': 0}
        for x in range(101):
            dct['current'] = x
            dct['message'] = "INFO: Prozessiere Karte %s von %s" % (x, dct['sum'])
            self.refreshProgress(dct)
            time.sleep(0.05)
        # ###############################
        # EXAMPLE END
        #################################

        self.dctMessages.emit(
            {"plugin": "henningPlugin", "level": "SUC",
             "message": "INFO: Prozessierung fertig! Die Karten sind in Ordner %s gespeichert." % self.outputDir, "count": 100, 'log': True,
             'okButtonEnabled': True, "cancelButtonEnabled": False})

        return
