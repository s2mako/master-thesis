
# ====================================
# FUNCTIONS
# ====================================
import random


def check_outfile_path(in_file, corpusdir, params):
    seglen = params["seglen"]
    format = in_file.stem.split("-")[0]
    filename = f"{format}-{str(params['ngram'])}-{seglen}.txt"
    outfile_path = corpusdir.joinpath(filename)
    if outfile_path.exists():
        print("--deleting existing file: " + filename)
        outfile_path.unlink()
    return outfile_path


def create_segments(scrambled, params):
    """
    Creates segments out of tagged Text.

    """
    seglen = round(params["seglen"] / params["ngram"])
    segments = [scrambled[x: x + seglen] for x in range(0, len(scrambled), params["seglen"])]
    return segments


def save_scrambled(segments, outfile_path):
    with open(outfile_path, "a", encoding="utf-8") as outfile:
        for seg in segments:
            outfile.write(" ".join(seg))
            outfile.write("\n")


def scramble(tagged):
    random.shuffle(tagged)  # scrambling
    return tagged


def read_file(file):
    """
    Removes empty lines and returns lines
    """
    return file.read().replace("\n\n", "\n").split("\n")

def create_text(lines):
    text = []
    for l in lines:
        if len(l.split("\t")) == 2:
            tkn_info = l.split("\t")[0]
            count = int(l.split("\t")[1])
            for i in range(count):
                text.append(tkn_info)
    return text


# ====================================
# MAIN
# ====================================


def main(ngrdir, corpusdir, params):
    print("running: ngr_to_plain")
    ngrfile = ngrdir.joinpath(f"allngrs-{params['ngram']}.tsv")
    outfile_path = check_outfile_path(ngrfile, corpusdir, params)  # deletes existing file
    with ngrfile.open("r") as f:
        print(f"--{ngrfile.stem}")
        lines = read_file(f)
        text = create_text(lines)
        scrambled = scramble(text)
        segments = create_segments(scrambled, params)
        save_scrambled(segments, outfile_path)
