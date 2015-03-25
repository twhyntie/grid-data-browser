#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...for the logging.
import logging as lg

##...for the data values.
#from datavals import *

#...for the HANDLING.
from handlers import getPixelmanTimeString, getPixelsStringFromPixelMap

#...for the Klusters (Clusters).
from kluster import KlusterFinder

class Frame:
    """
    A wrapper class for Timepix frames.
    """

    def __init__(self, **kwargs):
        """
        Constructor.
        """
        lg.debug(" Instantiating a Frame object.")

        # Geospatial information
        #------------------------

        if "lat" not in kwargs.keys():
            raise IOError("FRAME_NO_LAT")

        ## The frame latitude [deg.].
        self.__lat = kwargs["lat"]

        if "lon" not in kwargs.keys():
            raise IOError("FRAME_NO_LON")

        ## The frame longitude [deg.].
        self.__lon = kwargs["lon"]

        if "alt" not in kwargs.keys():
            raise IOError("FRAME_NO_ALT")

        ## The frame altitude [m].
        self.__alt = kwargs["alt"]

        ## The roll angle of the lab. frame [deg.].
        self.__roll = 0.0
        if "roll" in kwargs.keys():
            # TODO: validate the value.
            self.__roll = kwargs["roll"]

        ## The pitch angle of the lab. frame [deg.].
        self.__pitch = 0.0
        if "pitch" in kwargs.keys():
            # TODO: validate the value.
            self.__pitch = kwargs["pitch"]

        ## The yaw angle of the lab. frame [deg.].
        self.__yaw = 0.0
        if "yaw" in kwargs.keys():
            # TODO: validate the value.
            self.__yaw = kwargs["yaw"]

        ## The Omega_x of the lab frame [deg. s^{-1}].
        self.__omegax = 0.0
        if "omegax" in kwargs.keys():
            self.__omegax = kwargs["omegax"]

        ## The Omega_y of the lab frame [deg. s^{-1}].
        self.__omegay = 0.0
        if "omegay" in kwargs.keys():
            self.__omegay = kwargs["omegay"]

        ## The Omega_z of the lab frame [deg. s^{-1}].
        self.__omegaz = 0.0
        if "omegaz" in kwargs.keys():
            self.__omegaz = kwargs["omegaz"]

        # For the detector.

        if "chipid" not in kwargs.keys():
            raise IOError("FRAME_NO_CHIPID")

        ## The chip ID.
        self.__chipid = kwargs["chipid"]

        if "biasvoltage" not in kwargs.keys():
            raise IOError("FRAME_NO_HV")

        ## The bias voltage (HV) [V].
        self.__hv = kwargs["biasvoltage"]

        # The DAC values.

        if "ikrum" not in kwargs.keys():
            raise IOError("FRAME_NO_IKRUM")
        #
        ## The detector I_Krum value.
        self.__ikrum = kwargs["ikrum"]
        #
        if "disc" not in kwargs.keys():
            raise IOError("FRAME_NO_DISC")
        #
        ## The detector I_Krum value.
        self.__Disc = kwargs["disc"]
        #
        if "preamp" not in kwargs.keys():
            raise IOError("FRAME_NO_PREAMP")
        #
        ## The detector preamp DAC value.
        self.__Preamp = kwargs["preamp"]
        #
        if "buffanaloga" not in kwargs.keys():
            raise IOError("FRAME_NO_BUFFANALOGA")
        #
        ## The detector BuffAnalogA DAC value.
        self.__BuffAnalogA = kwargs["buffanaloga"]
        #
        if "buffanalogb" not in kwargs.keys():
            raise IOError("FRAME_NO_BUFFANALOGB")
        #
        ## The detector BuffAnalogB DAC value.
        self.__BuffAnalogB = kwargs["buffanalogb"]
        #
        if "hist" not in kwargs.keys():
            raise IOError("FRAME_NO_HIST")
        #
        ## The detector Hist DAC value.
        self.__Hist = kwargs["hist"]
        #
        if "thl" not in kwargs.keys():
            raise IOError("FRAME_NO_THL")
        #
        ## The detector THL DAC value.
        self.__THL = kwargs["thl"]
        #
        if "thlcoarse" not in kwargs.keys():
            raise IOError("FRAME_NO_THLCOARSE")
        #
        ## The detector THLCoarse DAC value.
        self.__THLCoarse = kwargs["thlcoarse"]
        #
        if "vcas" not in kwargs.keys():
            raise IOError("FRAME_NO_VCAS")
        #
        ## The detector Vcas DAC value.
        self.__Vcas = kwargs["vcas"]
        #
        if "fbk" not in kwargs.keys():
            raise IOError("FRAME_NO_FBK")
        #
        ## The detector FBK DAC value.
        self.__FBK = kwargs["fbk"]
        #
        if "gnd" not in kwargs.keys():
            raise IOError("FRAME_NO_GND")
        #
        ## The detector GND DAC value.
        self.__GND = kwargs["gnd"]
        #
        if "ths" not in kwargs.keys():
            raise IOError("FRAME_NO_THS")
        #
        ## The detector THS DAC value.
        self.__THS = kwargs["ths"]
        #
        if "biaslvds" not in kwargs.keys():
            raise IOError("FRAME_NO_BIASLVDS")
        #
        ## The detector BiasLVDS DAC value.
        self.__BiasLVDS = kwargs["biaslvds"]
        #
        if "reflvds" not in kwargs.keys():
            raise IOError("FRAME_NO_REFLVDS")
        #
        ## The detector RefLVDS DAC value.
        self.__RefLVDS = kwargs["reflvds"]

        ## The detector x position [mm].
        self.__det_x = 0.0
        if "detx" in kwargs.keys():
            self.__det_x = kwargs["detx"]

        ## The detector y position [mm].
        self.__det_y = 0.0
        if "dety" in kwargs.keys():
            self.__det_y = kwargs["dety"]

        ## The detector z position [mm].
        self.__det_z = 0.0
        if "detz" in kwargs.keys():
            self.__det_z = kwargs["detz"]

        ## The detector Euler angle a [deg.].
        self.__det_euler_a = 0.0
        if "deteulera" in kwargs.keys():
            self.__det_euler_a = kwargs["deteulera"]

        ## The detector Euler angle b [deg.].
        self.__det_euler_b = 0.0
        if "deteulerb" in kwargs.keys():
            self.__det_euler_b = kwargs["deteulerb"]

        ## The detector Euler angle c [deg.].
        self.__det_euler_c = 0.0
        if "deteulerc" in kwargs.keys():
            self.__det_euler_c = kwargs["deteulerc"]


        # Temporal information
        #----------------------

        if "starttime" not in kwargs.keys() or "acqtime" not in kwargs.keys():
            raise IOError("BAD_FRAME_TIME_INFO")

        ## The start time [s].
        self.__starttime = kwargs["starttime"]

        ## The acquisition time [s].
        self.__acqtime = kwargs["acqtime"]

        self.__starttimesec, self.__starttimesubsec, self.__startTimeS = \
            getPixelmanTimeString(self.__starttime)
        lg.debug(" Frame found with start time: '%s'." % (self.__startTimeS))

        ## The end time [s].
        self.__endtime = self.__starttime + self.__acqtime

        self.__endtimesec, self.__endtimesubsec, ets = \
            getPixelmanTimeString(self.__endtime)

        # Detector information
        #---------------------

        if "firmwarev" not in kwargs.keys():
            raise IOError("FRAME_NO_FIRMWAREV")
        #
        ## The detector firmware version.
        self.__firmwarev = kwargs["firmwarev"]
        #
        if "hwtimermode" not in kwargs.keys():
            raise IOError("FRAME_NO_HWTIMERMODE")
        #
        ## The detector hardware timer mode.
        self.__hwTimerMode = kwargs["hwtimermode"]
        #
        if "interface" not in kwargs.keys():
            raise IOError("FRAME_NO_INTERFACE")
        #
        ## The detector interface.
        self.__interface = kwargs["interface"]
        #
        if "mpxclock" not in kwargs.keys():
            raise IOError("FRAME_NO_MPXCLOCK")
        #
        ## The detector MPX clock.
        self.__mpxClock = kwargs["mpxclock"]
        #
        if "mpxtype" not in kwargs.keys():
            raise IOError("FRAME_NO_MPXTYPE")
        #
        ## The detector MPX type.
        self.__mpxType = kwargs["mpxtype"]
        #
        if "nameandsn" not in kwargs.keys():
            raise IOError("FRAME_NO_NAMEANDSN")
        #
        ## The detector name and serial number.
        self.__nameAndSN = kwargs["nameandsn"]
        #
        if "pixelmanv" not in kwargs.keys():
            raise IOError("FRAME_NO_PIXELMANVERSION")
        #
        ## The detector Pixelman version used to take the data.
        self.__pixelmanv = kwargs["pixelmanv"]
        #
        if "polarity" not in kwargs.keys():
            raise IOError("FRAME_NO_POLARITY")
        #
        ## The detector polarity.
        self.__polarity = kwargs["polarity"]
        #
        if "tpxclock" not in kwargs.keys():
            raise IOError("FRAME_NO_TPXCLOCK")
        #
        ## The detector .
        self.__tpxClock = kwargs["tpxclock"]


        # Payload information
        #--------------------

        ## The frame width.
        self.__width = 256

        if "width" in kwargs.keys():
            self.__width = kwargs["width"]

        ## The frame height.
        self.__height = 256

        if "height" in kwargs.keys():
            self.__height = kwargs["height"]

        if "format" not in kwargs.keys():
            raise IOError("FRAME_NO_FORMAT")

        ## The payload format.
        self.__format = kwargs["format"]

        ## The map of the pixels.
        self.__pixelmap = {}

        if "pixelmap" in kwargs.keys():
            self.__pixelmap = kwargs["pixelmap"]

        ## The pixel mask map.
        self.__pixel_mask_map = {}

        if "pixelmask" in kwargs.keys():
            self.__pixel_mask_map = kwargs["pixelmask"]

        ## Is the data from a Monte Carlo simulation?
        self.__isMC = False
        if "ismc" in kwargs.keys():
            self.__ismc = kwargs["ismc"]

        if "skipclustering" in kwargs.keys():
            if kwargs["skipclustering"]:
                #print("SKIPPING THE CLUSTERING!")
                self.__n_klusters = -1
                return None

        # Do the clustering.

        ## The frame's cluster finder.
        self.__kf = KlusterFinder(self.getPixelMap(), self.getWidth(), self.getHeight(), self.isMC(), self.__pixel_mask_map)

        self.__n_klusters = self.__kf.getNumberOfKlusters()

    # Accessor methods
    #==================

    # Geospatial information
    #------------------------

    def getLatitude(self):
        return self.__lat

    def getLongitude(self):
        return self.__lon

    def getAltitude(self):
        return self.__alt

    def getRoll(self):
        return self.__roll

    def getPitch(self):
        return self.__pitch

    def getYaw(self):
        return self.__yaw

    def getOmegax(self):
        return self.__omegax

    def getOmegay(self):
        return self.__omegay

    def getOmegaz(self):
        return self.__omegaz

    def getDetx(self):
        return self.__det_x

    def getDety(self):
        return self.__det_y

    def getDetz(self):
        return self.__det_z

    def getDetEulera(self):
        return self.__det_euler_a

    def getDetEulerb(self):
        return self.__det_euler_b

    def getDetEulerc(self):
        return self.__det_euler_c

    def getChipId(self):
        return self.__chipid

    def getBiasVoltage(self):
        return self.__hv

    def getIKrum(self):
        return self.__ikrum

    def getDisc(self):
        return self.__Disc

    def getPreamp(self):
        return self.__Preamp

    def getBuffAnalogA(self):
        return self.__BuffAnalogA

    def getBuffAnalogB(self):
        return self.__BuffAnalogB

    def getHist(self):
        return self.__Hist

    def getTHL(self):
        return self.__THL

    def getTHLCoarse(self):
        return self.__THLCoarse

    def getVcas(self):
        return self.__Vcas

    def getFBK(self):
        return self.__FBK

    def getGND(self):
        return self.__GND

    def getTHS(self):
        return self.__THS

    def getBiasLVDS(self):
        return self.__BiasLVDS

    def getRefLVDS(self):
        return self.__RefLVDS

    def getFirmwareVersion(self):
        return self.__firmwarev

    def getHwTimerMode(self):
        return self.__hwTimerMode

    def getInterface(self):
        return self.__interface

    def getMpxClock(self):
        return self.__mpxClock

    def getMpxType(self):
        return self.__mpxType

    def getNameAndSerialNumber(self):
        return self.__nameAndSN

