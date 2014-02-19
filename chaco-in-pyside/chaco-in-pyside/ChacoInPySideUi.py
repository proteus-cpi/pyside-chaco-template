import os, sys
os.environ['ETS_TOOLKIT'] = 'qt4'
from pyface.qt import QtGui, QtCore

from MayaviQWidget            import MayaviQWidget, Visualization
from MatplotlibQWidget        import MatplotlibInteractiveWidget
from TraitedQWidget           import TraitedQWidget
from DynamicChacoPlotQWidget  import DynamicChacoPlotQWidget


class ChacoInPySideUi(QtGui.QMainWindow):
    
    def __init__(self):
        super(ChacoInPySideUi, self).__init__()
        
        self.initUI()
        
    def initUI(self):     
        container = QtGui.QWidget()
        self.setCentralWidget(container)

        hbox_top = QtGui.QHBoxLayout(container)
        splitter_h = QtGui.QSplitter(QtCore.Qt.Horizontal)
        hbox_top.addWidget(splitter_h)

        leftPanel = QtGui.QFrame()
        leftPanel.setFrameShape(QtGui.QFrame.StyledPanel)
        splitter_h.addWidget(leftPanel)

        splitter_v = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter_h.addWidget(splitter_v)

        centerTab = QtGui.QTabWidget()
        splitter_v.addWidget(centerTab)

        centerTab.addTab(self.create_MayaviPanel(), "Mayavi tab")
        centerTab.addTab(self.create_MatplotlibTab(), "Matplotlib tab")
        centerTab.addTab(self.create_TraitedQWidget(), "Traited QWidget")
        centerTab.addTab(self.create_DynamicChacoPlotQWidget(), "Dynamic Chaco Plot")



        bottomPanel = QtGui.QFrame()
        bottomPanel.setFrameShape(QtGui.QFrame.StyledPanel)
        splitter_v.addWidget(bottomPanel)
        hbox_b = QtGui.QHBoxLayout(bottomPanel)
        hbox_b.addStretch(2)


        okButton     = QtGui.QPushButton("OK")
        cancelButton = QtGui.QPushButton("Cancel")

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QtGui.QVBoxLayout(leftPanel)
        vbox.addStretch(1)
        #vbox.addLayout(layout)
        vbox.addLayout(hbox)


        ####################
        # Actions
        ####################
        # Ref: https://developer.gnome.org/icon-naming-spec/ for QIcon.fromTheme
        openAction = QtGui.QAction(QtGui.QIcon.fromTheme("folder-open"), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open File')
        openAction.triggered.connect(self.Open)

        exitAction = QtGui.QAction(QtGui.QIcon.fromTheme("exit"), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)


        ####################
        # Menu Bar
        ####################
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        ####################
        # Toolbar
        ####################
        self.toolbar = self.addToolBar('File')
        self.toolbar.addAction(openAction)
        self.toolbar.addAction(exitAction)

        ####################
        # Status bar
        ####################
        self.statusBar().showMessage('Ready')

        ####################
        # Window title etc.
        ####################
        self.setGeometry(200, 200, 450, 350)
        self.setWindowTitle('Gallium C Link Budget Calculator')   
        self.setMinimumSize(800,600)
        self.show()

    def Open(self):
        self.statusBar().showMessage('Action Open invoked')

    def create_MayaviPanel(self):
        centerPanel = QtGui.QFrame()
        centerPanel.setFrameShape(QtGui.QFrame.StyledPanel)

        # define a "complex" layout to test the behaviour
        layout    = QtGui.QGridLayout(centerPanel)
        # put some stuff around mayavi
        label_list = []
        for i in range(3):
            for j in range(3):
                if (i==1) and (j==1):continue
                label = QtGui.QLabel(centerPanel)
                label.setText("Your QWidget at (%d, %d)" % (i,j))
                label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
                layout.addWidget(label, i, j)
                label_list.append(label)
        mayavi_widget = MayaviQWidget(centerPanel)   
        layout.addWidget(mayavi_widget, 1, 1, 2, 2)
        return centerPanel

    def create_MatplotlibTab(self):
        mpl_plot = MatplotlibInteractiveWidget()
        from numpy import arange, sin, pi
        x = arange(-2*pi,2*pi,0.1)
        y = sin(x)/x
        ax = mpl_plot.get_axes()
        ax.plot(x,y,label = r'$\mathrm{Sinc} \left ( x \right )$')
        ax.set_xlabel(r'$x$')
        ax.set_ylabel(r'$y$')
        ax.set_title(r'Example Plot')
        ax.legend(loc = 'best')
        return mpl_plot

    def create_TraitedQWidget(self):
        self.traitedQWidget = TraitedQWidget()
        return self.traitedQWidget

    def create_DynamicChacoPlotQWidget(self):
        self.dynamicChacoPlot = DynamicChacoPlotQWidget();
        return self.dynamicChacoPlot



def ChacoInPySideUi_main(argv):
    # Don't create a new QApplication, it would unhook the Events
    # set by Traits on the existing QApplication. Simply use the
    # '.instance()' method to retrieve the existing one.
    app       = QtGui.QApplication.instance()
    ui        = ChacoInPySideUi()
    # Start the main event loop.
    sys.exit(app.exec_())




