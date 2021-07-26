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
import preprocess_3_ngrams2plain
import preprocess
from scripts.parameters import params


# ==================================
# Files and folders
# ==================================

wdir = Path("../..")
resourcesdir = wdir.joinpath("resources")
stoplist = resourcesdir.joinpath("stoplist.txt")
sourcedir = wdir.joinpath("0_source")
taggedfile = wdir.joinpath("2_tagged", "tagged.txt")
formatsdir = wdir.joinpath("3_formats")
pseudodir = wdir.joinpath("4_plain", f"seglen-{params['seglen']}")
# corpusdir = wdir.joinpath("5_corpus", format, str(seglen))
corpusdir = wdir.joinpath("5_corpus", f"seglen-{params['seglen']}")

# format sources
tknsource = formatsdir.joinpath("tkn")
tknfile = tknsource.joinpath(f"tkn-{'_'.join(sorted(params['pos']))}.txt")
tdmsource = formatsdir.joinpath("tkn-tm")
srcfile = pseudodir.joinpath(f"src-{params['seglen']}.txt")
frqsource = formatsdir.joinpath("frq")
ngrdir = formatsdir.joinpath("ngr")
testdir = Path(r"/4_plain\test")

# pseudoplain target
tknpseudodir = pseudodir.joinpath("tkn-tm")
#tdmpseudodir = pseudodir.joinpath("tdm", "_".join(filter))
#srcpseudodir = pseudodir.joinpath("src", str(seglen_read), "_".join(filter))


# ==================================
# Call imported scripts
# ==================================

#preprocess_0_tagged_to_plain.main(taggedfile, pseudodir, params)
#preprocess_0_tagged_to_plain.main(tknfile, pseudodir, params)
#preprocess_2_frq_to_plain.main(frqsource, pseudodir, params)
#preprocess_3_ngrams2plain.main(ngrdir, pseudodir, params)
preprocess.main(pseudodir, corpusdir, stoplist, params)
#preprocess.main(testdir, corpusdir, stoplist, params)