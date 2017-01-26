class LensIdealParameters(OpticElementParameters):
    def __init__(self, beamline=Beamline(),
                 energy_min=1.0,
                 energy_max=100000.0,
                 lens_ideal=LensIdeal("lens", 0.0, 0.0)):
        super().__init__(beamline=beamline, energy_min=energy_min, energy_max=energy_max)
        self._lens_ideal = lens_ideal
