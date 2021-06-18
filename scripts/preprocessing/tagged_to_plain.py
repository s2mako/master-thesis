import re

# ====================================
# FUNCTIONS
# ====================================

def lemmatize(seg, params):
    pos = params["pos"]
    for s in seg:
        components = re.split("\t", s)
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

def write_to_file(lemmas, corpusdir, params):
    corpusdir.mkdir(exist_ok=True, parents=True)
    corpusfile = corpusdir.joinpath(f"original-{str(params['seglen_write'])}-test.txt")
    with corpusfile.open("a", encoding="utf-8") as cf:
        space = ""
        for l in lemmas:
            cf.write(space)
            space = " "
            cf.write(l)
        # newline as doc delimiter
        cf.write("\n")

def create_segments(lines, params):
    return [lines[x:x + params["seglen_write"]] for x in range(0, len(lines), params["seglen_write"])]

# ====================================
# MAIN
# ====================================


def main(sourcedir, corpusdir, stoplist, params):
    print("running: tagged_to_plain")
    i = 0
    for file in sourcedir.glob("*.txt"):
        print(f"--{file.stem}")
        with file.open("r") as f:
            lines = f.read().split("\n")
            segments = create_segments(lines, params)
            for seg in segments:
                lemmas = remove_stopwords(lemmatize(seg, params), stoplist)
                write_to_file(lemmas, corpusdir, params)
        i += 1
    print(f"processed {i} files")





if __name__ == "__main__":
    main(sourcedir, corpusdir, stoplist, params)
