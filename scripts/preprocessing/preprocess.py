import re

# ====================================
# FUNCTIONS
# ====================================

def lemmatize(seg, params):
    pos = params["pos"]
    for s in seg.split(" "):
        components = re.split("_", s)
        if len(components) != 3:
            print("skipped: " + s)
        elif (components[1] in pos):
            # yield lemma
            yield components[2].lower()


def remove_stopwords(lemmas, stoplist):
    """
    returns list of tokens without stop words
    """
    with stoplist.open("r") as s:
        stoplist = s.read().splitlines()
    for l in lemmas:
        if (l.lower() not in stoplist):
            yield l


def write_to_file(lemmas, corpusdir, filename):
    corpusdir.mkdir(exist_ok=True, parents=True)
    corpusfile = corpusdir.joinpath(filename + ".txt")
    with corpusfile.open("a", encoding="utf-8") as cf:
        sep = ""
        for l in lemmas:
            cf.write(sep)
            cf.write(l)
            sep = " "
        cf.write("\n")


# ====================================
# MAIN
# ====================================

def main(plaindir, corpusdir, stoplist, params):
    print("running: preprocess")
    for file in plaindir.glob("*.txt"):
        print("--" + file.stem)
        with file.open("r") as f:
            for seg in f.read().split("\n"):
                lemmas = lemmatize(seg, params)
                filtered_lemmas = remove_stopwords(lemmas, stoplist)
                write_to_file(filtered_lemmas, corpusdir, file.stem)
