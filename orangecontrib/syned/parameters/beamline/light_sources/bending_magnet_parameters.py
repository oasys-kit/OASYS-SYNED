
class BendingMagnetParameters(object):
    def __init__(self,
                 electron_beam=ElectronBeam(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                 bending_magnet=BendingMagnet(0.0, 0.0, 0.0)):
        self._electron_beam=electron_beam
        self._bending_magnet=bending_magnet