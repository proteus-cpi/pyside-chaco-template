from pyface.qt import QtGui, QtCore

from traits.api import HasTraits, Instance, on_trait_change, Enum, CInt
from traitsui.api import View, Item

################################################################################
#The actual visualization
class TraitedObject(HasTraits):

    gain = Enum(1, 2, 3,
                desc="the gain index of the camera",
                label="gain", )
    
    exposure = CInt(10, desc="the exposure time", label="Exposure", )


################################################################################
# The QWidget containing the visualization, this is pure PyQt4 code.
class TraitedQWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.traitedObject = TraitedObject()

        # The edit_traits call will generate the widget to embed.
        self.ui = self.traitedObject.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)
