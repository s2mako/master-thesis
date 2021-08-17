# ====================================
# FUNCTIONS
# ====================================


def write_to_file(segment, outfile_path):
    with outfile_path.open("a", encoding="utf-8") as cf:
        cf.write(" ".join(segment))
        cf.write("\n")

def check_outfile_path(in_file, corpusdir, params):
    seglen = params["seglen"]
    if ("segmented" in in_file.stem):
        filename = f"original-{seglen}.txt"
    else:
        format = in_file.stem.split("-")[0]
        filename = f"{format}-{seglen}.txt"
    outfile_path = corpusdir.joinpath(filename)
    if outfile_path.exists():
        print("--deleting existing file: " + filename)
        outfile_path.unlink()
    return outfile_path

# ====================================
# MAIN
# ====================================


def main(in_file, plaindir, params):
    print("running: seg2plain")
    plaindir.mkdir(exist_ok=True, parents=True)
    outfile_path = check_outfile_path(in_file, plaindir, params)  # deletes existing file
    with open(in_file, "r", encoding="utf-8") as f:
        for text in f.read().split("\n"):
            if len(text.split("\t")) == 2:
                filename, content = text.split("\t")
                print("--" + filename)
                write_to_file(content, outfile_path)


if __name__ == "__main__":
    main(sourcedir, corpusdir, stoplist, params)
