#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Main application entry point"""
import sys
from PyQt5 import QtWidgets

if __name__ == '__main__':
    from app.application import Application

    qApp = QtWidgets.QApplication(sys.argv)

    asphalt_simulator = Application()
    asphalt_simulator.setWindowTitle("Asphalt Mixtures Aging Simulator")
    asphalt_simulator.show()

    sys.exit(qApp.exec())

