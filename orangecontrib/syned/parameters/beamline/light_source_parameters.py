
from syned.beamline.light_source import LightSource

from orangecontrib.syned.parameters.storage_ring.electron_beam_parameters import ElectronBeamParameters

class LightSourceParameters(object):

    def __init__(self,
                 electron_beam_parameters=ElectronBeamParameters(),
                 light_source=LightSource()):
        self._electron_beam_parameters=electron_beam_parameters
        self._light_source=light_source

    def getElectronBeamParameters(self):
        return self._electron_beam_parameters

    def getLightSource(self):
        return self._light_source
