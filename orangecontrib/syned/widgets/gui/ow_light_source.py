__author__ = 'labx'

import os, sys

from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtCore import QRect

from orangewidget import gui
from orangewidget import widget
from orangewidget.settings import Setting

from oasys.widgets.widget import OWWidget
from oasys.widgets import gui as oasysgui
from oasys.widgets import congruence
from oasys.widgets.gui import ConfirmDialog

from syned.storage_ring.light_source import LightSource, ElectronBeam
from syned.beamline.beamline import Beamline

class OWLightSource(OWWidget):

    maintainer = "Luca Rebuffi"
    maintainer_email = "luca.rebuffi(@at@)elettra.eu"
    category = "Syned Light Sources"
    keywords = ["data", "file", "load", "read"]

    outputs = [{"name":"SynedData",
                "type":Beamline,
                "doc":"Syned Beamline",
                "id":"data"}]

    source_name         = Setting("Undefined")

    electron_energy_in_GeV = Setting(2.0)
    electron_energy_spread = Setting(0.001)
    ring_current           = Setting(0.4)
    number_of_bunches      = Setting(400)

    moment_xx           = Setting(0.0)
    moment_xxp          = Setting(0.0)
    moment_xpxp         = Setting(0.0)
    moment_yy           = Setting(0.0)
    moment_yyp          = Setting(0.0)
    moment_ypyp         = Setting(0.0)

    electron_beam_size_h       = Setting(0.0)
    electron_beam_divergence_h = Setting(0.0)
    electron_beam_size_v       = Setting(0.0)
    electron_beam_divergence_v = Setting(0.0)

    type_of_properties = Setting(0)

    want_main_area=0

    MAX_WIDTH = 460
    MAX_HEIGHT = 700

    TABS_AREA_HEIGHT = 625
    CONTROL_AREA_WIDTH = 450

    def __init__(self):
        super().__init__()

        self.runaction = widget.OWAction("Send Data", self)
        self.runaction.triggered.connect(self.send_data)
        self.addAction(self.runaction)

        button_box = oasysgui.widgetBox(self.controlArea, "", addSpace=False, orientation="horizontal")

        button = gui.button(button_box, self, "Send Data", callback=self.send_data)
        font = QFont(button.font())
        font.setBold(True)
        button.setFont(font)
        palette = QPalette(button.palette()) # make a copy of the palette
        palette.setColor(QPalette.ButtonText, QColor('Dark Blue'))
        button.setPalette(palette) # assign new palette
        button.setFixedHeight(45)

        button = gui.button(button_box, self, "Reset Fields", callback=self.callResetSettings)
        font = QFont(button.font())
        font.setItalic(True)
        button.setFont(font)
        palette = QPalette(button.palette()) # make a copy of the palette
        palette.setColor(QPalette.ButtonText, QColor('Dark Red'))
        button.setPalette(palette) # assign new palette
        button.setFixedHeight(45)
        button.setFixedWidth(150)

        gui.separator(self.controlArea)

        geom = QApplication.desktop().availableGeometry()
        self.setGeometry(QRect(round(geom.width()*0.05),
                               round(geom.height()*0.05),
                               round(min(geom.width()*0.98, self.MAX_WIDTH)),
                               round(min(geom.height()*0.95, self.MAX_HEIGHT))))

        self.setMaximumHeight(self.geometry().height())
        self.setMaximumWidth(self.geometry().width())

        self.controlArea.setFixedWidth(self.CONTROL_AREA_WIDTH)

        tabs_setting = oasysgui.tabWidget(self.controlArea)
        tabs_setting.setFixedHeight(self.TABS_AREA_HEIGHT)
        tabs_setting.setFixedWidth(self.CONTROL_AREA_WIDTH-5)

        self.tab_sou = oasysgui.createTabPage(tabs_setting, "Light Source Setting")

        oasysgui.lineEdit(self.tab_sou, self, "source_name", "Light Source Name", labelWidth=260, valueType=str, orientation="horizontal")

        self.electron_beam_box = oasysgui.widgetBox(self.tab_sou, "Electron Beam/Machine Parameters", addSpace=False, orientation="vertical")

        oasysgui.lineEdit(self.electron_beam_box, self, "electron_energy_in_GeV", "Energy [GeV]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.electron_beam_box, self, "electron_energy_spread", "Energy Spread", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.electron_beam_box, self, "ring_current", "Ring Current [A]", labelWidth=260, valueType=float, orientation="horizontal")

        gui.comboBox(self.electron_beam_box, self, "type_of_properties", label="Electron Beam Properties", labelWidth=350,
                     items=["From 2nd Moments", "From Size/Divergence"],
                     callback=self.set_TypeOfProperties,
                     sendSelectedValue=False, orientation="horizontal")

        self.left_box_2_1 = oasysgui.widgetBox(self.electron_beam_box, "", addSpace=False, orientation="vertical", height=150)

        oasysgui.lineEdit(self.left_box_2_1, self, "moment_xx", "Moment xx   [m^2]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.left_box_2_1, self, "moment_xxp", "Moment xxp  [m.rad]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.left_box_2_1, self, "moment_xpxp", "Moment xpxp [rad^2]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.left_box_2_1, self, "moment_yy", "Moment yy   [m^2]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.left_box_2_1, self, "moment_yyp", "Moment yyp  [m.rad]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.left_box_2_1, self, "moment_ypyp", "Moment ypyp [rad^2]", labelWidth=260, valueType=float, orientation="horizontal")


        self.left_box_2_2 = oasysgui.widgetBox(self.electron_beam_box, "", addSpace=False, orientation="vertical", height=150)

        oasysgui.lineEdit(self.left_box_2_2, self, "electron_beam_size_h",       "Horizontal Beam Size [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.left_box_2_2, self, "electron_beam_size_v",       "Vertical Beam Size [m]",  labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.left_box_2_2, self, "electron_beam_divergence_h", "Horizontal Beam Divergence [rad]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.left_box_2_2, self, "electron_beam_divergence_v", "Vertical Beam Divergence [rad]", labelWidth=260, valueType=float, orientation="horizontal")

        self.set_TypeOfProperties()

        gui.rubber(self.controlArea)


    def set_TypeOfProperties(self):
        self.left_box_2_1.setVisible(self.type_of_properties==0)
        self.left_box_2_2.setVisible(self.type_of_properties==1)


    def check_data(self):
        congruence.checkStrictlyPositiveNumber(self.electron_energy_in_GeV , "Energy")
        congruence.checkStrictlyPositiveNumber(self.electron_energy_spread, "Energy Spread")
        congruence.checkStrictlyPositiveNumber(self.ring_current, "Ring Current")

        if self.type_of_properties == 0:
            congruence.checkPositiveNumber(self.moment_xx   , "Moment xx")
            congruence.checkPositiveNumber(self.moment_xpxp , "Moment xpxp")
            congruence.checkPositiveNumber(self.moment_yy   , "Moment yy")
            congruence.checkPositiveNumber(self.moment_ypyp , "Moment ypyp")
        else:
            congruence.checkPositiveNumber(self.electron_beam_size_h       , "Horizontal Beam Size")
            congruence.checkPositiveNumber(self.electron_beam_divergence_h , "Vertical Beam Size")
            congruence.checkPositiveNumber(self.electron_beam_size_v       , "Horizontal Beam Divergence")
            congruence.checkPositiveNumber(self.electron_beam_divergence_v , "Vertical Beam Divergence")

        self.check_magnetic_structure()


    def send_data(self):
        try:
            self.check_data()

            electron_beam = ElectronBeam(energy_in_GeV=self.electron_energy_in_GeV,
                                         energy_spread=self.electron_energy_spread,
                                         current=self.ring_current,
                                         number_of_bunches=self.number_of_bunches)

            if self.type_of_properties == 0:
                electron_beam._moment_xx   = self.moment_xx
                electron_beam._moment_xxp  = self.moment_xxp
                electron_beam._moment_xpxp = self.moment_xpxp
                electron_beam._moment_yy   = self.moment_yy
                electron_beam._moment_yyp  = self.moment_yyp
                electron_beam._moment_ypyp = self.moment_ypyp

                x, xp, y, yp = electron_beam.get_sigmas_all()

                self.electron_beam_size_h = x
                self.electron_beam_size_v = y
                self.electron_beam_divergence_h = xp
                self.electron_beam_divergence_v = yp
            else:
                electron_beam.set_sigmas_all(sigma_x=self.electron_beam_size_h,
                                             sigma_y=self.electron_beam_size_v,
                                             sigma_xp=self.electron_beam_divergence_h,
                                             sigma_yp=self.electron_beam_divergence_v)

                self.moment_xx = electron_beam._moment_xx
                self.moment_xpxp = electron_beam._moment_xpxp
                self.moment_yy = electron_beam._moment_yy
                self.moment_ypyp = electron_beam._moment_ypyp

            light_source = LightSource(name=self.source_name,
                                       electron_beam = electron_beam,
                                       magnetic_structure = self.get_magnetic_structure())

            self.send("SynedData", Beamline(light_source=light_source))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e.args[0]), QMessageBox.Ok)

            self.setStatusMessage("")
            self.progressBarFinished()

    def check_magnetic_structure(self):
        raise NotImplementedError("Shoudl be implemented in subclasses")

    def get_magnetic_structure(self):
        raise NotImplementedError("Shoudl be implemented in subclasses")

    def callResetSettings(self):
        if ConfirmDialog.confirmed(parent=self, message="Confirm Reset of the Fields?"):
            try:
                self.resetSettings()
            except:
                pass
