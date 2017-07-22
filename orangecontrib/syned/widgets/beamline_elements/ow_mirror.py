import numpy

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui
from oasys.widgets import congruence
from oasys.util.oasys_util import ChemicalFormulaParser

from orangecontrib.syned.widgets.gui.ow_optical_element import OWOpticalElement

from syned.beamline.optical_elements.mirrors.mirror import Mirror
from syned.beamline.shape import Rectangle, Ellipse, Ellipsoid, Plane


class OWMirror(OWOpticalElement):

    name = "Mirror"
    description = "Syned: Mirror"
    icon = "icons/mirror.png"
    priority = 6

    horizontal_shift = Setting(0.0)
    vertical_shift = Setting(0.0)

    width = Setting(0.0)
    height = Setting(0.0)
    radius = Setting(0.0)

    min_ax = Setting(0.0)
    maj_ax = Setting(0.0)

    calculate_ellipsoid_parameter = Setting(0)
    min_ax_surface = Setting(0.0)
    maj_ax_surface = Setting(0.0)
    p_surface = Setting(0.0)
    q_surface = Setting(0.0)

    coating_material = Setting("")
    coating_thickness = Setting(0.0)

    def __init__(self):
        super().__init__()


    def draw_specific_box(self):

        self.shape_box = oasysgui.widgetBox(self.tab_bas, "Boundary Shape", addSpace=True, orientation="vertical")

        gui.comboBox(self.shape_box, self, "shape", label="Mirror Boundary Shape", labelWidth=350,
                     items=["Rectangle", "Circle", "Ellipse"],
                     callback=self.set_Shape,
                     sendSelectedValue=False, orientation="horizontal")

        oasysgui.lineEdit(self.shape_box, self, "horizontal_shift", "Horizontal Shift [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.shape_box, self, "vertical_shift", "Vertical Shift [m]", labelWidth=260, valueType=float, orientation="horizontal")

        self.rectangle_box = oasysgui.widgetBox(self.shape_box, "", addSpace=False, orientation="vertical", height=60)

        oasysgui.lineEdit(self.rectangle_box, self, "width", "Width [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.rectangle_box, self, "height", "Height [m]", labelWidth=260, valueType=float, orientation="horizontal")

        self.circle_box = oasysgui.widgetBox(self.shape_box, "", addSpace=False, orientation="vertical", height=60)

        oasysgui.lineEdit(self.circle_box, self, "radius", "Radius [m]", labelWidth=260, valueType=float, orientation="horizontal")

        self.ellipse_box = oasysgui.widgetBox(self.shape_box, "", addSpace=False, orientation="vertical", height=60)

        oasysgui.lineEdit(self.ellipse_box, self, "min_ax", "Minor Axis [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.ellipse_box, self, "maj_ax", "Major Axis [m]", labelWidth=260, valueType=float, orientation="horizontal")

        self.set_Shape()

        self.tab_mir = oasysgui.createTabPage(self.tabs_setting, "Mirror Setting")

        self.surface_shape_box = oasysgui.widgetBox(self.tab_mir, "Surface Shape", addSpace=True, orientation="vertical", height=250)

        gui.comboBox(self.surface_shape_box, self, "surface_shape", label="Mirror Surface Shape", labelWidth=350,
                     items=["Plane", "Ellipsoid"],
                     callback=self.set_SurfaceShape,
                     sendSelectedValue=False, orientation="horizontal")


        self.plane_box = oasysgui.widgetBox(self.surface_shape_box, "", addSpace=False, orientation="vertical", height=90)

        self.ellipsoid_box = oasysgui.widgetBox(self.surface_shape_box, "", addSpace=False, orientation="vertical", height=90)

        gui.comboBox(self.ellipsoid_box, self, "calculate_ellipsoid_parameter", label="Ellispoid Shape", labelWidth=350,
                     items=["Manual", "Automatic"],
                     callback=self.set_EllipsoidShape,
                     sendSelectedValue=False, orientation="horizontal")

        self.ellipsoid_box_1 = oasysgui.widgetBox(self.ellipsoid_box, "", addSpace=False, orientation="vertical", height=60)
        self.ellipsoid_box_2 = oasysgui.widgetBox(self.ellipsoid_box, "", addSpace=False, orientation="vertical", height=60)

        oasysgui.lineEdit(self.ellipsoid_box_1, self, "min_ax_surface", "Minor Axis [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.ellipsoid_box_1, self, "maj_ax_surface", "Major Axis [m]", labelWidth=260, valueType=float, orientation="horizontal")

        oasysgui.lineEdit(self.ellipsoid_box_2, self, "p_surface", "First Focus to Mirror Center (P) [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.ellipsoid_box_2, self, "q_surface", "Mirror Center to Second Focus (Q) [m]", labelWidth=260, valueType=float, orientation="horizontal")

        self.set_SurfaceShape()

        self.coating_box = oasysgui.widgetBox(self.tab_mir, "Coating", addSpace=True, orientation="vertical")

        oasysgui.lineEdit(self.coating_box, self, "coating_material", "Material [Chemical Formula]", labelWidth=180, valueType=str, orientation="horizontal")
        oasysgui.lineEdit(self.coating_box, self, "coating_thickness", "Thickness [m]", labelWidth=260, valueType=float, orientation="horizontal")

    def set_EllipsoidShape(self):
        self.ellipsoid_box_1.setVisible(self.calculate_ellipsoid_parameter==0)
        self.ellipsoid_box_2.setVisible(self.calculate_ellipsoid_parameter==1)

    def set_Shape(self):
        self.rectangle_box.setVisible(self.shape == 0)
        self.circle_box.setVisible(self.shape == 1)
        self.ellipse_box.setVisible(self.shape == 2)

    def set_SurfaceShape(self):
        self.plane_box.setVisible(self.surface_shape == 0)

        if self.surface_shape == 1 :
            self.ellipsoid_box.setVisible(True)
            self.set_EllipsoidShape()
        else:
            self.ellipsoid_box.setVisible(False)


    def get_optical_element(self):
        if self.shape == 0:
            boundary_shape = Rectangle(x_left=-0.5*self.width + self.horizontal_shift,
                                       x_right=0.5*self.width + self.horizontal_shift,
                                       y_bottom=-0.5*self.height + self.vertical_shift,
                                       y_top=0.5*self.height + self.vertical_shift)

        elif self.shape == 1:
            boundary_shape = Ellipse(min_ax_left=-0.5*self.radius + self.horizontal_shift,
                                     min_ax_right=0.5*self.radius + self.horizontal_shift,
                                     maj_ax_left=-0.5*self.radius + self.vertical_shift,
                                     maj_ax_right=0.5*self.radius + self.vertical_shift)
        elif self.shape == 2:
            boundary_shape = Ellipse(min_ax_left=-0.5*self.min_ax + self.horizontal_shift,
                                     min_ax_right=0.5*self.min_ax + self.horizontal_shift,
                                     maj_ax_left=-0.5*self.maj_ax + self.vertical_shift,
                                     maj_ax_right=0.5*self.maj_ax + self.vertical_shift)



        if self.surface_shape == 0:
            surface_shape = Plane()
        elif self.surface_shape == 1:
            if self.calculate_ellipsoid_parameter == 0:
                surface_shape = Ellipsoid(min_axis=self.min_ax_surface,
                                          maj_axis=self.maj_ax_surface)
            elif self.calculate_ellipsoid_parameter == 1:
                surface_shape = Ellipsoid()
                surface_shape.initialize_from_p_q(self.p_surface, self.q_surface, numpy.radians(90-self.angle_radial))

                self.min_ax_surface = round(surface_shape._min_axis, 4)
                self.maj_ax_surface = round(surface_shape._maj_axis, 4)

        mirror = Mirror(name=self.oe_name,
                        boundary_shape=boundary_shape,
                        surface_shape=surface_shape,
                        coating=self.coating_material,
                        coating_thickness=self.coating_thickness)

        return mirror

    def check_data(self):
        super().check_data()

        congruence.checkNumber(self.horizontal_shift, "Horizontal Shift")
        congruence.checkNumber(self.vertical_shift, "Vertical Shift")

        if self.shape == 0:
            congruence.checkStrictlyPositiveNumber(self.width, "Width")
            congruence.checkStrictlyPositiveNumber(self.height, "Height")
        elif self.shape == 1:
            congruence.checkStrictlyPositiveNumber(self.radius, "Radius")
        elif self.shape == 2:
            congruence.checkStrictlyPositiveNumber(self.min_ax, "(Boundary) Minor Axis")
            congruence.checkStrictlyPositiveNumber(self.maj_ax, "(Boundary) Major Axis")

        if self.surface_shape == 1:
            if self.calculate_ellipsoid_parameter == 0:
                congruence.checkStrictlyPositiveNumber(self.min_ax_surface, "(Surface) Minor Axis")
                congruence.checkStrictlyPositiveNumber(self.maj_ax_surface, "(Surface) Major Axis")
            elif self.calculate_ellipsoid_parameter == 1:
                congruence.checkStrictlyPositiveNumber(self.p_surface, "(Surface) P")
                congruence.checkStrictlyPositiveNumber(self.q_surface, "(Surface) Q")

        congruence.checkEmptyString(self.coating_material, "Coating Material")
        ChemicalFormulaParser.parse_formula(self.coating_material)
        congruence.checkStrictlyPositiveNumber(self.coating_thickness, "Coating Thickness")
