import sys, numpy,  scipy.constants as codata

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui
from oasys.widgets import congruence

from syned.storage_ring.magnetic_structures.undulator import Undulator

from orangecontrib.syned.widgets.gui import ow_insertion_device

from PyQt5.QtWidgets import QTextEdit

m2ev = codata.c * codata.h / codata.e

VERTICAL = 1
HORIZONTAL = 2
BOTH = 3

class OWUndulatorLightSource(ow_insertion_device.OWInsertionDevice):

    name = "Undulator Light Source"
    description = "Syned: Undulator Light Source"
    icon = "icons/undulator.png"
    priority = 2

    auto_energy = Setting(0.0)
    auto_harmonic_number = Setting(1)

    def __init__(self):
        super().__init__()

        tab_util = oasysgui.createTabPage(self.tabs_setting, "Utility")

        left_box_0 = oasysgui.widgetBox(tab_util, "Undulator calculated parameters", addSpace=False, orientation="vertical")
        gui.button(left_box_0, self, "Update info", callback=self.update_info)
        self.info_id = QTextEdit()
        self.info_id.readOnly = True
        left_box_0.layout().addWidget(self.info_id)



        left_box_1 = oasysgui.widgetBox(tab_util, "Auto Setting of Undulator", addSpace=False, orientation="vertical")

        oasysgui.lineEdit(left_box_1, self, "auto_energy", "Set Undulator at Energy [eV]",
                          labelWidth=250, valueType=float, orientation="horizontal")
        oasysgui.lineEdit(left_box_1, self, "auto_harmonic_number", "As Harmonic #",  labelWidth=250, valueType=int, orientation="horizontal")

        button_box = oasysgui.widgetBox(left_box_1, "", addSpace=False, orientation="horizontal")

        gui.button(button_box, self, "Set Kv value", callback=self.auto_set_undulator_V)
        gui.button(button_box, self, "Set Kh value", callback=self.auto_set_undulator_H)
        gui.button(button_box, self, "Set Both K values", callback=self.auto_set_undulator_B)


    def update_info(self):

        print(">>>>>",self.K_horizontal)
        print(">>>>>",self.K_vertical)
        print(">>>>>",self.period_length)
        print(">>>>>",self.number_of_periods)
        # electron_energy_in_GeV = Setting(2.0)
        # electron_energy_spread = Setting(0.001)
        # ring_current = Setting(0.4)
        print(">>>>>>>>>>>>>>>>>>> update info")
        syned_light_source = self.get_light_source()

        info_parameters = {
            "electron_energy_in_GeV":self.electron_energy_in_GeV,
            "gamma":"%8.3f"%self.gamma(),
            "ring_current":"%4.3f "%self.ring_current,
            "K_horizontal":self.K_horizontal,
            "K_vertical": self.K_vertical,
            "period_length": self.period_length,
            "number_of_periods": self.number_of_periods,
            "undulator_length": self.number_of_periods*self.period_length,
            "resonance_energy":"%6.3f"%self.resonance_energy(),
            "resonance_energy3": "%6.3f" % (self.resonance_energy()*3.0),
            "resonance_energy5": "%6.3f" % (self.resonance_energy()*5.5),
            "B_horizontal":"%4.2F"%self.magnetic_field_from_K(self.K_horizontal),
            "B_vertical": "%4.2F" % self.magnetic_field_from_K(self.K_vertical),
            "cc_1": "%4.2f" % (self.gaussian_central_cone_aperture(1)*1e6),
            "cc_3": "%4.2f" % (self.gaussian_central_cone_aperture(3)*1e6),
            "cc_5": "%4.2f" % (self.gaussian_central_cone_aperture(5)*1e6),
            # "cc_7": "%4.2f" % (self.gaussian_central_cone_aperture(7)*1e6),
            "sigma_rad": "%5.2f" % self.get_sigmas_radiation(1)[0],
            "sigma_rad_prime": "%5.2f" % self.get_sigmas_radiation(1)[1],
            "sigma_rad3": "%5.2f" % self.get_sigmas_radiation(3)[0],
            "sigma_rad_prime3": "%5.2f" % self.get_sigmas_radiation(3)[1],
            "first_ring_1": "%5.2f" % (1e6 * self.get_resonance_ring(1,1) ),
            "first_ring_3": "%5.2f" % (1e6 * self.get_resonance_ring(3,1) ),
            "first_ring_5": "%5.2f" % (1e6 * self.get_resonance_ring(5, 1)),
            "Sx": "%5.2f" % self.get_photon_sizes_and_divergences()[0],
            "Sy": "%5.2f" % self.get_photon_sizes_and_divergences()[1],
            "Sxp": "%5.2f" % self.get_photon_sizes_and_divergences()[2],
            "Syp": "%5.2f" % self.get_photon_sizes_and_divergences()[3],
            "und_power": "%5.2f" % self.undulator_full_emitted_power(),
            }

        self.info_id.setText(self.info_template().format_map(info_parameters))
        # self.K_horizontal = 0.0
        # K_vertical = Setting(1.0)
        # period_length = Setting(0.010)
        # number_of_periods = Setting(10)

    def info_template(self):
        return \
