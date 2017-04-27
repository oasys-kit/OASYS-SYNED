import sys

from PyQt4.QtGui import QPalette, QColor, QFont, QMessageBox, QApplication
from orangewidget import gui
from orangewidget import widget
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui
from oasys.widgets import congruence

from syned.storage_ring.light_source import LightSource, ElectronBeam, MagneticStructure

from orangecontrib.syned.widgets.gui import ow_insertion_device

class UndulatorLightSource(ow_insertion_device.InsertionDevice):

    name = "Undulator Light Source"
    description = "Syned: Undulator Light Source"
    icon = "icons/undulator.png"
    priority = 2

    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    a = QApplication(sys.argv)
    ow = UndulatorLightSource()
    ow.show()
    a.exec_()
    #ow.saveSettings()
