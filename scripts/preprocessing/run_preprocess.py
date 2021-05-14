"""
Pipeline to create a corpus for topic modeling from an plain full-text corpus or pseudo plain
text constructed from derived format.

"""


# =================================
# Import statements
# =================================

from pathlib import Path
from preprocessing import preprocess_tm, csv_to_plain, tkn_to_plain

# ==================================
# Parameters (need to be set)
# ==================================

formats_seglen = 5
seglen = 50  # segment length
filter = ["NN", "VV"]
format = "tkn"
csv = "src"  # tdm|src

params = {"seglen": seglen, "filter": filter, "format": format}

# ==================================
# Files and folders
# ==================================

wdir = Path("../..")
resourcesdir = wdir.joinpath("resources")
stoplist = resourcesdir.joinpath("stoplist.txt")
plaindir = wdir.joinpath("1_plain")
formatsdir = wdir.joinpath("3_formats")
pseudodir = wdir.joinpath("4_pseudoplain")
corpusdir = wdir.joinpath("5_corpus", format, str(seglen))


# format sources
tknsource = formatsdir.joinpath("tkn-tm")
tdmsource = formatsdir.joinpath("tkn-tm")
srcsource = formatsdir.joinpath("src", str(seglen))
# ngrdir = formatsdir.joinpath("ngr"+"-"+token+"-"+str(ngram), "")

# pseudoplain target
tknpseudodir = pseudodir.joinpath("tkn-tm")
tdmpseudodir = pseudodir.joinpath("tdm", "_".join(filter))
srcpseudodir = pseudodir.joinpath("src", str(seglen), "_".join(filter))


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


def get_pseudoplaindir(format):
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


#tkn_to_plain.main(tknsource, tknpseudodir)
#csv_to_plain.main(get_csvsource(csv), get_csvpseudo(csv), params)
preprocess_tm.main(get_pseudoplaindir(format), corpusdir, stoplist, params)
