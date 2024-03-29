#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #########################################################################
# Copyright (c) 2018, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2018. UChicago Argonne, LLC. This software was produced       #
# under U.S. Government contract DE-AC02-06CH11357 for Argonne National   #
# Laboratory (ANL), which is operated by UChicago Argonne, LLC for the    #
# U.S. Department of Energy. The U.S. Government has rights to use,       #
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR    #
# UChicago Argonne, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR        #
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is     #
# modified to produce derivative works, such modified software should     #
# be clearly marked, so as not to confuse it with the version available   #
# from ANL.                                                               #
#                                                                         #
# Additionally, redistribution and use in source and binary forms, with   #
# or without modification, are permitted provided that the following      #
# conditions are met:                                                     #
#                                                                         #
#     * Redistributions of source code must retain the above copyright    #
#       notice, this list of conditions and the following disclaimer.     #
#                                                                         #
#     * Redistributions in binary form must reproduce the above copyright #
#       notice, this list of conditions and the following disclaimer in   #
#       the documentation and/or other materials provided with the        #
#       distribution.                                                     #
#                                                                         #
#     * Neither the name of UChicago Argonne, LLC, Argonne National       #
#       Laboratory, ANL, the U.S. Government, nor the names of its        #
#       contributors may be used to endorse or promote products derived   #
#       from this software without specific prior written permission.     #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY UChicago Argonne, LLC AND CONTRIBUTORS     #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT       #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS       #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL UChicago     #
# Argonne, LLC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,        #
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,    #
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;        #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER        #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT      #
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN       #
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         #
# POSSIBILITY OF SUCH DAMAGE.                                             #
# #########################################################################

import os

import orangecanvas.resources as resources

try:
    from mpl_toolkits.mplot3d import Axes3D  # necessario per caricare i plot 3D
except:
    pass

from oasys.util.oasys_objects import OasysPreProcessorData, OasysErrorProfileData, OasysSurfaceData
import oasys.util.oasys_util as OU

from syned_gui.error_profile.abstract_multiple_height_profile_simulator_S import OWAbstractMultipleHeightProfileSimulatorS

class OWMultipleHeightProfileSimulatorS(OWAbstractMultipleHeightProfileSimulatorS):
    name = "Multiple Height Profile Simulator (S)"
    id = "height_profile_simulator_s"
    icon = "icons/simulator_S.png"
    description = "Calculation of mirror surface height profile"
    author = "Luca Rebuffi"
    maintainer_email = "lrebuffi@anl.gov"
    priority = 2
    category = ""
    keywords = ["height_profile_simulator"]

    outputs = [{"name": "PreProcessor_Data",
                "type": OasysPreProcessorData,
                "doc": "PreProcessor Data",
                "id": "PreProcessor_Data"},
               {"name":"Files",
                "type":list,
                "doc":"Files",
                "id":"Files"}]

    usage_path = os.path.join(resources.package_dirname("orangecontrib.shadow.widgets.gui"), "misc", "height_error_profile_usage.png")

    def __init__(self):
        super().__init__()

    def get_usage_path(self):
        return self.usage_path

    def write_error_profile_file(self, zz, xx, yy, outFile):
        OU.write_surface_file(zz, xx, yy, outFile)

    def send_data(self, height_profile_file_names, dimension_x, dimension_y):
        self.send("PreProcessor_Data", OasysPreProcessorData(error_profile_data=OasysErrorProfileData(surface_data=OasysSurfaceData(xx=self.xx,
                                                                                                                                    yy=self.yy,
                                                                                                                                    zz=self.zz,
                                                                                                                                    surface_data_file=height_profile_file_names),
                                                                                                      error_profile_x_dim=dimension_x,
                                                                                                      error_profile_y_dim=dimension_y)))


        self.send("Files", height_profile_file_names)
