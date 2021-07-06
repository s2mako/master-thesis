# ==================================
# Parameters (need to be set)
# ==================================

lang = "en"
seglen = 500
casing = "lower" # "lower"|"original"
token = "lemma" # "lemma"|"pos|"mixed" ## expand to wordforms
pos = ["NN", "NNS", "VV", "VVD", "VVG", "VVN", "VVP", "VVZ", "JJ"]
ngram = 3
threshold = 1

params = {"lang":lang, "casing":casing, "token":token, "pos":pos,
          "ngram":ngram, "threshold": threshold, "seglen":seglen}

