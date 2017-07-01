import os

from PyQt4 import QtGui
from orangewidget import gui, widget
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from syned.beamline.beamline import Beamline

class FileWriter(widget.OWWidget):
    name = "Syned File Writer"
    description = "Utility: Syned File Writer"
    icon = "icons/file_writer.png"
    maintainer = "Manuel Sanchez del Rio"
    maintainer_email = "srio(@at@)esrf.eu"
    priority = 4
    category = "Utility"
    keywords = ["data", "file", "load", "read"]

    want_main_area = 0

    syned_file_name = Setting("")
    is_automatic_run= Setting(1)

    inputs = [("SynedBeamline" , Beamline, "setBeamline" ),]

    outputs = [{"name":"SynedBeamline",
                "type":Beamline,
                "doc":"Syned Beamline",
                "id":"data"}]

    syned_data = None

    def __init__(self):
        super().__init__()

        self.runaction = widget.OWAction("Write Syned File", self)
        self.runaction.triggered.connect(self.write_file)
        self.addAction(self.runaction)

        self.setFixedWidth(590)
        self.setFixedHeight(180)

        left_box_1 = oasysgui.widgetBox(self.controlArea, "Syned File Selection", addSpace=True, orientation="vertical",
                                         width=570, height=100)

        gui.checkBox(left_box_1, self, 'is_automatic_run', 'Automatic Execution')

        gui.separator(left_box_1, height=10)

        figure_box = oasysgui.widgetBox(left_box_1, "", addSpace=True, orientation="horizontal", width=550, height=50)

        self.le_syned_file_name = oasysgui.lineEdit(figure_box, self, "syned_file_name", "Syned File Name",
                                                    labelWidth=120, valueType=str, orientation="horizontal")
        self.le_syned_file_name.setFixedWidth(330)

        gui.button(figure_box, self, "...", callback=self.selectFile)

        gui.separator(left_box_1, height=10)

        button = gui.button(self.controlArea, self, "Write Syned File", callback=self.write_file)
        button.setFixedHeight(45)

        gui.rubber(self.controlArea)

    def selectFile(self):
        self.le_syned_file_name.setText(oasysgui.selectFileFromDialog(self, self.syned_file_name, "Open Syned File"))

    def checkEmptyBeam(self, beam):
        return True
    def checkGoodBeam(self, beam):
        return True

    def setBeamline(self, beam):
        if self.checkEmptyBeam(beam):
            if self.checkGoodBeam(beam):
                self.syned_data = beam

                if self.is_automatic_run:
                    self.write_file()
            else:
                QtGui.QMessageBox.critical(self, "Error",
                                           "No good rays or bad content",
                                           QtGui.QMessageBox.Ok)

    def write_file(self):
        self.setStatusMessage("")

        try:
            if self.checkEmptyBeam(self.syned_data):
                if self.checkGoodBeam(self.syned_data):
                    if congruence.checkFileName(self.syned_file_name):
                        self.syned_data.to_json(self.syned_file_name)

                        path, file_name = os.path.split(self.syned_file_name)

                        self.setStatusMessage("File Out: " + file_name)

                        self.send("SynedBeamline", self.syned_data)
                else:
                    QtGui.QMessageBox.critical(self, "Error",
                                               "No good rays or bad content",
                                               QtGui.QMessageBox.Ok)
        except Exception as exception:
            QtGui.QMessageBox.critical(self, "Error",
                                       str(exception), QtGui.QMessageBox.Ok)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    a = QApplication(sys.argv)
    ow = FileWriter()

    ow.show()
    a.exec_()