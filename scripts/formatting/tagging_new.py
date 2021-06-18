#!/usr/bin/env python3
# Filename: run_treetagger.py
# Author: #cf

"""
Create annotated text from plain text.
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
import treetaggerwrapper
from os.path import join


# ====================================
# FUNCTIONS
# ====================================


def get_filename(textfile):
    filename, ext = os.path.basename(textfile).split(".")
    return filename


def read_text(textfile):
    with open(textfile, "r") as infile:
        text = infile.read()
        return text


def apply_tagger(text, params):
    tagger = treetaggerwrapper.TreeTagger(TAGLANG=params["lang"])
    tagged = tagger.tag_text(text)
    tagged = "\n".join(tagged)
    return tagged


def save_tagged(segments, taggedfolder, params):
    if params["seglen"]:
        filepath = join(taggedfolder, f"tagged-{params['seglen']}.txt")
    else:
        filepath = join(taggedfolder, "tagged.txt")
    with open(filepath, "w", encoding="utf-8") as outfile:
        for seg in segments:
            outfile.write(seg)


def create_segments(plainfolder, params):
    for textfile in glob.glob(join(plainfolder, "*.txt")):
        filename = get_filename(textfile)
        print("--" + filename)
        text = read_text(textfile)
        tagged = apply_tagger(text, params)
        yield f"<DOC>\n"
        if params["seglen"]:
            i = 1
            for line in tagged.split("\n"):
                i += 1
                yield line
                yield "\n"
                if (i == params["seglen"]):
                    yield "<SEG>\n"
                    i = 1
        else:
            yield tagged
            yield "\n"


# ====================================
# MAIN
# ====================================

def main(plainfolder, taggedfolder, params):
    print("\nformats0_tagging")
    if not os.path.exists(taggedfolder):
        os.makedirs(taggedfolder)
    save_tagged(create_segments(plainfolder, params), taggedfolder, params)


if __name__ == "__main__":
    main(plainfolder, taggedfolder, params)
