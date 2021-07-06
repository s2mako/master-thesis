
# ==================================
# Parameters (need to be set)
# ==================================

endpoint = "cv"  #
topic_count = 1
seglen = 500

params = {"endpoint": endpoint, "topic_count": topic_count, "seglen": seglen}

# =================================
# Import statements
# =================================

from pathlib import Path
import gensim_coherence
import palmetto_coherence

# ==================================
# Files and folders
# ==================================

wdir = Path("../..")
modelsdir = wdir.joinpath("6_models")
scoresdir = wdir.joinpath("7_scores")

# ==================================
# Call imported scripts
# ==================================

palmetto_coherence.main(modelsdir, scoresdir, params)
#gensim_coherence.main(modelsdir, scoresdir, params)
