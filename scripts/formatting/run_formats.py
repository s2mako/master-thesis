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
from pathlib import Path

import formats0_tagging
import formats0_segmenting
import formats1_tkn
import formats2_frq
import formats3_tdm
import formats4_src
import formats5_ngr
from os.path import join
from library import create_segfolder
from scripts.parameters import params
from pathlib import Path

# ==================================
# Parameters (need to be set in scripts/parameters)
# ==================================

# ====================================
# FUNCTIONS
#====================================


def check_inputfile(path, taggedfile):
    if not path.is_file():
        print("Segmentfile not found. Creating segmentfile ", params['seglen'])
        formats0_segmenting.main(taggedfile, input_segmentsfolder, params)
    return path

# ==================================
# Files and folders (done't change)
# ==================================

wdir = Path("../..")
sourcefolder = wdir.joinpath("0_source")
taggedfolder = wdir.joinpath("1_tagged")
formatsfolder = wdir.joinpath( "3_formats")
taggedfile = wdir.joinpath("1_tagged", "tagged.txt")
input_segmentsfolder = wdir.joinpath("2_segmented")
segmentfile_name = input_segmentsfolder.joinpath(f"segmented-{params['seglen']}.txt")
input_segmentfile = check_inputfile(segmentfile_name, taggedfile)

output_segmentsfolder = formatsfolder.joinpath(f"seglen-{params['seglen']}")
tknfolder = output_segmentsfolder.joinpath("tkn")
frqfolder = output_segmentsfolder.joinpath("frq")
tdmfolder = output_segmentsfolder.joinpath("tdm")
ngrfolder = output_segmentsfolder.joinpath("ngr")
selfolder = output_segmentsfolder.joinpath("sel")
srcfolder = wdir.joinpath("4_plain", f"seglen-{params['seglen']}")


# ==================================
# Call imported scripts
# ==================================

#formats0_tagging.main(plainfolder, taggedfolder, params)

#formats2_frq.main(taggedfile, frqfolder, params)
formats5_ngr.main(input_segmentfile, output_segmentsfolder, params)
#formats5_ngr.main(taggedfile, output_segmentsfolder, params)

#formats1_tkn.main(input_segmentfile, output_segmentsfolder, params)

#formats4_src.main(input_segmentfile, srcfolder, params)

#formats3_tdm.main(taggedfile, tdmfolder, params)
