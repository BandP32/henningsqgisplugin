# -*- coding: utf-8 -*-
"""
 **********************************************************************************************************************
	alkisLoader		A QGIS 3 plugin

 ----------------------------------------------------------------------------------------------------------------------
	copyright:		(C) 2020 by Lars Froehlich
	email:			lars.froehlich@lgln.niedersachsen.de
 ----------------------------------------------------------------------------------------------------------------------

 **********************************************************************************************************************
 *  This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public *
 *  License as published by the Free Software Foundation; either version 2 of the License or (at your option)any      *
 *  later version.                                                                                                    *
 **********************************************************************************************************************
"""

from PyQt5.QtCore import *
from qgis.core import *

"""********************************************************************************************************************
													Class
********************************************************************************************************************"""

###################################################
# Thread-"working"-class:
class Worker(QThread):
    """
    Download
    Extract GZ Alkis package

    Info:
    A QThread instance represents a thread and provides the means to start()
    a thread, which will then execute the reimplementation of QThread::run().
    The run() implementation is for a thread what the main() entry point is
    for the application.
    """
    # QT-signal-variables for communication from one thread to another
    dctMessages = pyqtSignal(dict)  # Defines a dictionary as pyqt signal variable

    def __init__(self):
        """Refresh the progress bar from dictionary keys current and sum"""
        super().__init__()      # init QThread


    def refreshProgress(self, _dct):
        progress = int(_dct['current'] / _dct['sum'] * 100)
        if progress > 100:
            progress = 100
        self.dctMessages.emit({"plugin": "henningPlugin", "level": "INF",
                               "message": '',
                               "count": progress, 'log': False})

    def run(self):  # This is the thread entry point of QThread

        count = 0
        self.dctMessages.emit(
            {"plugin": "henningPlugin", "level": "INF", "message": "INFO: Starte Thread", "count": count, 'log': True})

        dct = {'sum':100, 'current': 0}
        for x in range(100):
            dct['current'] = x
            self.refreshProgress(dct)