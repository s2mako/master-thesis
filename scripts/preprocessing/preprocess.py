import re

# ====================================
# FUNCTIONS
# ====================================

def lemmatize(seg, params):
    """
    extracts lemmas out of features
    may take a while
    """
    pos = params["pos"]
    for s in seg.split(" "):
        # if not do_lemmatize:
        #     yield clean_token(s)
        #     continue
        components = re.split("_", s)
        if len(components) != 3:
            pass
            #print("skipped: " + s)
        elif (components[1] in pos):
            # yield lemma
            yield clean_token(components[2].lower())


def clean_token(token):
    # removes non
    regex = re.compile("(?!-)[^a-zA-Z]")
    return re.sub(regex, "", token)


def remove_stopwords(lemmas, stoplist):
    """
    returns list of tokens without stop words
    """
    with stoplist.open("r") as s:
        stoplist = s.read().splitlines()
    for l in lemmas:
        if (l.lower() not in stoplist):
            yield l


def write_to_file(lemmas, outfile_path):
    with outfile_path.open("a", encoding="utf-8") as cf:
        sep = ""
        for l in lemmas:
            cf.write(sep)
            cf.write(l)
            sep = " "
        cf.write("\n")


def check_outfile_path(in_file, corpusdir, params):
    seglen = params["seglen"]
    if (in_file.stem == "tagged"):
        filename = f"original-{seglen}.txt"
    else:
        filename = f"{in_file.stem}.txt"
    outfile_path = corpusdir.joinpath(filename)
    if outfile_path.is_file():
        print("file already exists: " + filename)
        outfile_path.unlink()
    return outfile_path


# ====================================
# MAIN
# ====================================


def main(plaindir, corpusdir, stoplist, params):
    print("running: preprocess")
    corpusdir.mkdir(exist_ok=True, parents=True)
    for file in plaindir.glob("*.txt"):
        #do_lemmatize = False if file.stem.split("-")[0] == "allngrs" else True # done't lemmatize NGrams
        outfile_path = check_outfile_path(file, corpusdir, params)  # deletes existing file
        print("--" + file.stem)
        with file.open("r") as f:
            for seg in f.read().split("\n"):
                lemmas = lemmatize(seg, params)
                filtered_lemmas = remove_stopwords(lemmas, stoplist)
                write_to_file(filtered_lemmas, outfile_path)