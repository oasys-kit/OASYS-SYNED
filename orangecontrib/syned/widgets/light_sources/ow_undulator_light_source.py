import sys

from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtGui import QPalette, QColor, QFont

from syned.storage_ring.magnetic_structures.undulator import Undulator

from orangecontrib.syned.widgets.gui import ow_insertion_device

class UndulatorLightSource(ow_insertion_device.InsertionDevice):

    name = "Undulator Light Source"
    description = "Syned: Undulator Light Source"
    icon = "icons/undulator.png"
    priority = 2

    def __init__(self):
        super().__init__()

    def get_magnetic_structure(self):
        return Undulator(K_horizontal=self.K_horizontal,
                         K_vertical=self.K_vertical,
                         period_length=self.period_length,
                         number_of_periods=self.number_of_periods)


if __name__ == "__main__":
    a = QApplication(sys.argv)
    ow = UndulatorLightSource()
    ow.show()
    a.exec_()
    #ow.saveSettings()
