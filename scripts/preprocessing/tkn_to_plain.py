# =================================
# Import statements
# =================================

from library import segmenting


# ====================================
# FUNCTIONS
# ====================================

def read(file):
    with file.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f.readlines()):
            if line.islower():
                yield line


def write_to_file(tknpseudodir, file, lemmas):
    tknpseudodir.mkdir(exist_ok=True, parents=True)
    outfile = tknpseudodir.joinpath(file.name)
    with outfile.open("w", encoding="utf-8") as f:
        for s in lemmas:
            f.write(s)


# ====================================
# MAIN
# ====================================
def main(tknsource, tknpseudodir):
    print("tkn_to_plain")
    for file in tknsource.glob("*.txt"):
        print(f"--{file.stem}")
        write_to_file(tknpseudodir, file, read(file))
