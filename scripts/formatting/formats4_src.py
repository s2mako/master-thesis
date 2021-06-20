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
from os.path import join
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


def create_segments(tagged, params):
    """
    Creates segments out of tagged Text.

    """
    segments = [tagged[x:x+params["seglen"]] for x in range(0, len(tagged), params["seglen"])]
    return segments


def scramble_segments(segments, params): 
    scrambled = []
    for seg in segments: 
        random.shuffle(seg) # scrambling
        seg = " ".join(seg)
        scrambled.append(seg)
    return scrambled
   

def save_scrambled(scrambled, srcfolder, params):
    seglen = params["seglen"]
    filepath = join(srcfolder, f"src-{seglen}.txt")
    scrambled = "\n".join(scrambled)
    with open(filepath, "a", encoding="utf-8") as outfile:
        outfile.write(scrambled)
        outfile.write("\n")

# ====================================
# MAIN
# ====================================

def main(taggedfile, srcfolder, params):
    print("\nformats4_tdm")
    if not os.path.exists(srcfolder):
        os.makedirs(srcfolder)
    with open(taggedfile, "r", encoding="utf-8") as f:
        for text in f.read().split("\n"):
            filename, content = text.split("\t")
            print("--" + filename)
            tagged = content.split(" ")
            segments = create_segments(tagged, params)
            scrambled = scramble_segments(segments, params)
            save_scrambled(scrambled, srcfolder, params)

if __name__ == "__main__":
    main(sourcefolder, srcfolder, params)
