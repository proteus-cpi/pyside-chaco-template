#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2013 Robert Norris
# Licensed under the terms of the MIT License

"""
MatplotlibWidget
================

This is a Qt4 widget that displays a matplotlib window and toolbar, useful
for embedding in any PySide program that requires simple plotting facilities.

Derived from 'matplotlibwidget.py', which was written for PyQt4.
Copyright © 2009 Pierre Raybaut

Further Derived from 'embedding_in_pyqt4.py':
Copyright © 2005 Florent Rougon, 2006 Darren Dale

This software is licensed under the terms of the MIT License
"""

__version__ = "1.0.0"

import PySide
from PySide import QtGui, QtCore


import matplotlib
matplotlib.use("Qt4Agg")
matplotlib.rcParams['backend.qt4']='PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

class MatplotlibWidget(FigureCanvas):
    """
    MatplotlibWidget inherits PySide.QtGui.QWidget
    and matplotlib.backend_bases.FigureCanvasBase
    
    Options: option_name (default_value)
    -------    
    parent (None): parent widget
    title (''): figure title
    xlabel (''): X-axis label
    ylabel (''): Y-axis label
    xlim (None): X-axis limits ([min, max])
    ylim (None): Y-axis limits ([min, max])
    xscale ('linear'): X-axis scale
    yscale ('linear'): Y-axis scale
    width (4): width in inches
    height (3): height in inches
    dpi (100): resolution in dpi
    hold (False): if False, figure will be cleared each time plot is called
    
    Widget attributes:
    -----------------
    figure: instance of matplotlib.figure.Figure
    axes: figure axes
    
    Example:
    -------
    self.widget = MatplotlibWidget(self, yscale='log', hold=True)
    from numpy import linspace
    x = linspace(-10, 10)
    self.widget.axes.plot(x, x**2)
    self.wdiget.axes.plot(x, x**3)
    """
    def __init__(self, parent=None, title='', xlabel='', ylabel='',
                 xlim=None, ylim=None, xscale='linear', yscale='linear',
                 width=4, height=3, dpi=100, hold=True, X = None, Y = None, Z = None):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_title(title)
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        if xscale is not None:
            self.axes.set_xscale(xscale)
        if yscale is not None:
            self.axes.set_yscale(yscale)
        if xlim is not None:
            self.axes.set_xlim(*xlim)
        if ylim is not None:
            self.axes.set_ylim(*ylim)
        self.axes.hold(hold)

        if X is not None:
          self.X = X
        if Y is not None:
          self.Y = Y
        if Z is not None:
          self.Z = Z

        FigureCanvas.__init__(self, self.figure)
        if parent is not None:
          self.setParent(parent)

        #Canvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def sizeHint(self):
        w, h = self.get_width_height()
        return QtCore.QSize(w, h)

    def minimumSizeHint(self):
        return QtCore.QSize(10, 10)


class MatplotlibInteractiveWidget(QtGui.QWidget):
    """
    A subclass of QtGui.QWidget, the MatplotlibInteractiveWidget is a container
    for two child widgets: a MatplotlibWidget and a NavigationToolbar.  The
    navigation toolbar allows the user to edit the plot parameters such as 
    title, x/y scale, labels, etc. from the GUI, a capability that is not
    present in the bare MatplotlibWidget.  The interactive widget is similar
    to the window that the user sees when calling matplotlib.show()
    """
    def __init__(self, parent = None):
        """
        Initializer for the MatplotlibInteractiveWidget.  Currently only takes
        an optional parameter for a parent widget.
        """
        super(MatplotlibInteractiveWidget, self).__init__()
        self.main_layout = QtGui.QVBoxLayout()
        self.plot_widget = MatplotlibWidget()
        self.navigation_toolbar = NavigationToolbar(self.plot_widget, self)
        self.main_layout.addWidget(self.plot_widget)
        self.main_layout.addWidget(self.navigation_toolbar)
        self.setLayout(self.main_layout)

    def get_axes(self):
        """Returns the axes of the child MatplotlibWidget
        :returns: @todo

        """
        return self.plot_widget.axes

if __name__ == '__main__':
  import sys
  application = QtGui.QApplication(sys.argv)
  main_widget = MatplotlibInteractiveWidget()
  from numpy import arange, sin, pi
  x = arange(-2*pi,2*pi,0.1)
  y = sin(x)/x
  ax = main_widget.get_axes()
  ax.plot(x,y,label = r'$\mathrm{Sinc} \left ( x \right )$')
  ax.set_xlabel(r'$x$')
  ax.set_ylabel(r'$y$')
  ax.set_title(r'Example Plot')
  ax.legend(loc = 'best')
  main_widget.show()
  main_widget.raise_()
  sys.exit(application.exec_())