"""
Electron beam energy [GeV]: {electron_energy_in_GeV}
Electron beam gamma:        {gamma}
Electron current:           {ring_current}
Horizontal K:               {K_horizontal}
Vertical K:                 {K_vertical}
Period Length [m]:          {period_length}
Number of Periods:          {number_of_periods}

Undulator Length [m]:               {undulator_length}
Horizontal Peak Magnetic field [T]: {B_horizontal}
Vertical Peak Magnetic field [T]:   {B_vertical}

Total power radiated by the undulator [W]: {und_power}

Resonances: 


Photon energy: {resonance_energy}
       for harmonic 1 : {resonance_energy}
       for harmonic 3 : {resonance_energy3}
       for harmonic 3 : {resonance_energy5}

Central cone (RMS urad):
       for harmonic 1 : {cc_1}
       for harmonic 3 : {cc_3}
       for harmonic 5 : {cc_5}

First ring at (urad):
       for harmonic 1 : {first_ring_1}
       for harmonic 3 : {first_ring_3}
       for harmonic 5 : {first_ring_5}

Sizes and divergences of radiation :
    at 1st harmonic: sigma: {sigma_rad} u m, sigma': {sigma_rad_prime} urad
    at 3rd harmonic: sigma: {sigma_rad3} u m, sigma': {sigma_rad_prime3} urad

Sizes and divergences of photon source (convolution) at 1st harmonic: :
    Sx: {Sx} u m
    Sy: {Sy} um, 
    Sx': {Sxp} urad
    Sy': {Syp} urad

"""

    def get_magnetic_structure(self):
        return Undulator(K_horizontal=self.K_horizontal,
                         K_vertical=self.K_vertical,
                         period_length=self.period_length,
                         number_of_periods=self.number_of_periods)


    def check_magnetic_structure_instance(self, magnetic_structure):
        if not isinstance(magnetic_structure, Undulator):
            raise ValueError("Magnetic Structure is not a Undulator")

    def populate_magnetic_structure(self, magnetic_structure):
        self.K_horizontal = magnetic_structure._K_horizontal
        self.K_vertical = magnetic_structure._K_vertical
        self.period_length = magnetic_structure._period_length
        self.number_of_periods = magnetic_structure._number_of_periods

    def auto_set_undulator_V(self):
        self.auto_set_undulator(VERTICAL)

    def auto_set_undulator_H(self):
        self.auto_set_undulator(HORIZONTAL)

    def auto_set_undulator_B(self):
        self.auto_set_undulator(BOTH)

    def auto_set_undulator(self, which=VERTICAL):
        congruence.checkStrictlyPositiveNumber(self.auto_energy, "Set Undulator at Energy")
        congruence.checkStrictlyPositiveNumber(self.auto_harmonic_number, "As Harmonic #")
        congruence.checkStrictlyPositiveNumber(self.electron_energy_in_GeV, "Energy")
        congruence.checkStrictlyPositiveNumber(self.period_length, "Period Length")

        wavelength = self.auto_harmonic_number*m2ev/self.auto_energy
        K = round(numpy.sqrt(2*(((wavelength*2*self.gamma()**2)/self.period_length)-1)), 6)

        if which == VERTICAL:
            self.K_vertical = K
            self.K_horizontal = 0.0

        if which == BOTH:
            Kboth = round(K / numpy.sqrt(2), 6)
            self.K_vertical =  Kboth
            self.K_horizontal = Kboth

        if which == HORIZONTAL:
            self.K_horizontal = K
            self.K_vertical = 0.0

        self.update_info()

    def gamma(self):
        return 1e9*self.electron_energy_in_GeV / (codata.m_e *  codata.c**2 / codata.e)

    def resonance_energy(self, theta_x=0.0, theta_z=0.0, harmonic=1):
        gamma = self.gamma()

        wavelength = (self.period_length / (2.0*gamma **2)) * \
                     (1 + self.K_vertical**2 / 2.0 + self.K_horizontal**2 / 2.0 + \
                      gamma**2 * (theta_x**2 + theta_z ** 2))

        wavelength /= harmonic

        return m2ev/wavelength

    def magnetic_field_from_K(self, K):
        return K * 2 * numpy.pi * codata.m_e * codata.c / (codata.e * self.period_length)

    def gaussian_central_cone_aperture(self, n):
        return (1/self.gamma())*numpy.sqrt((1.0/(2.0*n*self.number_of_periods)) * (1.0 + self.K_horizontal**2/2.0 + self.K_vertical**2/2.0))

    def get_sigmas_radiation(self, n=1):
        photon_energy = self.resonance_energy() * n
        lambdan = 1e-10 * codata.h * codata.c / codata.e * 1e10 / photon_energy  # in m
        return 1e6 * 2.740 / 4 / numpy.pi * numpy.sqrt(lambdan * self.number_of_periods * self.period_length), 1e6 * \
               0.69 * numpy.sqrt(lambdan / (self.period_length*self.number_of_periods))

    def get_resonance_ring(self,harmonic_number=1, ring_order=1):
        K_value = numpy.sqrt( self.K_vertical**2 + self.K_horizontal**2)
        return 1.0/self.gamma()*numpy.sqrt( ring_order / harmonic_number * (1+0.5*K_value**2) )

    def get_photon_sizes_and_divergences(self,n=1):
        sr,srp = self.get_sigmas_radiation(n=1)

        syned_electron_beam = self.get_light_source().get_electron_beam()
        sx,sz,sxp,szp = syned_electron_beam.get_sigmas_all()

        Sx = numpy.sqrt(  (1e6*sx)**2 + sr**2)
        Sz = numpy.sqrt(  (1e6*sz)**2 + sr**2)
        Sxp = numpy.sqrt( (1e6*sxp)**2 + srp**2)
        Szp = numpy.sqrt( (1e6*szp)**2 + srp**2)

        return Sx,Sz,Sxp,Szp

    def undulator_full_emitted_power(self):
        ptot = (self.number_of_periods/6) * codata.value('characteristic impedance of vacuum') * \
               self.ring_current * codata.e * 2 * numpy.pi * codata.c * self.gamma()**2 * \
               (self.K_vertical**2+self.K_horizontal**2) / self.period_length
        return ptot


from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    a = QApplication(sys.argv)
    ow = OWUndulatorLightSource()
    ow.show()
    a.exec_()
