import os, sys

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui
from oasys.widgets import congruence

from orangecontrib.syned.widgets.gui.ow_optical_element import OWOpticalElement

from syned.beamline.optical_elements.absorbers.beam_stopper import BeamStopper
from syned.beamline.shape import Rectangle, Ellipse

class OWBeamStopper(OWOpticalElement):

    name = "Beam Stopper"
    description = "Syned: Beam Stopper"
    icon = "icons/beam_stopper.png"
    priority = 1

    horizontal_shift = Setting(0.0)
    vertical_shift = Setting(0.0)

    width = Setting(0.0)
    height = Setting(0.0)
    radius = Setting(0.0)

    def __init__(self):
        super().__init__()


    def draw_specific_box(self):

        self.shape_box = oasysgui.widgetBox(self.tab_bas, "Shape", addSpace=True, orientation="vertical")

        gui.comboBox(self.shape_box, self, "shape", label="Beam Stopper Shape", labelWidth=350,
                     items=["Rectangle", "Circle"],
                     callback=self.set_Shape,
                     sendSelectedValue=False, orientation="horizontal")

        oasysgui.lineEdit(self.shape_box, self, "horizontal_shift", "Horizontal Shift [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.shape_box, self, "vertical_shift", "Vertical Shift [m]", labelWidth=260, valueType=float, orientation="horizontal")

        self.rectangle_box = oasysgui.widgetBox(self.shape_box, "", addSpace=False, orientation="vertical", height=60)

        oasysgui.lineEdit(self.rectangle_box, self, "width", "Width [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.rectangle_box, self, "height", "Height [m]", labelWidth=260, valueType=float, orientation="horizontal")

        self.circle_box = oasysgui.widgetBox(self.shape_box, "", addSpace=False, orientation="vertical", height=60)

        oasysgui.lineEdit(self.circle_box, self, "radius", "Radius [m]", labelWidth=260, valueType=float, orientation="horizontal")

        self.set_Shape()

    def set_Shape(self):
        self.rectangle_box.setVisible(self.shape == 0)
        self.circle_box.setVisible(self.shape == 1)

    def get_optical_element(self):
        if self.shape == 0:
            boundary_shape = Rectangle(x_left=-0.5*self.width + self.horizontal_shift,
                                       x_right=0.5*self.width + self.horizontal_shift,
                                       y_bottom=-0.5*self.height + self.vertical_shift,
                                       y_top=0.5*self.height + self.vertical_shift)

        elif self.shape == 1:
            boundary_shape = Ellipse(min_ax_left=-0.5*self.radius + self.horizontal_shift,
                                     min_ax_right=0.5*self.radius + self.horizontal_shift,
                                     maj_ax_bottom=-0.5*self.radius + self.vertical_shift,
                                     maj_ax_top=0.5*self.radius + self.vertical_shift)


        return  BeamStopper(boundary_shape=boundary_shape)

    def check_data(self):
        super().check_data()

        congruence.checkNumber(self.horizontal_shift, "Horizontal Shift")
        congruence.checkNumber(self.vertical_shift, "Vertical Shift")

        if self.shape == 0:
            congruence.checkStrictlyPositiveNumber(self.width, "Width")
            congruence.checkStrictlyPositiveNumber(self.height, "Height")
        elif self.shape == 1:
            congruence.checkStrictlyPositiveNumber(self.radius, "Radius")


