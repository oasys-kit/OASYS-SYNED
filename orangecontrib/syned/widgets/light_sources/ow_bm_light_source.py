import sys

from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtGui import QPalette, QColor, QFont

from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui
from oasys.widgets import congruence

from syned.storage_ring.magnetic_structures.bending_magnet import BendingMagnet

from orangecontrib.syned.widgets.gui import ow_light_source

class OWBMLightSource(ow_light_source.OWLightSource):

    name = "BM Light Source"
    description = "Syned: BM Light Source"
    icon = "icons/bm.png"
    priority = 1

    radius         = Setting(0.0)
    magnetic_field = Setting(0.0)
    length         = Setting(0.0)

    def __init__(self):
        super().__init__()

        left_box_1 = oasysgui.widgetBox(self.tab_sou, "BM Parameters", addSpace=True, orientation="vertical")

        oasysgui.lineEdit(left_box_1, self, "radius", "Radius [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(left_box_1, self, "magnetic_field", "Magnetic Field [T]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(left_box_1, self, "length", "Length [m]", labelWidth=260, valueType=float, orientation="horizontal")

    def check_magnetic_structure(self):
        congruence.checkStrictlyPositiveNumber(self.radius , "Radius")
        congruence.checkStrictlyPositiveNumber(self.magnetic_field, "Magnetic Field")
        congruence.checkStrictlyPositiveNumber(self.length, "Length")

    def get_magnetic_structure(self):
        return BendingMagnet(radius=self.radius,
                             magnetic_field=self.magnetic_field,
                             length=self.length)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    ow = OWBMLightSource()
    ow.show()
    a.exec_()
    #ow.saveSettings()
