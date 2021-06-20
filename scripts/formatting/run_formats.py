#!/usr/bin/env python3
# author: #cf, 2020.

"""
Pipeline to create derived formats from an annotated full-text corpus.

Presupposes the existence of an annotated full text in TSV format,
with one token per line and Tab-separated annotations. 

Creates a derived format suitable for applications like stylometric 
text similarity measurement, topic modeling or analysis of distinctive
features. 

"""


# =================================
# Import statements
# =================================

import formats0_tagging
import formats1_tkn
import formats2_frq
import formats3_tdm
import formats4_src
import formats5_ngr
from os.path import join


# ==================================
# Parameters (need to be set)
# ==================================
from formatting import formats5_sel

lang = "en"
coll = "acd"
seglen = 100  # segment length. 0 creates a tdm instead src by "tdm_to_plain.py"
casing = "lower" # "lower"|"original"
token = "mixed" # "lemma"|"pos|"mixed"|"tm" ## expand to wordforms
#pos = ["NN0", "NN1", "NN2", "AJ0", "AV0", "VVG", "VVD", "VVN"] # list of POS-tags or "all"
#pos = ["DET:ART", "DET:POS", "PRP", "PRP:det", "PUN", "PRO:PER", "PRO:REL", "PRO:DEM", "KON"] # list of POS-tags or "all"
#pos = ["NN", "NE", "ADV", "ADJA", "ADJD", "VVFIN", "VAFIN"]
#pos = ["NN0", "NN1", "NN2", "VVB", "VVD", "VVG", "AJ0", "AJ1", "AJC", ] # English
#pos = ["NN0", "NN1", "NN2", "VVB", "VVD", "VVG", "AJ0", "AJ1", "AJC", ]
pos = ["NN", "NNS"]
#pos = "all"
ngram = 3

params = {"lang":lang, "coll":coll, "seglen":seglen, "casing":casing, "token":token, "pos":pos,
          "ngram":ngram}


# ==================================
# Files and folders (don't change)
# ==================================

wdir = join("../..")
plainfolder = join(wdir, "1_plain/original")
taggedfolder = join(wdir, "2_tagged", "")
formatsfolder = join(wdir, "3_formats")
taggedfile = join(wdir, "2_tagged", "tagged.txt")

tknfolder = join(wdir, "3_formats", "tkn")
frqfolder = join(wdir, "3_formats", "frq", "")
tdmfolder = join(wdir, "3_formats", "tdm", "")
srcfolder = join(wdir, "3_formats", "src")
ngrfolder = join(wdir, "3_formats", "ngr", "")
selfolder = join(wdir, "3_formats", "sel", "")


# ==================================
# Call imported scripts
# ==================================

#formats0_tagging.main(plainfolder, taggedfolder, params)
formats1_tkn.main(taggedfile, tknfolder, params)
# formats2_frq.main(taggedfile, frqfolder, params)
# formats3_tdm.main(taggedfolder, tdmfolder, params)
# formats4_src.main(taggedfile, srcfolder, params)
# formats5_ngr.main(taggedfolder, ngrfolder, params)
# formats5_sel.main(taggedfolder, selfolder, params)
