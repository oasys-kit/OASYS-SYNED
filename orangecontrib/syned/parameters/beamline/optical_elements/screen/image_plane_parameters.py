
class ImagePlaneParameters(OpticElementParameters):
    def __init__(self, beamline=Beamline(),
                 energy_min=1.0,
                 energy_max=100000.0,
                 image_plane=ImagePlane("image plane")):
        super().__init__(beamline=beamline, energy_min=energy_min, energy_max=energy_max)
        self._image_plane = image_plane
