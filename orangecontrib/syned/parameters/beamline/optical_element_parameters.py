from syned.beamline.optical_element import OpticalElement

class OpticElementParameters(object):
    def __init__(self, optical_element=OpticalElement()):
        self._optical_element=optical_element

