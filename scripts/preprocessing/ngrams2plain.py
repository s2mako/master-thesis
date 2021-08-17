import random


# ====================================
# FUNCTIONS
# ====================================


def check_outfile_path(in_file, plaindir, params):
    plaindir.mkdir(exist_ok=True, parents=True)
    format = in_file.stem.split("-")[0]
    filename = f"{format}-{str(params['ngram'])}_thr-{str(params['threshold'])}.txt"
    outfile_path = plaindir.joinpath(filename)
    if outfile_path.exists():
        print("--deleting existing file: " + filename)
        outfile_path.unlink()
    return outfile_path


def save_scrambled(segment, outfile_path):
    with open(outfile_path, "a", encoding="utf-8") as outfile:
        for feature in segment:
            outfile.write(feature)
        outfile.write("\n")


def scramble(tagged):
    random.shuffle(tagged)  # scrambling
    return tagged


def cleaning(content):
    content = content.replace("\t0\n\n", "")
    content = content.replace("\n\n", "\n")
    content = content.split("<seg>")
    return content


def read_file(file):
    content = file.read()
    content = cleaning(content)  # hacky cleaning
    segments = []
    for segment in content:
        segment = segment.split("\n")
        if len(segment) > 0:
            segments.append(segment)
    return segments


def create_text(seg):
    text = []
    for line in seg:
        if len(line.split("\t")) == 2:
            tkn_info = line.split("\t")[0]
            count = int(line.split("\t")[1])
            for i in range(count):
                text.append(tkn_info)
    return text


# ====================================
# MAIN
# ====================================


def main(segdir, plaindir, params):
    print("running: ngrams2plain")
    ngrfile = segdir.joinpath(f"allngrs-{params['ngram']}_thr-{params['threshold']}.tsv")
    outfile_path = check_outfile_path(ngrfile, plaindir, params)  # deletes existing file
    with ngrfile.open("r") as f:
        print(f"--{ngrfile.stem}")
        for seg in read_file(f):
            text = create_text(seg)
            scrambled = scramble(text)
            save_scrambled(scrambled, outfile_path)
