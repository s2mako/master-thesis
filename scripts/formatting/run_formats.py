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

# ==================================
# Parameters (need to be set in scripts/parameters)
# ==================================

# ==================================
# Files and folders (done't change)
# ==================================

wdir = join("../..")
sourcefolder = join(wdir, "0_source")
taggedfolder = join(wdir, "1_tagged")
formatsfolder = join(wdir, "3_formats")
taggedfile = join(wdir, "1_tagged", "tagged.txt")
input_segmentsfolder = join(wdir, "2_segmented")
input_segmentfile = join(input_segmentsfolder, f"segmented-{params['seglen']}.txt")

output_segmentsfolder = join(formatsfolder, f"seglen-{params['seglen']}")
tknfolder = join(output_segmentsfolder, "tkn")
frqfolder = join(output_segmentsfolder, "frq")
tdmfolder = join(output_segmentsfolder, "tdm")
ngrfolder = join(output_segmentsfolder, "ngr")
selfolder = join(output_segmentsfolder, "sel")
srcfolder = join(wdir, "4_plain", f"seglen-{params['seglen']}")



# ==================================
# Call imported scripts
# ==================================
#formats0_tagging.main(plainfolder, taggedfolder, params)


#formats0_segmenting.main(taggedfile, input_segmentsfolder, params)

#formats2_frq.main(taggedfile, frqfolder, params)
formats5_ngr.main(input_segmentfile, output_segmentsfolder, params)
#formats5_ngr.main(taggedfile, output_segmentsfolder, params)

#formats1_tkn.main(input_segmentfile, output_segmentsfolder, params)

#formats4_src.main(input_segmentfile, srcfolder, params)

#formats3_tdm.main(taggedfile, tdmfolder, params)
