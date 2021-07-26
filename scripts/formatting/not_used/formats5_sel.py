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


def get_filename(textfile):
    filename, ext = os.path.basename(textfile).split(".")
    return filename


def read_text(text):
    tagged = text.split(" ")
    tagged = [token for token in tagged if token]
    return tagged



def select_features(tagged, params):
    if params["token"] == "lemma":
        if params["pos"] == "all":
            features = [token.split("_")[2] for token in tagged if len(token.split("_")) == 3]
        else:
            features = [token.split("_")[2] for token in tagged if
                        len(token.split("_")) == 3 and token.split("_")[1] in params["pos"]]
    if params["token"] == "pos":
        if params["pos"] == "all":
            features = [token.split("_")[1] for token in tagged if len(token.split("_")) == 3]
        else:
            features = [token.split("_")[1] for token in tagged if
                        len(token.split("_")) == 3 and token.split("_")[1] in params["pos"]]
    features = "\n".join(features)
    return features


def create_ngrams(features, params): 
    ngrams = zip(*[features[i:] for i in range(params["ngram"])])
    ngrams = [" ".join(ngram) for ngram in ngrams]
    ngrams = "\n".join(ngrams)
    return ngrams


def save_features(features, ngrfolder, filename): 
    filepath = join(ngrfolder, filename+".txt")
    with open(filepath, "w", encoding="utf-8") as outfile:
        outfile.write(features)
    

# ====================================
# MAIN
# ====================================

def main(taggedfile, ngrfolder, params):
    print("\nformats5_sel")
    if not os.path.exists(ngrfolder):
        os.makedirs(ngrfolder)
    with open(taggedfile, "r", encoding="utf-8") as f:
        for text in f.read().split("\n"):
            filename, content = text.split("\t")
            print("--"+filename)
            tagged = read_text(content)
            features = select_features(tagged, params)
            save_features(features, ngrfolder, filename)
            ngrams = create_ngrams(features, params)
            #save_features(ngrams, ngrfolder, filename)

if __name__ == "__main__":
    main(sourcefolder, ngrfolder, params)
