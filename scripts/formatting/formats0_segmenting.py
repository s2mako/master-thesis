from pathlib import Path


def create_segments(tagged, params):
    """
    Creates segments out of tagged Text.

    """
    tagged = tagged.split(" ")
    segments = [tagged[x:x+params["seglen"]] for x in range(0, len(tagged), params["seglen"])]
    return segments


def read_file(taggedfile):
    return taggedfile.open().readlines()


def write_to_file(outfile_path, doc_name, segments, segmentsfolder):
    segmentsfolder = Path(segmentsfolder)
    segmentsfolder.mkdir(exist_ok=True, parents=True)
    with outfile_path.open("a", encoding="utf-8") as f:
        newline = ""
        for seg in segments:
            f.write(newline)
            f.write(doc_name)
            f.write("\t")
            f.write(" ".join(seg))
            newline = "\n"


def check_outfile_path(outdir, params):
    seglen = params["seglen"]
    filename = f"segmented-{seglen}.txt"
    outfile_path = Path(outdir).joinpath(filename)
    if outfile_path.is_file():
        print("file already exists: " + filename)
        outfile_path.unlink()
    return outfile_path

# ====================================
# MAIN
# ====================================

def main(taggedfile, segmentsfolder, params):
    taggedfile = Path(taggedfile)
    docs = read_file(taggedfile)
    outfile_path = check_outfile_path(segmentsfolder, params) # delete if exists already
    for doc in docs:
        doc_name, content = doc.split("\t")
        print("--" + doc_name)
        segments = create_segments(content, params)
        write_to_file(outfile_path, doc_name, segments, segmentsfolder)

if __name__ == "__main__":
    main(taggedfile, segmentsfolder, params)