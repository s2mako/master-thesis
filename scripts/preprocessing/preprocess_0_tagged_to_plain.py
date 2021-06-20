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

def write_to_file(segments, corpusdir, params, filename):
    corpusdir.mkdir(exist_ok=True, parents=True)
    if "tkn" in filename:
        corpusfile = corpusdir.joinpath(f"tkn-{str(params['seglen_write'])}.txt")
    else:
        corpusfile = corpusdir.joinpath(f"original-{str(params['seglen_write'])}.txt")
    with corpusfile.open("a", encoding="utf-8") as cf:
        for seg in segments:
            cf.write(" ".join(seg))
            cf.write("\n")

def create_segments(lines, params):
    return [lines[x:x + params["seglen_write"]] for x in range(0, len(lines), params["seglen_write"])]

# ====================================
# MAIN
# ====================================

def main(taggedfile, corpusdir, params):
    print("running: tagged_to_plain")
    with open(taggedfile, "r", encoding="utf-8") as f:
        for text in f.read().split("\n"):
            if len(text.split("\t")) == 2:
                filename, content = text.split("\t")
                print("--" + filename)
                segments = create_segments(content.split(" "), params)
                write_to_file(segments, corpusdir, params,taggedfile.stem)

            # for seg in segments:
            #     lemmas = lemmatize(seg, params)
            #     lemmas = remove_stopwords(lemmas, stoplist)
            #     write_to_file(lemmas, corpusdir, params)



if __name__ == "__main__":
    main(sourcedir, corpusdir, stoplist, params)
