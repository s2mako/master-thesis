from pathlib import Path

def read_tagged_as_docs(taggedfolder, seglen=None):
    taggedfolder = Path(taggedfolder)
    for file in taggedfolder.glob("*.txt"):
        print(file.stem)
        yield "<DOC>\n"
        with file.open("r") as f:
            if seglen:
                i = 1
                for line in f.read().split("\n"):
                    i += 1
                    yield line
                    yield "\n"
                    if (i == seglen):
                        yield "<SEG>\n"
                        i = 1
            else:
                yield f.read()
                yield "\n"

def save_to_file(taggedfolder, seglen):
    filepath = taggedfolder.joinpath("..", f"tagged-{seglen}.txt")
    with open(filepath, "w", encoding="utf-8") as outfile:
        for t in read_tagged_as_docs(taggedfolder, seglen):
            outfile.write(t)

seglen = 100
taggedfolder = Path(r"C:\Users\martin\git\master-thesis\2_tagged\old")

#for seglen in range(seglen, 1000, 50):
save_to_file(taggedfolder, None)


