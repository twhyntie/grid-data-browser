#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 CERN@school - Processing Frames

 See the README.md file and the GitHub wiki for more information.

 http://cernatschool.web.cern.ch

"""

# Import the code needed to manage files.
import os, glob

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg

#...for file manipulation.
from shutil import rmtree

# Import the JSON library.
import json

#...for processing the datasets.
from cernatschool.dataset import Dataset

#...for making time.
from cernatschool.handlers import make_time_dir

#...for making the frame and clusters images.
from visualisation import makeFrameImage, makeKlusterImage

#...for creating a browser page for a given datafile.
from pagemaker import make_browser_page


if __name__ == "__main__":

    print("*")
    print("*======================================*")
    print("* CERN@school - local frame processing *")
    print("*======================================*")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("inputPath",       help="Path to the input dataset.")
    parser.add_argument("outputPath",      help="The path for the output files.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The path to the data file.
    datapath = args.inputPath

    ## The output path.
    outputpath = args.outputPath

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    # Configure the logging.
    lg.basicConfig(filename=os.path.join(outputpath, 'log_process-frames.log'), filemode='w', level=level)

    print("*")
    print("* Input path          : '%s'" % (datapath))
    print("* Output path         : '%s'" % (outputpath))
    print("*")


    # Set up the directories
    #------------------------

    # Check if the output directory exists. If it doesn't, quit.
    if not os.path.isdir(outputpath):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (outputpath))

    # Create the subdirectories.

    ## The path to the frame images.
    frame_image_path = os.path.join(outputpath, "png")
    #
    if os.path.isdir(frame_image_path):
        rmtree(frame_image_path)
        lg.info(" * Removing directory '%s'..." % (frame_image_path))
    os.mkdir(frame_image_path)
    lg.info(" * Creating directory '%s'..." % (frame_image_path))
    lg.info("")

    ## The path to the frame HTML pages.
    web_page_path = os.path.join(outputpath, "html")
    #
    if os.path.isdir(web_page_path):
        rmtree(web_page_path)
        lg.info(" * Removing directory '%s'..." % (web_page_path))
    os.mkdir(web_page_path)
    lg.info(" * Creating directory '%s'..." % (web_page_path))
    lg.info("")

    ## The path to the data files.
    dat_files_path = os.path.join(datapath, "ASCIIxyC")

    ## The dataset to process.
    ds = Dataset(dat_files_path)

    ## The path to the geographic information JSON file.
    geo_json_path = os.path.join(outputpath, "geo.json")
    #
    if not os.path.exists(geo_json_path):
        raise IOError("* ERROR: no geographics metadata JSON!")

    ## The geographic information JSON file.
    mf = open(geo_json_path, "r")
    #
    md = json.load(mf)
    mf.close()

    ## The latitude [deg.]
    lat = float(md['lat'])

    ## The longitude [deg.]
    lon = float(md['lon'])

    ## The altitude [m].
    alt = float(md['alt'])

    ## The frames from the dataset.
    frames = ds.getFrames((lat, lon, alt))

    lg.info("* Found %d datafiles:" % (len(frames)))

    ## A list of frames.
    mds = []

    # Loop over the frames and upload them to the DFC.
    for i, f in enumerate(frames):

        ## The basename for the data frame, based on frame information.
        bn = "%s_%s" % (f.getChipId(), make_time_dir(f.getStartTimeSec()))

        # Create the frame image.
        makeFrameImage(bn, f.getPixelMap(), frame_image_path)

        # Create the metadata dictionary for the frame.
        metadata = {
            "id"          : bn,
            #
            "chipid"      : f.getChipId(),
            "hv"          : f.getBiasVoltage(),
            "ikrum"       : f.getIKrum(),
            #
            "lat"         : f.getLatitude(),
            "lon"         : f.getLongitude(),
            "alt"         : f.getAltitude(),
            #
            "start_time"  : f.getStartTimeSec(),
            "end_time"    : f.getEndTimeSec(),
            "acqtime"     : f.getAcqTime(),
            #
            "n_pixel"     : f.getNumberOfUnmaskedPixels(),
            "occ"         : f.getOccupancy(),
            "occ_pc"      : f.getOccupancyPc(),
            #
            "n_kluster"   : f.getNumberOfKlusters(),
            "n_gamma"     : f.getNumberOfGammas(),
            "n_non_gamma" : f.getNumberOfNonGammas(),
            #
            "ismc"        : int(f.isMC())
            }

        # Add the frame metadata to the list of frames.
        mds.append(metadata)

        # Create the web page for the frame.

        ## The filename of the HTML page to create.
        page_filename = os.path.join(web_page_path, bn + ".html")

        ## The filename of the previous frame in the dataset.
        prev_filename = bn + ".html"
        #
        if i > 0:
            prev_filename = "%s_%s.html" % (frames[i-1].getChipId(), make_time_dir(frames[i-1].getStartTimeSec()))

        ## The filename of the next frame in the dataset.
        next_filename = bn + ".html"
        if i < (len(frames) - 1):
            next_filename = "%s_%s.html" % (frames[i+1].getChipId(), make_time_dir(frames[i+1].getStartTimeSec()))

        # Make the page.
        with open(page_filename, "w") as pf:
            pf.write(make_browser_page(f, i+1, len(frames), prev_filename, next_filename, f.getPayloadString()))

        #break # TMP - uncomment to only process the first frame.


    ## The frame metadata JSON file name.
    frame_metadata_path = "frames.json"
    #frame_metadata_path = "%s_%s.json" % (frames[0].getChipId(), make_time_dir(frames[0].getStartTimeSec()))
    #
    # Write out the frame information to a JSON file.
    with open(os.path.join(outputpath, frame_metadata_path), "w") as jf:
        json.dump(mds, jf)
