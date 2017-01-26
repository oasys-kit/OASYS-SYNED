__author__ = 'labx'

from syned.storage_ring.electron_beam import ElectronBeam

class ElectronBeamParameters(object):
    def __init__(self,
                 electron_beam=ElectronBeam()):
        self._electron_beam=electron_beam

    def getElectronBeam(self):
        return self._light_source_parameters
