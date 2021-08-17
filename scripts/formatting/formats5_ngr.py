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
from pathlib import Path

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
    features = []
    if params["token"] == "lemma":
        if params["pos"] == "all": 
            features = [token.split("_")[2] for token in tagged if len(token.split("_"))== 3]
        else: 
            features = [token.split("_")[2] for token in tagged if len(token.split("_"))== 3 and token.split("_")[1] in params["pos"]]
    if params["token"] == "pos":
        if params["pos"] == "all": 
            features = [token.split("_")[1] for token in tagged if len(token.split("_"))==3]
        else: 
            features = [token.split("_")[1] for token in tagged if len(token.split("_"))==3 and token.split("_")[1] in params["pos"]]
    if params["token"] == "wordform":
        if params["pos"] == "all": 
            features = [token.split("_")[0].lower() for token in tagged if len(token.split("_"))==3]
        else: 
            features = [token.split("_")[0].lower() for token in tagged if len(token.split("_"))==3 and token.split("_")[1] in params["pos"]]
    if params["token"] == "mixed":
        if params["pos"] == "all":
            features = [token.lower() for token in tagged if len(token.split("_"))==3]
        else:
            features = [token.lower() for token in tagged if len(token.split("_"))==3 and token.split("_")[1] in params["pos"]]
    return features


def create_ngrams(ngrams, params):
    ngrams = zip(*[ngrams[i:] for i in range(params["ngram"])])
    ngrams = [" ".join(ngram) for ngram in ngrams]
    return ngrams


def count_allngrams(allngrams, params):
    from collections import Counter
    allcounts = dict(Counter(allngrams))
    filteredcounts = dict()
    for (key, value) in allcounts.items():
        if value > params["threshold"]:
            filteredcounts[key] = value
    print(filteredcounts)
    return filteredcounts


def save_counts(outfile, counts):
    counts = pd.Series(counts)
    counts.sort_values(ascending=False, inplace=True)
    with open(outfile, "a", encoding="utf8") as outfile:
        counts.to_csv(outfile, sep="\t")
        outfile.write("<seg>")

    

# ====================================
# MAIN
# ====================================

def main(segmentfile, ngrfolder, params):
    print("\nformats5_ngr")
    ngrfolder = Path(ngrfolder)
    ngrfolder.mkdir(parents=True, exist_ok=True)
    outfile = ngrfolder.joinpath(f"allngrs-{params['ngram']}_thr-{params['threshold']}.tsv")
    if outfile.is_file(): outfile.unlink()
    with open(segmentfile, "r", encoding="utf-8") as f:
        for text in f.read().split("\n"):
            allngrams = []
            filename, content = text.split("\t")
            print("--"+filename)
            tagged = read_text(content)
            features = select_features(tagged, params)
            ngrams = create_ngrams(features, params)
            allngrams.extend(ngrams)
            filteredcounts = count_allngrams(allngrams, params)
            save_counts(outfile, filteredcounts)


if __name__ == "__main__":
    main(taggedfolder, ngrfolder, params)
