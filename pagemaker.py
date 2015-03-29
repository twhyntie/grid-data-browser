#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...for the logging.
import logging as lg

#...for the time (being).
import time

#...for making time.
from cernatschool.handlers import make_time_dir


def make_time_stamp(sec):

    ## The time represented as a Python time object.
    mytime = time.gmtime(sec)

    ## The time in the directory format.
    s = time.strftime("%H:%M:%S, %d/%m/%Y", mytime)

    return s

def make_browser_page(f, i, N, prev_loc, next_loc, xyC):

    """
    @param [in] f The CERN@school frame object.
    @param [in] i The index of the frame in the dataset.
    @param [in] N The number of frames in the dataset.
    @param [in] prev_loc The previous frame HTML page URL (relative).
    @param [in] prev_loc The name frame HTML page URL (relative).
    @param [in] xyC String containing the payload data in [x y C] format.

    FIXME: Finish documenting this!
    """

    ## The latitude [degrees].
    lat = f.getLatitude()

    ## The longitude [degrees].
    lon = f.getLongitude()

    ## The altitude [m].
    alt = f.getAltitude()

    ## The frame start time [s].
    start_time = f.getStartTimeSec()

    ## Timestamp for the frame.
    time_stamp = make_time_stamp(start_time)

    ## The HTML page string to return.
    ps = ""

    ps += "<!DOCTYPE html>\n"
    ps += "<title>GridPP Data Browser</title>\n"
    ps += "<link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>\n"
    ps += "<link rel = 'stylesheet' href = '../../../assets/css/main.css'>\n"
    #ps += "<script src='https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js'></script>\n"
    ps += "<script src='../../../js/jquery.min.js'></script>\n"
    ps += "<script src = '../../../js/raphael-min.js'></script>\n"
    ps += "<div id = 'container'>\n"
    ps += "  <div id = 'sidebar'>\n"
    ps += "    <div id = 'title-container'>\n"
    #ps += "    <!-- <div id = "title">Data Browser</div> -->\n"
    ps += "    </div>\n"
    ps += "    <div id = \"menu-button\" onclick = \"$('#mask, #menu').fadeIn();\"><img src = \"../../../assets/images/menu.svg\"></div>\n"

    ps += "    <div id = \"details\">\n"
    ps += "      <table>\n"
    ps += "        <tr><td>Timestamp:</td><td>%s</td></tr>\n" % (time_stamp)
    ps += "        <tr><td>&nbsp;</td><td>&nbsp;</td></tr>\n"
    ps += "        <tr><td>Latitude:</td><td>%.6f &deg;</td></tr>\n" % (lat)
    ps += "        <tr><td>Longitude:</td><td>%.6f &deg;</td></tr>\n" % (lon)
    ps += "        <tr><td>Altitude:</td><td>%.1f m;</td></tr>\n" % (alt)
    ps += "      </table>\n"
    ps += "    </div>\n"
    ps += "  </div>\n"
    ps += "  <div id = \"data\">\n"
    ps += "    <div id = \"canvas-container\" onclick = \"$('#mask, #xyCbox').fadeIn();\"></div>\n"
    ps += "  </div>\n"
    ps += "  <div id = \"frame-indicator\">Frame %d of %d</div>\n" % (i, N)
    ps += "  <div id = \"back-button\" class = \"button\" onclick = \"prevFrame();\"><img src = \"../../../assets/images/back.svg\"></div>\n"
    ps += "  <div id = \"forward-button\" class = \"button\" onclick = \"nextFrame();\"><img src = \"../../../assets/images/forward.svg\"></div>\n"
    ps += "</div>\n"
    ps += "<div id = \"mask\" onclick = \"$('#mask, #menu, #xyCbox').fadeOut();\"></div>\n"
    ps += "<div id = \"menu\">\n"
    ps += "  <div id = \"menu-title\">Select a dataset</div>\n"
    ps += "  <img src = \"assets/images/close.svg\" id = \"menu-close\" onclick = \"$('#mask, #menu').fadeOut();\">\n"
    ps += "  <ul>\n"
    ps += "    <li><a href=\"%s\">Dataset 1</a></li>\n" % ("this")
    ps += "    <li>Dataset 2</li>\n"
    ps += "  </ul>\n"
    ps += "</div>\n"
    ps += "<div id = \"xyCbox\">\n"
    ps += "  <textarea readonly>%s</textarea>\n" % (xyC)
    ps += "</div>\n"
    ps += "\n"
    ps += "<div id = \"loading\">Loading</div>\n"
    ps += "\n"
    ps += "<script>\n"
    ps += "\n"
    ps += "var prevFrameLocation = \"%s\";\n" % (prev_loc)
    ps += "\n"
    ps += "var nextFrameLocation = \"%s\";\n" % (next_loc)
    ps += "\n"
    ps += "var frameImageUrl = '../png/%s_%s.png'\n" % (f.getChipId(), make_time_dir(f.getStartTimeSec()))
    ps += "\n"
    ps += "var r = Raphael(\"canvas-container\", '100%', '100%');\n"
    ps += "\n"
    ps += "var h = 524; var w = 524; var b_w = 6; var s_w = w - 2*b_w;\n"
    ps += "\n"
    ps += "var bg_panel = r.rect(0,0,w,h).attr({fill:'#999999', stroke:'#000000'});\n"
    ps += "\n"
    ps += "var bg_screen = r.rect(b_w,b_w,w - 2*b_w,h - 2*b_w).attr({fill:'#000000', stroke:'#000000'});\n"
    ps += "\n"
    ps += "var frame = r.image(frameImageUrl, 8, 8, 508, 508);\n"
    ps += "\n"
    ps += "function prevFrame() {\n"
    ps += "  window.location.href = prevFrameLocation;\n"
    ps += "};\n"
    ps += "\n"
    ps += "function nextFrame() {\n"
    ps += "  window.location.href = nextFrameLocation;\n"
    ps += "};\n"
    ps += "\n"
    ps += "$(document).keydown(function(e) {\n"
    ps += "  switch(e.which) {\n"
    ps += "    case 37: // left\n"
    ps += "      prevFrame();\n"
    ps += "    break;\n"
    ps += "\n"
    ps += "    case 39: // right\n"
    ps += "      nextFrame();\n"
    ps += "    break;\n"
    ps += "\n"
    ps += "    default: return;\n"
    ps += "  }\n"
    ps += "  e.preventDefault();\n"
    ps += "});\n"
    ps += "\n"
    ps += "</script>"

    return ps
