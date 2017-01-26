__author__ = 'labx'

from syned.beamline.beamline import Beamline
from orangecontrib.syned.parameters.beamline.light_source_parameters import LightSourceParameters

class SimulationParameters(object):
    def __init__(self,
                 light_source_parameters=LightSourceParameters(),
                 beamline=Beamline()):
        self._light_source_parameters=light_source_parameters
        self._beamline=beamline

    def getLightSourceParameters(self):
        return self._light_source_parameters

    def getBeamline(self):
        return self._beamline
