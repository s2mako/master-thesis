# ====================================
# FUNCTIONS
# ====================================


def write_to_file(segments, outfile_path):
    with outfile_path.open("a", encoding="utf-8") as cf:
        for seg in segments:
            cf.write(" ".join(seg))
            cf.write("\n")


def create_segments(lines, params):
    return [lines[x:x + params["seglen"]] for x in range(0, len(lines), params["seglen"])]


def check_outfile_path(in_file, corpusdir, params):
    seglen = params["seglen"]
    if (in_file.stem == "tagged"):
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


def main(in_file, corpusdir, params):
    print("running: tagged_to_plain")
    corpusdir.mkdir(exist_ok=True, parents=True)
    outfile_path = check_outfile_path(in_file, corpusdir, params)  # deletes existing file
    with open(in_file, "r", encoding="utf-8") as f:
        for text in f.read().split("\n"):
            if len(text.split("\t")) == 2:
                filename, content = text.split("\t")
                print("--" + filename)
                segments = create_segments(content.split(" "), params)
                write_to_file(segments, outfile_path)




if __name__ == "__main__":
    main(sourcedir, corpusdir, stoplist, params)
