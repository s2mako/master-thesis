"""
Pipeline to create a corpus for topic modeling from an plain full-text corpus or pseudo plain
text constructed from derived format.

"""

# =================================
# Import statements
# =================================

from pathlib import Path
import seg2plain
import frq2plain
import ngrams2plain
import tkn2plain
import preprocess
from scripts.parameters import params


# ==================================
# Files and folders
# ==================================

wdir = Path("../..")
resourcesdir = wdir.joinpath("resources")
stoplist = resourcesdir.joinpath("stoplist.txt")
sourcedir = wdir.joinpath("0_source")
taggedfile = wdir.joinpath("1_tagged", "tagged.txt")
segdir = wdir.joinpath(f"2_segmented")
segfile = segdir.joinpath(f"segmented-{params['seglen']}.txt")
formatsdir = wdir.joinpath("3_formats", f"seglen-{params['seglen']}")
plaindir = wdir.joinpath("4_plain", f"seglen-{params['seglen']}")
# corpusdir = wdir.joinpath("5_corpus", format, str(seglen))
corpusdir = wdir.joinpath("5_corpus", f"seglen-{params['seglen']}")

# format sources
#tknsource = formatsdir.joinpath("tkn")
tknfile = segdir.joinpath(f"tkn-.txt")
tdmsource = formatsdir.joinpath("tkn-tm")
srcfile = plaindir.joinpath(f"src-{params['seglen']}.txt")
frqinput = wdir.joinpath("3_formats", "frq")
frqoutput = wdir.joinpath("4_plain", "frq")
ngrdir = formatsdir.joinpath("ngr")
testdir = Path(r"/4_plain\test")

# pseudoplain target
tknpseudodir = plaindir.joinpath("tkn-tm")
#tdmpseudodir = pseudodir.joinpath("tdm", "_".join(filter))
#srcpseudodir = pseudodir.joinpath("src", str(seglen_read), "_".join(filter))


# ==================================
# Call imported scripts
# ==================================

#seg2plain.main(segfile, plaindir)
#tkn2plain.main(formatsdir, plaindir)
#frq2plain.main(frqinput, plaindir, params)
ngrams2plain.main(formatsdir, plaindir, params)
#preprocess.main(plaindir, corpusdir, stoplist, params)
#preprocess.main(testdir, corpusdir, stoplist, params)