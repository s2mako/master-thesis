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
            resolved = ""
            for i in range(count):
                text.append(tkn_info)
    return text


def save_scrambled(segments, srcfolder, params):
    seglen = params["seglen"]
    filepath = join(srcfolder, f"frq-{seglen}.txt")
    with open(filepath, "a", encoding="utf-8") as outfile:
        for seg in segments:
            outfile.write(" ".join(seg))
            outfile.write("\n")


# ====================================
# MAIN
# ====================================
def main(sourcedir, targetdir, params):
    print("running: frq_to_plain")
    for file in sourcedir.glob("*.txt"):
        with file.open("r") as f:
            print(f"--{file.stem}")
            lines = f.read().splitlines()
            tagged = create_text(lines)
            scrambled = scramble(tagged)
            segments = create_segments(scrambled, params)
            save_scrambled(segments, targetdir, params)


if __name__ == "__main__":
    main(formatsdir, sourcedir, params)
