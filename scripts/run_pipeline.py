import run_formats
import run_preprocess

# ==================================
# Parameters (need to be set)
# ==================================
from formatting import formats5_sel

lang = "en"
seglen = 1000
casing = "lower" # "lower"|"original"
token = "mixed" # "lemma"|"pos|"mixed"|"tm" ## expand to wordforms
pos = ["NN", "NNS", "VV", "VVD", "VVG", "VVN", "VVP", "VVZ", "JJ"]
ngram = 3
formats = ["tkn", "frq", "src", "original", "ngr"]
skip = "frq"

params = {"lang":lang, "casing":casing, "token":token, "pos":pos,
          "ngram":ngram, "seglen":seglen}

# ==================================
# Call imported scripts
# ==================================

run_formats(params, formats, skip)
run_preprocess(params, formats)
