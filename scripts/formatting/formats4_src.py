#!/usr/bin/env python3
# Filename: run_treetagger.py
# Author: #cf

"""
Create a derived format from full, annotated text.
"""

# ====================================
# IMPORTS
# ====================================

import glob
import os
import re
import csv
import pandas as pd
import numpy as np
from os.path import join, exists
import random

# ====================================
# FUNCTIONS
# ====================================


def get_filename(textfile):
    filename, ext = os.path.basename(textfile).split(".")
    return filename


def read_text(textfile):
    with open(textfile, "r") as infile:
        tagged = infile.read()
        return tagged

def scramble_segments(segments, params): 
    scrambled = []
    for seg in segments: 
        random.shuffle(seg) # scrambling
        seg = " ".join(seg)
        scrambled.append(seg)
    return scrambled
   

def save_scrambled(scrambled, outfile_path, params):
    scrambled = "\n".join(scrambled)
    with open(outfile_path, "a", encoding="utf-8") as outfile:
        outfile.write(scrambled)
        outfile.write("\n")


def check_outfile_path(srcfolder, params):
    seglen = params["seglen"]
    filename = f"src-{seglen}.txt"
    outfile_path = join(srcfolder, filename)
    if exists(outfile_path):
        print("--clearing existing file: " + filename)
        f = open(outfile_path, "w")
        f.close()
    return outfile_path

# ====================================
# MAIN
# ====================================


def main(taggedfile, srcfolder, params):
    print("\nformats4_src")
    outfile_path = check_outfile_path(srcfolder, params)  # deletes content of existing file
    if not exists(srcfolder):
        os.makedirs(srcfolder)
    with open(taggedfile, "r", encoding="utf-8") as f:
        for text in f.read().split("\n"):
            filename, content = text.split("\t")
            print("--" + filename)
            tagged = content.split(" ")
            segments = create_segments(tagged, params)
            scrambled = scramble_segments(segments, params)
            save_scrambled(scrambled, outfile_path, params)

if __name__ == "__main__":
    main(sourcefolder, srcfolder, params)
