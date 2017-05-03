
from orangewidget import gui,widget
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence
from oasys.widgets import widget as oasyswidget

from syned.storage_ring.light_source import LightSource
from syned.beamline.beamline import Beamline
from syned.util.json_tools import load_from_json_file, load_from_json_url

class FileReader(oasyswidget.OWWidget):
    name = "Syned File Reader"
    description = "Utility: Syned File Reader"
    icon = "icons/file_reader.png"
    maintainer = "Manuel Sanchez del Rio"
    maintainer_email = "srio(@at@)esrf.eu"
    priority = 2
    category = "Utility"
    keywords = ["data", "file", "load", "read"]

    want_main_area = 0

    syned_file_name = Setting("")

    outputs = [{"name":"SynedBeamline",
                "type":Beamline,
                "doc":"Syned Beamline",
                "id":"data"}]


    def __init__(self):
        super().__init__()

        self.runaction = widget.OWAction("Read Syned File", self)
        self.runaction.triggered.connect(self.read_file)
        self.addAction(self.runaction)

        self.setFixedWidth(590)
        self.setFixedHeight(150)

        left_box_1 = oasysgui.widgetBox(self.controlArea, "Syned Local/Remote File Selection", addSpace=True,
                                        orientation="vertical",width=570, height=60)

        figure_box = oasysgui.widgetBox(left_box_1, "", addSpace=True, orientation="horizontal", width=550, height=50)

        self.le_syned_file_name = oasysgui.lineEdit(figure_box, self, "syned_file_name", "Syned File Name or File URL",
                                                    labelWidth=190, valueType=str, orientation="horizontal")
        self.le_syned_file_name.setFixedWidth(260)

        gui.button(figure_box, self, "...", callback=self.selectFile)

        gui.separator(left_box_1, height=20)

        button = gui.button(self.controlArea, self, "Read Syned File", callback=self.read_file)
        button.setFixedHeight(45)

        gui.rubber(self.controlArea)

    def selectFile(self):
        self.le_syned_file_name.setText(oasysgui.selectFileFromDialog(self, self.syned_file_name, "Open Syned File"))

    def read_file(self):
        self.setStatusMessage("")
        if self.syned_file_name[:4] == "http":
            is_remote = True
        else:
            is_remote = False

        try:
            if is_remote:
                tmp = load_from_json_url(self.syned_file_name)
            else:
                tmp = load_from_json_file(self.syned_file_name)
            print("Reading file %s, returned class: "%self.syned_file_name,type(tmp))

            if  isinstance(tmp,LightSource):
                bl = Beamline(tmp)
            else:
                raise Exception("json file must contain a SYNED LightSource")

        except:
            raise Exception("Error reading SYNED LightSource from file")

        self.send("SynedBeamline", bl)


if __name__ == "__main__":
    from PyQt4.QtGui import QApplication
    import sys

    a = QApplication(sys.argv)
    ow = FileReader()
    ow.syned_file_name = "" # /scisoft/xop2.4/extensions/shadowvui/shadow3-scripts/ESRF-LIGHTSOURCES/ESRF_ID30_HighBeta_PPU35_23.json"

    ow.show()
    a.exec_()

