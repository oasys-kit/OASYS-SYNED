import numpy

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui
from oasys.widgets import congruence
from oasys.util.oasys_util import ChemicalFormulaParser

from orangecontrib.syned.widgets.gui.ow_optical_element import OWOpticalElement

from syned.beamline.optical_elements.mirrors.mirror import Mirror
from syned.beamline.shape import *


class OWMirror(OWOpticalElement):

    name = "Mirror"
    description = "Syned: Mirror"
    icon = "icons/mirror.png"
    priority = 6

    horizontal_shift = Setting(0.0)
    vertical_shift = Setting(0.0)
    
    # BOUNDARY
    
    width = Setting(0.0)
    height = Setting(0.0)
    radius = Setting(0.0)

    min_ax = Setting(0.0)
    maj_ax = Setting(0.0)
    
    # SURFACE
    
    convexity = Setting(0)
    is_cylinder = Setting(1)
    cylinder_direction = Setting(0)
    
    p_surface = Setting(0.0)
    q_surface = Setting(0.0)

    calculate_sphere_parameter = Setting(0)
    calculate_ellipsoid_parameter = Setting(0)
    calculate_paraboloid_parameter = Setting(0)
    calculate_hyperboloid_parameter = Setting(0)
    calculate_torus_parameter = Setting(0)


    # SPHERE
    radius_surface = Setting(0.0)
    
    # ELLIPSOID/HYPERBOLOID
    min_ax_surface = Setting(0.0)
    maj_ax_surface = Setting(0.0)

    # PARABOLOID
    parabola_parameter_surface = Setting(0.0)
    
    # TORUS
    min_radius_surface = Setting(0.0)
    maj_radius_surface = Setting(0.0)

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

        self.surface_shape_box = oasysgui.widgetBox(self.tab_mir, "Surface Shape", addSpace=True, orientation="vertical", height=160)

        gui.comboBox(self.surface_shape_box, self, "surface_shape", label="Mirror Surface Shape", labelWidth=350,
                     items=["Plane", "Sphere", "Ellipsoid", "Paraboloid", "Hyperboloid", "Torus"],
                     callback=self.set_SurfaceParameters,
                     sendSelectedValue=False, orientation="horizontal")


        self.plane_box = oasysgui.widgetBox(self.surface_shape_box, "", addSpace=False, orientation="vertical", height=90)

        self.sphere_box = oasysgui.widgetBox(self.surface_shape_box, "", addSpace=False, orientation="vertical", height=90)
        self.ellipsoid_box = oasysgui.widgetBox(self.surface_shape_box, "", addSpace=False, orientation="vertical", height=90)
        self.paraboloid_box = oasysgui.widgetBox(self.surface_shape_box, "", addSpace=False, orientation="vertical", height=90)
        self.hyperboloid_box = oasysgui.widgetBox(self.surface_shape_box, "", addSpace=False, orientation="vertical", height=90)
        self.torus_box = oasysgui.widgetBox(self.surface_shape_box, "", addSpace=False, orientation="vertical", height=90)

        # SPHERE -------------------------- 
        
        gui.comboBox(self.sphere_box, self, "calculate_sphere_parameter", label="Sphere Shape", labelWidth=350,
                     items=["Manual", "Automatic"],
                     callback=self.set_SphereShape,
                     sendSelectedValue=False, orientation="horizontal")

        self.sphere_box_1 = oasysgui.widgetBox(self.sphere_box, "", addSpace=False, orientation="vertical", height=60)
        self.sphere_box_2 = oasysgui.widgetBox(self.sphere_box, "", addSpace=False, orientation="vertical", height=60)

        oasysgui.lineEdit(self.sphere_box_1, self, "radius_surface", "Radius [m]", labelWidth=260, valueType=float, orientation="horizontal")

        oasysgui.lineEdit(self.sphere_box_2, self, "p_surface", "First Focus to Mirror Center (P) [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.sphere_box_2, self, "q_surface", "Mirror Center to Second Focus (Q) [m]", labelWidth=260, valueType=float, orientation="horizontal")


        # ELLIPSOID -------------------------- 
        
        gui.comboBox(self.ellipsoid_box, self, "calculate_ellipsoid_parameter", label="Ellipsoid Shape", labelWidth=350,
                     items=["Manual", "Automatic"],
                     callback=self.set_EllipsoidShape,
                     sendSelectedValue=False, orientation="horizontal")

        self.ellipsoid_box_1 = oasysgui.widgetBox(self.ellipsoid_box, "", addSpace=False, orientation="vertical", height=60)
        self.ellipsoid_box_2 = oasysgui.widgetBox(self.ellipsoid_box, "", addSpace=False, orientation="vertical", height=60)

        oasysgui.lineEdit(self.ellipsoid_box_1, self, "min_ax_surface", "Minor Axis [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.ellipsoid_box_1, self, "maj_ax_surface", "Major Axis [m]", labelWidth=260, valueType=float, orientation="horizontal")

        oasysgui.lineEdit(self.ellipsoid_box_2, self, "p_surface", "First Focus to Mirror Center (P) [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.ellipsoid_box_2, self, "q_surface", "Mirror Center to Second Focus (Q) [m]", labelWidth=260, valueType=float, orientation="horizontal")


        # PARABOLOID -------------------------- 
        
        gui.comboBox(self.paraboloid_box, self, "calculate_paraboloid_parameter", label="Sphere Shape", labelWidth=350,
                     items=["Manual", "Automatic"],
                     callback=self.set_ParaboloidShape,
                     sendSelectedValue=False, orientation="horizontal")

        self.paraboloid_box_1 = oasysgui.widgetBox(self.paraboloid_box, "", addSpace=False, orientation="vertical", height=60)
        self.paraboloid_box_2 = oasysgui.widgetBox(self.paraboloid_box, "", addSpace=False, orientation="vertical", height=60)

        oasysgui.lineEdit(self.paraboloid_box_1, self, "parabola_parameter_surface", "Parabola Parameter [m]", labelWidth=260, valueType=float, orientation="horizontal")

        oasysgui.lineEdit(self.paraboloid_box_2, self, "p_surface", "First Focus to Mirror Center (P) [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.paraboloid_box_2, self, "q_surface", "Mirror Center to Second Focus (Q) [m]", labelWidth=260, valueType=float, orientation="horizontal")

        # HYPERBOLOID --------------------------
        
        gui.comboBox(self.hyperboloid_box, self, "calculate_hyperboloid_parameter", label="Hyperboloid Shape", labelWidth=350,
                     items=["Manual", "Automatic"],
                     callback=self.set_HyperboloidShape,
                     sendSelectedValue=False, orientation="horizontal")

        self.hyperboloid_box_1 = oasysgui.widgetBox(self.hyperboloid_box, "", addSpace=False, orientation="vertical", height=60)
        self.hyperboloid_box_2 = oasysgui.widgetBox(self.hyperboloid_box, "", addSpace=False, orientation="vertical", height=60)

        oasysgui.lineEdit(self.hyperboloid_box_1, self, "min_ax_surface", "Minor Axis [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.hyperboloid_box_1, self, "maj_ax_surface", "Major Axis [m]", labelWidth=260, valueType=float, orientation="horizontal")

        oasysgui.lineEdit(self.hyperboloid_box_2, self, "p_surface", "First Focus to Mirror Center (P) [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.hyperboloid_box_2, self, "q_surface", "Mirror Center to Second Focus (Q) [m]", labelWidth=260, valueType=float, orientation="horizontal")


        # TORUS -------------------------- 
        
        gui.comboBox(self.torus_box, self, "calculate_torus_parameter", label="Torus Shape", labelWidth=350,
                     items=["Manual", "Automatic"],
                     callback=self.set_TorusShape,
                     sendSelectedValue=False, orientation="horizontal")

        self.torus_box_1 = oasysgui.widgetBox(self.torus_box, "", addSpace=False, orientation="vertical", height=60)
        self.torus_box_2 = oasysgui.widgetBox(self.torus_box, "", addSpace=False, orientation="vertical", height=60)

        oasysgui.lineEdit(self.torus_box_1, self, "min_radius_surface", "Minor radius [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.torus_box_1, self, "maj_radius_surface", "Major radius [m]", labelWidth=260, valueType=float, orientation="horizontal")

        oasysgui.lineEdit(self.torus_box_2, self, "p_surface", "First Focus to Mirror Center (P) [m]", labelWidth=260, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(self.torus_box_2, self, "q_surface", "Mirror Center to Second Focus (Q) [m]", labelWidth=260, valueType=float, orientation="horizontal")

        # -----------------------------------------------------
        # -----------------------------------------------------
        
        self.surface_orientation_box = oasysgui.widgetBox(self.tab_mir, "Surface Orientation", addSpace=False, orientation="vertical")

        gui.comboBox(self.surface_orientation_box, self, "convexity", label="Convexity", labelWidth=350,
                     items=["Upward", "Downward"],
                     sendSelectedValue=False, orientation="horizontal")

        gui.comboBox(self.surface_orientation_box, self, "is_cylinder", label="Cylinder", labelWidth=350,
                     items=["No", "Yes"], callback=self.set_Cylinder,
                     sendSelectedValue=False, orientation="horizontal")

        self.cylinder_box_1 = oasysgui.widgetBox(self.surface_orientation_box, "", addSpace=False, orientation="vertical", height=25)
        self.cylinder_box_2 = oasysgui.widgetBox(self.surface_orientation_box, "", addSpace=False, orientation="vertical", height=25)

        gui.comboBox(self.cylinder_box_1, self, "cylinder_direction", label="Cylinder Direction", labelWidth=350,
                     items=["Tangential", "Sagittal"],
                     sendSelectedValue=False, orientation="horizontal")

        self.set_SurfaceParameters()


        self.coating_box = oasysgui.widgetBox(self.tab_mir, "Coating", addSpace=True, orientation="vertical")

        oasysgui.lineEdit(self.coating_box, self, "coating_material", "Material [Chemical Formula]", labelWidth=180, valueType=str, orientation="horizontal")
        oasysgui.lineEdit(self.coating_box, self, "coating_thickness", "Thickness [m]", labelWidth=260, valueType=float, orientation="horizontal")

    def set_SphereShape(self):
        self.sphere_box_1.setVisible(self.calculate_sphere_parameter==0)
        self.sphere_box_2.setVisible(self.calculate_sphere_parameter==1)

    def set_EllipsoidShape(self):
        self.ellipsoid_box_1.setVisible(self.calculate_ellipsoid_parameter==0)
        self.ellipsoid_box_2.setVisible(self.calculate_ellipsoid_parameter==1)

    def set_ParaboloidShape(self):
        self.paraboloid_box_1.setVisible(self.calculate_paraboloid_parameter==0)
        self.paraboloid_box_2.setVisible(self.calculate_paraboloid_parameter==1)

    def set_HyperboloidShape(self):
        self.hyperboloid_box_1.setVisible(self.calculate_hyperboloid_parameter==0)
        self.hyperboloid_box_2.setVisible(self.calculate_hyperboloid_parameter==1)

    def set_TorusShape(self):
        self.torus_box_1.setVisible(self.calculate_torus_parameter==0)
        self.torus_box_2.setVisible(self.calculate_torus_parameter==1)

    def set_Shape(self):
        self.rectangle_box.setVisible(self.shape == 0)
        self.circle_box.setVisible(self.shape == 1)
        self.ellipse_box.setVisible(self.shape == 2)

    def set_Cylinder(self):
        self.cylinder_box_1.setVisible(self.is_cylinder==1)
        self.cylinder_box_2.setVisible(self.is_cylinder==0)

    def set_SurfaceParameters(self):
        self.plane_box.setVisible(self.surface_shape == 0)

        if self.surface_shape == 1 :
            self.sphere_box.setVisible(True)
            self.set_SphereShape()
        else:
            self.sphere_box.setVisible(False)
        
        if self.surface_shape == 2 :
            self.ellipsoid_box.setVisible(True)
            self.set_EllipsoidShape()
        else:
            self.ellipsoid_box.setVisible(False)

        if self.surface_shape == 3 :
            self.paraboloid_box.setVisible(True)
            self.set_ParaboloidShape()
        else:
            self.paraboloid_box.setVisible(False)

        if self.surface_shape == 4 :
            self.hyperboloid_box.setVisible(True)
            self.set_HyperboloidShape()
        else:
            self.hyperboloid_box.setVisible(False)

        if self.surface_shape == 5 :
            self.torus_box.setVisible(True)
            self.set_TorusShape()
        else:
            self.torus_box.setVisible(False)

        if self.surface_shape in (1,2,3,4):
            self.surface_orientation_box.setVisible(True)
            self.set_Cylinder()
        else:
            self.surface_orientation_box.setVisible(False)

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

        # SPHERE --------------------------
        elif self.surface_shape == 1:
            if self.calculate_sphere_parameter == 0:
                if self.is_cylinder == 0:
                    surface_shape = Sphere(radius=self.radius_surface,
                                           convexity=self.convexity)
                else:
                    surface_shape = SphericalCylinder(radius=self.radius_surface,
                                                      convexity=self.convexity,
                                                      cylinder_direction=self.cylinder_direction)
            elif self.calculate_sphere_parameter == 1:
                if self.is_cylinder == 0:
                    surface_shape = Sphere(convexity=self.convexity)
                else:
                    surface_shape = SphericalCylinder(convexity=self.convexity,
                                                      cylinder_direction=self.cylinder_direction)

                surface_shape.initialize_from_p_q(self.p_surface, self.q_surface, numpy.radians(90-self.angle_radial))

                self.radius_surface = round(surface_shape._radius, 4)

        # ELLIPSOID --------------------------
        elif self.surface_shape == 2:
            if self.calculate_ellipsoid_parameter == 0:
                if self.is_cylinder == 0:
                    surface_shape = Ellipsoid(min_axis=self.min_ax_surface,
                                              maj_axis=self.maj_ax_surface,
                                              convexity=self.convexity)
                else:
                    surface_shape = EllipticalCylinder(min_axis=self.min_ax_surface,
                                                       maj_axis=self.maj_ax_surface,
                                                       convexity=self.convexity,
                                                       cylinder_direction=self.cylinder_direction)
            elif self.calculate_ellipsoid_parameter == 1:
                if self.is_cylinder == 0:
                    surface_shape = Ellipsoid(convexity=self.convexity)
                else:
                    surface_shape = EllipticalCylinder(convexity=self.convexity,
                                                       cylinder_direction=self.cylinder_direction)

                surface_shape.initialize_from_p_q(self.p_surface, self.q_surface, numpy.radians(90-self.angle_radial))

                self.min_ax_surface = round(surface_shape._min_axis, 4)
                self.maj_ax_surface = round(surface_shape._maj_axis, 4)

        # PARABOLOID --------------------------
        elif self.surface_shape == 3:
            if self.calculate_paraboloid_parameter == 0:
                if self.is_cylinder == 0:
                    surface_shape = Paraboloid(parabola_parameter=self.parabola_parameter_surface,
                                               convexity=self.convexity)
                else:
                    surface_shape = ParabolicCylinder(parabola_parameter=self.parabola_parameter_surface,
                                                      convexity=self.convexity,
                                                      cylinder_direction=self.cylinder_direction)
            elif self.calculate_paraboloid_parameter == 1:
                if self.is_cylinder == 0:
                    surface_shape = Paraboloid(convexity=self.convexity)
                else:
                    surface_shape = ParabolicCylinder(convexity=self.convexity,
                                                    cylinder_direction=self.cylinder_direction)

                surface_shape.initialize_from_p_q(self.p_surface, self.q_surface, numpy.radians(90-self.angle_radial))

                self.parabola_parameter_surface = round(surface_shape._parabola_parameter, 4)

        # HYPERBOLOID --------------------------
        elif self.surface_shape == 4:
            if self.calculate_hyperboloid_parameter == 0:
                if self.is_cylinder == 0:
                    surface_shape = Hyperboloid(min_axis=self.min_ax_surface,
                                                maj_axis=self.maj_ax_surface,
                                                convexity=self.convexity)
                else:
                    surface_shape = HyperbolicCylinder(min_axis=self.min_ax_surface,
                                                       maj_axis=self.maj_ax_surface,
                                                       convexity=self.convexity,
                                                       cylinder_direction=self.cylinder_direction)
            elif self.calculate_ellipsoid_parameter == 1:
                raise NotImplementedError("HYPERBOLOID, you should not be here!")

        # TORUS --------------------------
        elif self.surface_shape == 5:
            if self.calculate_torus_parameter == 0:
                surface_shape = Torus(min_radius=self.min_radius_surface,
                                      maj_radius=self.maj_radius_surface,
                                      convexity=self.convexity)
            elif self.calculate_torus_parameter == 1:
                surface_shape = Torus(convexity=self.convexity)

                surface_shape.initialize_from_p_q(self.p_surface, self.q_surface, numpy.radians(90-self.angle_radial))

                self.min_radius_surface = round(surface_shape._min_radius, 4)
                self.maj_radius_surface = round(surface_shape._maj_radius, 4)



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

        if self.surface_shape == 1: # SPHERE
            if self.calculate_sphere_parameter == 0:
                congruence.checkStrictlyPositiveNumber(self.radius_surface, "(Surface) Radius")
            elif self.calculate_sphere_parameter == 1:
                congruence.checkStrictlyPositiveNumber(self.p_surface, "(Surface) P")

        if self.surface_shape == 2: # ELLIPSOID
            if self.calculate_ellipsoid_parameter == 0:
                congruence.checkStrictlyPositiveNumber(self.min_ax_surface, "(Surface) Minor Axis")
                congruence.checkStrictlyPositiveNumber(self.maj_ax_surface, "(Surface) Major Axis")
            elif self.calculate_ellipsoid_parameter == 1:
                congruence.checkStrictlyPositiveNumber(self.p_surface, "(Surface) P")
                congruence.checkStrictlyPositiveNumber(self.q_surface, "(Surface) Q")

                if self.is_cylinder and self.cylinder_direction == Direction.SAGITTAL:
                    raise NotImplementedError("Sagittal automatic calculation is not supported, yet")

        if self.surface_shape == 3: # PARABOLOID
            if self.calculate_paraboloid_parameter == 0:
                congruence.checkStrictlyPositiveNumber(self.parabola_parameter_surface, "(Surface) Parabola Parameter")
            elif self.calculate_paraboloid_parameter == 1:
                congruence.checkStrictlyPositiveNumber(self.p_surface, "(Surface) P")
                congruence.checkStrictlyPositiveNumber(self.q_surface, "(Surface) Q")

                if self.is_cylinder and self.cylinder_direction == Direction.SAGITTAL:
                    raise NotImplementedError("Sagittal automatic calculation is not supported, yet")

        if self.surface_shape == 4: # HYPERBOLOID
            if self.calculate_hyperboloid_parameter == 0:
                congruence.checkStrictlyPositiveNumber(self.min_ax_surface, "(Surface) Minor Axis")
                congruence.checkStrictlyPositiveNumber(self.maj_ax_surface, "(Surface) Major Axis")
            elif self.calculate_hyperboloid_parameter == 1:
                raise NotImplementedError("Automatic calculation is not supported, yet")

        if self.surface_shape == 5: # TORUS
            if self.calculate_torus_parameter == 0:
                congruence.checkStrictlyPositiveNumber(self.min_radius_surface, "(Surface) Minor Radius")
                congruence.checkStrictlyPositiveNumber(self.maj_radius_surface, "(Surface) Major Radius")
            elif self.calculate_torus_parameter == 1:
                congruence.checkStrictlyPositiveNumber(self.p_surface, "(Surface) P")
                congruence.checkStrictlyPositiveNumber(self.q_surface, "(Surface) Q")


        congruence.checkEmptyString(self.coating_material, "Coating Material")
        ChemicalFormulaParser.parse_formula(self.coating_material)
        congruence.checkStrictlyPositiveNumber(self.coating_thickness, "Coating Thickness")
