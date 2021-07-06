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
from formatting import formats5_sel
from os.path import join
from scripts.parameters import params

# ==================================
# Parameters (need to be set in scripts/parameters)
# ==================================

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
srcfolder = join(wdir, "4_plain")
ngrfolder = join(wdir, "3_formats", "ngr", "")
selfolder = join(wdir, "3_formats", "sel", "")


# ==================================
# Call imported scripts
# ==================================



#formats0_tagging.main(plainfolder, taggedfolder, params)

#formats2_frq.main(taggedfile, frqfolder, params)
formats5_ngr.main(taggedfile, ngrfolder, params)
#formats5_sel.main(taggedfile, selfolder, params)

#formats1_tkn.main(taggedfile, tknfolder, params)

#formats4_src.main(taggedfile, srcfolder, params)

#formats3_tdm.main(taggedfolder, tdmfolder, params)
