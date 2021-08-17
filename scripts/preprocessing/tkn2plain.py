# ====================================
# FUNCTIONS
# ====================================


def write_to_file(segment, outfile_path):
    with outfile_path.open("a", encoding="utf-8") as cf:
        cf.write(segment)
        cf.write("\n")


def check_outfile_path(tknfile, plaindir):
    outfile_path = plaindir.joinpath(tknfile.name)
    if outfile_path.exists():
        print("--deleting existing file: " + tknfile.name)
        outfile_path.unlink()
    return outfile_path

# ====================================
# MAIN
# ====================================


def main(segdir, plaindir):
    print("running: tkn2plain")
    plaindir.mkdir(exist_ok=True, parents=True)
    for tknfile in segdir.glob("tkn*.txt"):
        outfile_path = check_outfile_path(tknfile, plaindir)  # deletes existing file
        with open(tknfile, "r", encoding="utf-8") as f:
            for text in f.read().split("\n"):
                if len(text.split("\t")) == 2:
                    filename, content = text.split("\t")
                    print("--" + filename)
                    write_to_file(content, outfile_path)


if __name__ == "__main__":
    main(sourcedir, corpusdir, stoplist, params)
