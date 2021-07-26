# ==================================
# Parameters (need to be set)
# ==================================
import re

from palmettopy.palmetto import Palmetto

endpoint = "cv"  #
topic_count = 60
seglen = 500


# =================================
# Import statements
# =================================

from pathlib import Path

# ==================================
# Files and folders
# ==================================

wdir = Path("../..")
modelsdir = wdir.joinpath("6_evaluation")
scoresdir = wdir.joinpath("6_evaluation")
modelsdir = wdir.joinpath("6_evaluation", "models", "mallet", f"seglen-{seglen}", f"topics-{topic_count}")


# ==================================
# Functions
# ==================================

def extract_top_words(file):
    """
    return words without gensims markup
    """
    for l in file.open().readlines():
        columns = l.split("\t")
        yield {columns[0]: columns[2].split(" ")}


def get_coherences(top_words):
    """
    establishes connection to palmetto endpoint and returns coherence score for each topic
    """
    palmetto = Palmetto()
    print("connecting to palmetto service...")
    for dict in top_words:
        for topic, words in dict.items():
            print(topic, words[:10])
            score = palmetto.get_coherence(words[:10], endpoint)  # I needed to increase timeout in source code
            yield {topic: score}


def write_to_file(scores, outfile_path):
    with outfile_path.open("w", encoding="utf-8") as of:
        for dict in scores:
            for topic, values in dict.items():
                coherence = values[0]
                words = " ".join(values[1])
                of.write(f"{topic}\t{coherence}\t{words}")
                of.write("\n")
                print(f"{topic}\t{coherence}\t{words}")


def create_outfile_path(in_file, scoresdir):
    palmettodir = scoresdir.joinpath("palmetto")
    palmettodir.mkdir(exist_ok=True)
    format = in_file.parent.name
    filename = f"{format}-{seglen}-{topic_count}.csv"
    outfile_path = palmettodir.joinpath(filename)
    if outfile_path.exists():
        print("--warning: file already exists")
    return outfile_path

# ==================================
# Main
# ==================================

def main(modelsdir, scoresdir):
    print("palmetto coherence")
    for file in modelsdir.glob(f"*/keys.txt"):
        print(f"--{file.parent}")
        outfile_path = create_outfile_path(file, scoresdir)  # deletes existing file
        top_words = extract_top_words(file)  # used for palmetto coherence - takes a while
        scores = get_coherences(top_words)
        write_to_file(scores, outfile_path)


if __name__ == "__main__":
    main(modelsdir, scoresdir)