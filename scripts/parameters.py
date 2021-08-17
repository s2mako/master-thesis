# ==================================
# Parameters (need to be set)
# ==================================

seglen = 1000
casing = "lower" # "lower"|"original"
token = "lemma"
pos = ["NN", "NNS", "VV", "VVD", "VVG", "VVN", "VVP", "VVZ", "JJ"]
#pos = "all"
token = "mixed" # "lemma"|"pos|"mixed" ## expand to wordforms
ngram = 3
threshold = 0

params = {"casing":casing, "token":token, "pos":pos,
          "ngram":ngram, "threshold": threshold, "seglen":seglen}

