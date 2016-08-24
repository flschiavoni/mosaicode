#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from harpia.constants import *
import gettext
_ = gettext.gettext
gettext.bindtextdomain(APP, DIR)
gettext.textdomain(APP)

from harpia.GUI.fieldtypes import *
from harpia.model.plugin import Plugin

class NewImage(Plugin):

# ------------------------------------------------------------------------------
    def __init__(self):
        Plugin.__init__(self)
        self.id = -1
        self.type = "00"
        self.width = "640"
        self.height = "480"

    # ----------------------------------------------------------------------
    def get_help(self):
        return "Cria uma nova imagem."

    # ----------------------------------------------------------------------
    def generate(self, blockTemplate):
        blockTemplate.imagesIO += 'IplImage * block$$_img_o1 = NULL; //Capture\n'

        blockTemplate.functionCall = \
            'CvSize size = cvSize(' + self.width +','+ self.height +');\n' + \
            'block$$_img_o1 = cvCreateImage(size,IPL_DEPTH_8U,3);\n' + \
            'cvSetZero(block$$_img_o1);\n'

        blockTemplate.dealloc = 'cvReleaseImage(&block$$_img_o1);\n'

    # ----------------------------------------------------------------------
    def __del__(self):
        pass

    # ----------------------------------------------------------------------
    def get_description(self):
        return {"Type": str(self.type),
         "Label":_("New Image"),
         "Icon":"images/acquisition.png",
         "Color":"50:100:200:150",
                 "InTypes":"",
                 "OutTypes":{0:"HRP_IMAGE"},
                 "Description":_("Create a new image."),
                 "TreeGroup":_("Image Source"),
                 "IsSource":True
         }

    # ----------------------------------------------------------------------
    def get_properties(self):
        return {

        "width":{"name": "Width",
                    "type": HARPIA_INT,
                    "value": self.width,
                    "lower":0,
                    "upper":65535,
                    "step":1
                    },
        "height":{"name": "Height",
                    "type": HARPIA_INT,
                    "value": self.height,
                    "lower":0,
                    "upper":65535,
                    "step":1
                    }
        }

# ------------------------------------------------------------------------------
