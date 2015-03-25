#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 CERN@school - Making browser pages

 See the README.md file and the GitHub wiki for more information.

 http://cernatschool.web.cern.ch

"""

# Import the code needed to manage files.
import os, glob

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg

# Import the JSON library.
import json

#...for processing the datasets.
#from cernatschool.dataset import Dataset

#...for creating a browser page for a given datafile.
from pagemaker import make_browser_page

if __name__ == "__main__":

    print("*")
    print("*===========================*")
    print("* CERN@school - page making *")
    print("*===========================*")

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
    lg.basicConfig(filename='%s/log_make_pages.log' % (outputpath), filemode='w', level=level)

    print("*")
    print("* Input path          : '%s'" % (datapath))
    print("* Output path         : '%s'" % (outputpath))
    print("*")

    ## The name of the JSON file containing the frame information.
    frame_json_filename = os.path.join(datapath, "frames.json")
    #
    if not os.path.exists(frame_json_filename):
        raise IOError("* ERROR: frames.json not found!")

    ## The frame JSON file.
    ff = open(frame_json_filename, "r")

    ## The frame data.
    fd = json.load(ff)

    ff.close()

    # Loop over the frames, making a page for each.
    for i, f in enumerate(fd):

        ## The filename of the HTML page to create.
        page_filename = outputpath + "/" + f['id'] + ".html"

        ## The filename of the previous frame in the dataset.
        prev_filename = f['id'] + ".html"
        if i > 0:
            prev_filename = fd[i-1]['id'] + ".html"

        ## The filename of the next frame in the dataset.
        next_filename = f['id'] + ".html"
        if i < (len(fd) - 1):
            next_filename = fd[i+1]['id'] + ".html"

        # Make the page.
        with open(page_filename, "w") as pf:
            pf.write(make_browser_page(f, i+1, len(fd), prev_filename, next_filename, "1\t4\t265"))
