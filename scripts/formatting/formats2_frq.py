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
from collections import Counter

# ====================================
# FUNCTIONS
# ====================================

def select_features(tagged, params):
    if params["casing"] == "lower": 
        features = [token for token in tagged]
    else: 
        features = [token.split("_")[0] for token in tagged]
    return features


def get_counts(features): 
    counts = pd.Series(Counter(features))
    counts.sort_values(inplace=True, ascending=False)
    return counts


def save_counts(counts, frqfolder, filename):
    with open(filepath, "w", encoding="utf-8") as outfile:
        counts.to_csv(outfile, sep="\t")

# ====================================
# MAIN
# ====================================

def create_frq(taggedfile, frqfolder, params):
    with open(taggedfile, "r", encoding="utf-8") as f:
        for text in f.read().split("\n"):
            filename, content = text.split("\t")
            print("--" + filename)
            tagged = content.split(" ")
            features = select_features(tagged, params)
            counts = get_counts(features)
            save_counts(counts, frqfolder, filename)


def create_tdm(segmentfile, frqfolder, params):
    with open(segmentfile, "r", encoding="utf-8") as f:
        for text in f.read().split("\n"):
            filename, content = text.split("\t")
            print("--" + filename)
            tagged = content.split(" ")
            features = select_features(tagged, params)
            counts = get_counts(features)
            save_counts(counts, frqfolder, filename)


def main(inputfile, frqfolder, params):
    print("\nformats2_frq")
    frqfolder.mkdir(exist_ok=True, parents=True)
    filepath = join(frqfolder, ".txt")
    if inputfile.stem == "tagged":
        create_frq(inputfile, frqfolder, params)
    else:
        create_tdm(inputfile, frqfolder, params)

if __name__ == "__main__":
    main(sourcefolder, frqfolder, params)
