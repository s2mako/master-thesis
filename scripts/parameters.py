# ==================================
# Parameters (need to be set)
# ==================================

lang = "en"
seglen = 500
casing = "lower" # "lower"|"original"
token = "lemma"
pos = ["NN", "NNS", "VV", "VVD", "VVG", "VVN", "VVP", "VVZ", "JJ"]
#pos = "all"
token = "mixed" # "lemma"|"pos|"mixed" ## expand to wordforms
ngram = 3
threshold = 3

params = {"lang":lang, "casing":casing, "token":token, "pos":pos,
          "ngram":ngram, "threshold": threshold, "seglen":seglen}

