"""
Pipeline to create a corpus for topic modeling from an plain full-text corpus or pseudo plain
text constructed from derived format.

"""

# =================================
# Import statements
# =================================

from pathlib import Path
import preprocess_0_tagged_to_plain
import preprocess_1_tkn_to_plain
import preprocess_2_frq_to_plain
#import preprocess_3_src_to_plain
#import preprocess_4_ngr_to_plain
import preprocess

# ==================================
# Parameters In-Folder
# ==================================

active_segmentation = True
seglen_write = 500  # as integer - determines segment length in preprocess_tm.py
seglen_read = 5  # as integer - selects subfolder in 3_formats

pos = ["NN", "NNS"]
format = "tkn"  # "tkn", "src", "original", "tdm", "ngr"
step = "tm"  # "tm"|"pseudoplain"
csv = "src"  # tdm|src

params = {"seglen": seglen_write, "filter": filter, "format": format, "active_segmentation": active_segmentation,
          "seglen_read": seglen_read, "seglen_write": seglen_write, "pos": pos}

# ==================================
# Files and folders
# ==================================

wdir = Path("../..")
resourcesdir = wdir.joinpath("resources")
stoplist = resourcesdir.joinpath("stoplist.txt")
sourcedir = wdir.joinpath("0_source")
plaindir = wdir.joinpath("1_plain", format)
taggedfile = wdir.joinpath("2_tagged", "tagged.txt")
formatsdir = wdir.joinpath("3_formats")
pseudodir = wdir.joinpath("4_plain")
# corpusdir = wdir.joinpath("5_corpus", format, str(seglen))
corpusdir = wdir.joinpath("5_corpus")

# format sources
tknsource = formatsdir.joinpath("tkn")
tknfile = tknsource.joinpath(f"tkn-{'_'.join(pos)}.txt")
tdmsource = formatsdir.joinpath("tkn-tm")
srcsource = formatsdir.joinpath("src", str(seglen_read))
frqsource = formatsdir.joinpath("frq")
# ngrdir = formatsdir.joinpath("ngr"+"-"+token+"-"+str(ngram), "")

# pseudoplain target
tknpseudodir = pseudodir.joinpath("tkn-tm")
#tdmpseudodir = pseudodir.joinpath("tdm", "_".join(filter))
#srcpseudodir = pseudodir.joinpath("src", str(seglen_read), "_".join(filter))


# ====================================
# FUNCTIONS
# ====================================

def get_csvsource(csv):
    if csv == "src":
        return srcsource
    else:
        return tknsource


def get_csvpseudo(csv):
    if csv == "src":
        return srcpseudodir
    else:
        return tknpseudodir


def get_sourcedir(format):
    if format == "tkn":
        return tknpseudodir
    elif format == "tdm":
        return tdmpseudodir
    elif format == "src":
        return srcpseudodir
    elif format == "original":
        return plaindir
    else:
        return


# ==================================
# Call imported scripts
# ==================================

#preprocess_0_tagged_to_plain.main(taggedfile, pseudodir, params)
#preprocess_0_tagged_to_plain.main(tknfile, pseudodir, params)
#preprocess_2_frq_to_plain.main(frqsource, pseudodir, params)
preprocess.main(pseudodir, corpusdir, stoplist, params)
