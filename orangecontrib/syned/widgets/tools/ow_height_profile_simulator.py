import os, sys

from PyQt5.QtWidgets import QApplication

import orangecanvas.resources as resources

from oasys.widgets.error_profile.ow_abstract_height_profile_simulator import OWAbstractHeightErrorProfileSimulator

from oasys.util.oasys_objects import OasysPreProcessorData, OasysErrorProfileData, OasysSurfaceData
import oasys.util.oasys_util as OU

class OWHeightProfileSimulator(OWAbstractHeightErrorProfileSimulator):
    name = "Height Profile Simulator"
    id = "height_profile_simulator"
    description = "Calculation of mirror surface height profile"
    icon = "icons/simulator.png"
    author = "Luca Rebuffi"
    maintainer_email = "srio@esrf.eu; luca.rebuffi@elettra.eu"
    priority = 3
    category = ""
    keywords = ["height_profile_simulator"]

    outputs = [{"name": "PreProcessor_Data",
                "type": OasysPreProcessorData,
                "doc": "PreProcessor Data",
                "id": "PreProcessor_Data"}]

    usage_path = os.path.join(resources.package_dirname("orangecontrib.syned.widgets.tools"), "misc", "height_error_profile_usage.png")

    def __init__(self):
        super().__init__()

    def get_usage_path(self):
        return self.usage_path

    def write_error_profile_file(self):
        if not (self.heigth_profile_file_name.endswith("h5") or self.heigth_profile_file_name.endswith("hdf5") or self.heigth_profile_file_name.endswith("hdf")):
            self.heigth_profile_file_name += ".hdf5"

        OU.write_surface_file(self.zz, self.xx, self.yy, self.heigth_profile_file_name)

    def send_data(self, dimension_x, dimension_y):
        self.send("PreProcessor_Data", OasysPreProcessorData(error_profile_data=OasysErrorProfileData(surface_data=OasysSurfaceData(xx=self.xx,
                                                                                                                                    yy=self.yy,
                                                                                                                                    zz=self.zz,
                                                                                                                                    surface_data_file=self.heigth_profile_file_name),
                                                                                                      error_profile_x_dim=dimension_x,
                                                                                                      error_profile_y_dim=dimension_y)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OWHeightProfileSimulator()
    w.si_to_user_units = 1.0
    w.show()
    app.exec()
    w.saveSettings()