#    def getBSPreampEnabled(self):
#        return self.__bspenabled
#
    def getPixelmanVersion(self):
        return self.__pixelmanv

    def getPolarity(self):
        return self.__polarity

    def getTpxClock(self):
        return self.__tpxClock

    # Temporal information
    #----------------------

    def getStartTime(self):
        return self.__starttime

    def getStartTimeSec(self):
        return self.__starttimesec

    def getStartTimeSubSec(self):
        return self.__starttimesubsec

    def getStartTimeS(self):
        return self.__startTimeS

    def getEndTime(self):
        return self.__endtime

    def getEndTimeSec(self):
        return self.__endtimesec

    def getEndTimeSubSec(self):
        return self.__endtimesubsec

    def getAcqTime(self):
        return self.__acqtime

    # Payload information
    #---------------------

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getFormat(self):
        return self.__format

    def getPixelMap(self):
        return self.__pixelmap

    def getPixelMask(self):
        return self.__pixel_mask_map

    def getRawNumberOfPixels(self):
        return len(self.__pixelmap)

    def getNumberOfUnmaskedPixels(self):
        unmasked = 0
        #lg.debug(self.__pixelmap)
        #lg.debug(self.__pixel_mask_map)
        #for X in self.__pixel_mask_map.keys():
        #    lg.debug(" * %5d -> (%5d,%5d)." % (X, X%256, X/256))
        for X in self.__pixelmap.keys():
            #lg.debug(" * Is %5d -> (%5d,%5d) in the map?" % (X, X%256, X/256))
            if X not in self.__pixel_mask_map.keys():
                #lg.debug(" *---> NO!")
                unmasked += 1
            #else:
            #    lg.debug(" *---> YES!")
        return unmasked

    def getNumberOfMaskedPixels(self):
        return len(self.__pixel_mask_map)

    def getOccupancy(self):
        return len(self.__pixelmap)

    def getOccupancyPc(self):
        return float(len(self.__pixelmap))/float(self.__width * self.__height)

    def isMC(self):
        return self.__ismc

    def getPixelsString(self):
        s = ""

    def getNumberOfKlusters(self):
        return self.__n_klusters

    def getNumberOfGammas(self):
        return self.__kf.getNumberOfGammas()

    def getNumberOfMonopixels(self):
        return self.__kf.getNumberOfMonopixels()

    def getNumberOfBipixels(self):
        return self.__kf.getNumberOfBipixels()

    def getNumberOfTripixelGammas(self):
        return self.__kf.getNumberOfTripixelGammas()

    def getNumberOfTetrapixelGammas(self):
        return self.__kf.getNumberOfTetrapixelGammas()

    def getNumberOfNonGammas(self):
        return self.getNumberOfKlusters() - self.getNumberOfGammas()

    def getKlusterFinder(self):
        return self.__kf

    def getPayloadString(self):

        ## The payload string to return.
        ps = ""

        n = 0

        # Loop over the pixel map and output in the x y C format.
        for X, C in self.__pixelmap.iteritems():
            ps += "%d\t%d\t%d" % (X%256, X/256, C)
            n += 1
            if n < len(self.__pixelmap):
                ps += "\n"

        return ps

    def getDscFileString(self):
        """ Create a DSC file string from a CERN@school frame wrapper. """

        ## The frame metadata (for the DSC file).
        d = ""

        d += "A000000001\r\n"
        d += "[F0]\r\n"
        d += "Type=i16 "

        # The payload format.
        d += "[X,Y,C]"
        d += " width=%d height=%d\r\n" % (self.__width, self.__height)
        d += "\"Acq mode\" (\"Acquisition mode\"):\r\n"
        d += "i32[1]\r\n"
        d += "%d \r\n" % (1)
        d += "\r\n"
        d += "\"Acq time\" (\"Acquisition time [s]\"):\r\n"
        d += "double[1]\r\n"
        d += "%f \r\n" % (self.getAcqTime())
        d += "\r\n"
        d += "\"ChipboardID\" (\"Medipix or chipboard ID\"):\r\n"
        d += "uchar[10]\r\n"
        d += "%s\r\n" % (self.getChipId())
        d += "\r\n"
