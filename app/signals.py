# -*- coding: utf-8 -*-
"""QT Signals that the application provides"""

from PyQt5.QtCore import QObject, pyqtSignal, QProcess

class Signals(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    segmentation_finished = pyqtSignal()

    simulation_finished = pyqtSignal()

signals = Signals()