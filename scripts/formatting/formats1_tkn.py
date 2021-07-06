#!/usr/bin/env python3
# Filename: run_treetagger.py
# Author: #cf

"""
Create a derived format from full, annotated text.
"""

# ====================================
# IMPORTS
# ====================================

import os
from os.path import join, exists


# ====================================
# FUNCTIONS
# ====================================

def select_features(tagged, params):
    features = []
    if params["token"] == "lemma":
        features = [token.split("_")[2] for token in tagged if len(token.split("_")) == 3]
    elif params["token"] == "pos":
        features = [token.split("_")[1] for token in tagged if len(token.split("_")) == 3]
    elif params["token"] == "mixed":
        features = []
        for token in tagged:
            if len(token.split("_")) == 3:
                if token.split("_")[1] in params["pos"]:
                    features.append(token)
                else:
                    features.append(token.split("_")[1])
    features = " ".join(features)
    return features


def save_features(features, tknfolder, params, textfilename):
    outfilename = "tkn-" + "_".join(sorted(params["pos"]))
    filepath = join(tknfolder, f"{outfilename}.txt")
    with open(filepath, "a", encoding="utf-8") as outfile:
        outfile.write(textfilename)
        outfile.write("\t")
        outfile.write(features)
        outfile.write("\n")


def check_outfile_path(srcfolder, params):
    pos = params["pos"]
    filename = f"tkn-{'_'.join(pos)}.txt"
    outfile_path = join(srcfolder, filename)
    if exists(outfile_path):
        print("--clearing existing file: " + filename)
        f = open(outfile_path, "w")
        f.close()
    return outfile_path

# ====================================
# MAIN
# ====================================

def main(taggedfile, tknfolder, params):
    print("\nformats1_tkn")
    if not os.path.exists(tknfolder):
        os.makedirs(tknfolder)
    outfile_path = check_outfile_path(tknfolder, params)  # deletes content of existing file
    with open(taggedfile, "r", encoding="utf-8") as f:
        for text in f.read().split("\n"):
            filename, content = text.split("\t")
            print("--" + filename)
            tagged = content.split(" ")
            features = select_features(tagged, params)
            save_features(features, tknfolder, params, filename)


if __name__ == "__main__":
    main(sourcefolder, tknfolder, params)