#        customname = str(chain.FramesData.GetCustomName()).strip()
#        if customname != "":
#            d += "\"Custom name\" (\"Custom name\"):\n"
#            d += "uchar[7]\n"
#            d += "%s\n" % (customname)
#            d += "\n"
        d += "\"DACs\" (\"DACs values of all chips\"):\r\n"
        d += "u16[14]\r\n"
        #
        # The DACs.
        d += "%d " % (self.getIKrum())
        d += "%d " % (self.getDisc())
        d += "%d " % (self.getPreamp())
        d += "%d " % (self.getBuffAnalogA())
        d += "%d " % (self.getBuffAnalogB())
        d += "%d " % (self.getHist())
        d += "%d " % (self.getTHL())
        d += "%d " % (self.getTHLCoarse())
        d += "%d " % (self.getVcas())
        d += "%d " % (self.getFBK())
        d += "%d " % (self.getGND())
        d += "%d " % (self.getTHS())
        d += "%d " % (self.getBiasLVDS())
        d += "%d " % (self.getRefLVDS())
        d += "\r\n"
        d += "\r\n"
        d += "\"Firmware\" (\"Firmware version\"):\r\n"
        d += "char[64]\r\n"
        d += "%s\r\n" % (self.getFirmwareVersion())
        d += "\r\n"
        d += "\"HV\" (\"Bias voltage [V]\"):\r\n"
        d += "double[1]\r\n"
        d += "%f \r\n" % (self.getBiasVoltage())
        d += "\r\n"
        d += "\"Hw timer\" (\"Hw timer mode\"):\r\n"
        d += "i32[1]\r\n"
        d += "%d \r\n" % (self.getHwTimerMode())
        d += "\r\n"
        d += "\"Interface\" (\"Medipix interface\"):\r\n"
        d += "uchar[6]\r\n"
        d += "%s\r\n" % (self.getInterface())
        d += "\r\n"
        d += "\"Mpx clock\" (\"Medipix clock [MHz]\"):\r\n"
        d += "double[1]\r\n"
        d += "%f \r\n" % (self.getMpxClock())
        d += "\r\n"
        d += "\"Mpx type\" (\"Medipix type (1-2.1, 2-MXR, 3-TPX)\"):\r\n"
        d += "i32[1]\r\n"
        d += "%d \r\n" % (self.getMpxType())
        d += "\r\n"
        d += "\"Name+SN\" (\"Name and serial number\"):\r\n"
        d += "char[64]\r\n"
        d += "%s\r\n" % (self.getNameAndSerialNumber())
        d += "\r\n"
        d += "\"Pixelman version\" (\"Pixelman version\"):\r\n"
        d += "uchar[6]\r\n"
        d += "%s\r\n" % (self.getPixelmanVersion())
        d += "\r\n"
        d += "\"Polarity\" (\"Detector polarity (0 negative, 1 positive)\"):\r\n"
        d += "i32[1]\r\n"
        d += "%d \r\n" % (self.getPolarity())
        d += "\r\n"
        d += "\"Start time\" (\"Acquisition start time\"):\r\n"
        d += "double[1]\r\n"
        d += "%f \r\n" % (self.getStartTime())
        d += "\r\n"
        d += "\"Start time (string)\" (\"Acquisition start time (string)\"):\r\n"
        d += "char[64]\r\n"
        d += "%s\r\n" % (self.getStartTimeS())
        d += "\r\n"
        #d += "\"Timepix clock\" (\"Timepix clock (0-3: 10MHz, 20MHz, 40MHz, 80MHz)\"):\r\n"
        d += "\"Timepix clock\" (\"Timepix clock (in MHz)\"):\r\n"
        d += "double[1]\r\n"
        d += "%f \r\n" % (self.getTpxClock())

        return d
