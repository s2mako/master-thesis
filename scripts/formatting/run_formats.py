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
coll = r"acd"
seglen = 50  # segment length. 0 creates a tdm instead src by "tdm_to_plain.py"
casing = "lower" # "lower"|"original"
token = "lemma" # "lemma"|"pos|"mixed" ## expand to wordforms
#pos = ["NN0", "NN1", "NN2", "AJ0", "AV0", "VVG", "VVD", "VVN"] # list of POS-tags or "all"
#pos = ["DET:ART", "DET:POS", "PRP", "PRP:det", "PUN", "PRO:PER", "PRO:REL", "PRO:DEM", "KON"] # list of POS-tags or "all"
#pos = ["NN", "NE", "ADV", "ADJA", "ADJD", "VVFIN", "VAFIN"]
#pos = ["NN0", "NN1", "NN2", "VVB", "VVD", "VVG", "AJ0", "AJ1", "AJC", ] # English
pos = ["NN0", "NN1", "NN2", "VVB", "VVD", "VVG", "AJ0", "AJ1", "AJC", ]
#pos = "all"
ngram = 3

params = {"lang":lang, "coll":coll, "seglen":seglen, "casing":casing, "token":token, "pos":pos,
          "ngram":ngram}


# ==================================
# Files and folders (don't change)
# ==================================

wdir = join("../..")
plainfolder = join(wdir, "1_plain")
taggedfolder = join(wdir, "2_tagged")

tknfolder = join(wdir, "3_formats", "tkn", token, "")
frqfolder = join(wdir, "3_formats", "frq"+"-"+casing, "")
tdmfolder = join(wdir, "3_formats", "tdm", str(seglen), "")
srcfolder = join(wdir, "3_formats", "src"+"-"+str(seglen), "")
ngrfolder = join(wdir, "3_formats", "ngr"+"-"+token+"-"+str(ngram), "")
selfolder = join(wdir, "3_formats", "sel"+"-"+token+"-"+str(ngram), "")


# ==================================
# Call imported scripts
# ==================================

#formats0_tagging.main(plainfolder, taggedfolder, params)
#formats1_tkn.main(taggedfolder, tknfolder, params)
#formats2_frq.main(taggedfolder, frqfolder, params)
#formats3_tdm.main(taggedfolder, tdmfolder, params)
#formats4_src.main(taggedfolder, srcfolder, params)
#formats5_ngr.main(taggedfolder, ngrfolder, params)
formats5_sel.main(taggedfolder, selfolder, params)
