import random
from os.path import join


def create_segments(tagged, params):
    """
    Creates segments out of tagged Text.

    """
    segments = [tagged[x: x + params["seglen"]] for x in range(0, len(tagged), params["seglen"])]
    return segments


def scramble(tagged):
    random.shuffle(tagged)  # scrambling
    return tagged


def create_text(lines):
    text = []
    for l in lines:
        if len(l.split("\t")) == 2:
            tkn_info = l.split("\t")[0]
            count = int(l.split("\t")[1])
            for i in range(count):
                text.append(tkn_info)
    return text


def save_scrambled(segments, outfile_path):
    with open(outfile_path, "a", encoding="utf-8") as outfile:
        for seg in segments:
            outfile.write(" ".join(seg))
            outfile.write("\n")


def check_outfile_path(targetdir, params):
    seglen = params["seglen"]
    filename = f"frq-{seglen}.txt"
    outfile_path = targetdir.joinpath(filename)
    if outfile_path.exists():
        print("--deleting existing file: " + filename)
        outfile_path.unlink()
    return outfile_path


def read_file(file):
    """
    Removes empty lines and returns lines
    """
    return file.read().split("\n\n")



# ====================================
# MAIN
# ====================================



def main(sourcedir, targetdir, params):
    print("running: frq2plain")
    targetdir.mkdir(exist_ok=True, parents=True)
    outfile_path = check_outfile_path(targetdir, params)  # deletes existing file
    for file in sourcedir.glob("*.txt"):
        with file.open("r") as f:
            print(f"--{file.stem}")
            lines = read_file(f)
            tagged = create_text(lines)
            scrambled = scramble(tagged)
            segments = create_segments(scrambled, params)
            save_scrambled(segments, outfile_path)


if __name__ == "__main__":
    main(sourcedir, targetdir, params)
