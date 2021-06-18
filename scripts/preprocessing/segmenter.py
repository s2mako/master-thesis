


def write_to_file(tknpseudodir, file, lemmas):
    tknpseudodir.mkdir(exist_ok=True, parents=True)
    outfile = tknpseudodir.joinpath(file.name)
    with outfile.open("w", encoding="utf-8") as f:
        for s in lemmas:
            f.write(s)


def segmenting(lines, seglen):
    i = 0
    for l in lines:
        if (i < seglen):
            yield segment
        else:
            yield

def main(file, params):
    print("segmenting")
    seglen = params["seglen_write"]
    with file.open("r") as f:
        segments = segmenting(f.readlines(), seglen)
        write_to_file(tknpseudodir, file, read(file))