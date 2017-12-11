'''
Copyright (C) 2015 Jeison Pacateque, Santiago Puerto, Wilmar Fernandez

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

from PyQt5 import QtWidgets, QtCore

import matplotlib.image as mpimg
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Canvas(FigureCanvas):
    """Set the graphical elements to show in a Qt Window"""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.axes.hold(False)  # We want the axes cleared every time plot() is called
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class DynamicMplCanvas(Canvas):
    """This Class implements the canvas update method to animate the samples """

    def __init__(self, main_widget, width=5, height=4, dpi=100, collection=[]):
        super(DynamicMplCanvas, self).__init__(main_widget, width=width, height=height, dpi=dpi)
        self.timer = QtCore.QTimer()  # Timer intended to update the image
        self.paused = True
        self.index = 0
        self._collection = collection
        self.myFigure = Canvas()
        initial = mpimg.imread('./images/python.png')
        self.temp = self.axes.imshow(initial)

        min, max = (-1, 2)
        step = 1
        # Setting up a colormap
        self.mymap = mpl.colors.LinearSegmentedColormap.from_list('mycolors', ['blue', 'white', 'red'])
        Z = [[0, 0], [0, 0]]
        levels = range(min, max + step, step)
        material_colors = plt.contourf(Z, levels, cmap=self.mymap)
        plt.clf()

        # Plotting what I actually want
        X = [[1, 2], [1, 2], [1, 2], [1, 2]]
        Y = [[1, 2], [1, 3], [1, 4], [1, 5]]
        Z = [-50, -1, 0, 50]
        for x, y, z in zip(X, Y, Z):
            # setting rgb color based on z normalized to my range
            r = (float(z) - min) / (max - min)
            g = 0
            b = 1 - r
        plt.plot(x, y, color=(r, g, b))
        self.fig_colorbar = self.myFigure.fig.colorbar(material_colors, ax=self.axes)
        self.fig_colorbar.set_ticklabels(['', '', '', ''])

    def update_figure(self):
        """Read and plot all the images stored in the image list"""
        # Set the labels for the materials
        self.fig_colorbar.set_ticklabels(['', 'Voids', 'Mastic', 'Aggregate'])
        #if len(self.collection) <= 0:
        #    self.collection = aw.get_collection()
        if self.index != len(self._collection):  # Conditional to restart the loop

            self.temp = self.axes.imshow(self._collection[self.index], cmap='seismic', interpolation='nearest')

            status_text = "Sample: " + str(self.index)
            #aw.update_staus(status_text)  # Show in status bar the current index #TODO
            self.index += 1
            self.draw()
        else:
            self.index = 0  # When iteration catches the len(self.collection) restart the loop

    @property
    def collection(self):
        return self.collection

    @collection.setter
    def collection(self, collection):
        self._collection = collection

    def start_animation(self):
        """
        Run the 2D ui of the X-Ray raw or treated Dicom slices from
        the asphalt mixture sample
        """
        self.index = 0
        self.timer.timeout.connect(self.update_figure)
        self.timer.start(300)  # Set the update time
        self.paused = False

    def pause_animation(self):
        """
        Pause and Resume the 2D ui of the X-Ray raw or treated Dicom slices from
        the asphalt mixture sample
        """
        if self.paused:
            self.timer.start(300)
            self.paused = False
        else:
            self.timer.stop()
            self.paused = True