# ==================================
# Parameters (need to be set)
# ==================================
import re
import shutil

from palmettopy.palmetto import Palmetto

endpoint = "cv"
topic_count = 20
seglen = 500
retries = 10 # if used with online service


# =================================
# Import statements
# =================================

from pathlib import Path

# ==================================
# Files and folders
# ==================================

wdir = Path("../../..")
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
            # Try again when connection fails
            for i in range(0, retries):
                try:
                    print("calculating ", topic, "...")
                    score = palmetto.get_coherence(words[:10], endpoint)
                    print(score, words[:10])
                    break
                except:
                    print("next try: ", str(i+1))
                    continue
            yield {topic: [score, words[:10]]}


def write_to_file(scores, outfile_path):
    with outfile_path.open("a", encoding="utf-8") as of:
        for dict in scores:
            for topic, values in dict.items():
                coherence = values[0]
                words = " ".join(values[1])
                of.write(f"{topic}\t{coherence}\t{words}")
                of.write("\n")
                print(f"{topic}\t{coherence}\t{words}")


def create_outfile_path(in_file, scoresdir):
    # create subfolders
    palmettodir = scoresdir.joinpath("palmetto")
    segdir = palmettodir.joinpath(f"seglen-{seglen}")
    topicdir = segdir.joinpath(f"topics-{topic_count}")
    format = in_file.parents[1].stem.split("-")[0]
    formatdir = topicdir.joinpath(format)
    formatdir.mkdir(exist_ok=True, parents=True)
    # create file
    iteration = in_file.parent.stem.split("-")[1]
    filename = f"{in_file.parent.name}.csv"
    outfile_path = formatdir.joinpath(filename)
    if outfile_path.exists():
        print("--warning: file already exists")
    return outfile_path


def move_to_done(file):
    done_folder = file.parents[1].joinpath("done")
    done_folder.mkdir(exist_ok=True, parents=True)
    folder = file.parent
    folder.rename(done_folder)


# ==================================
# Main
# ==================================

def main(modelsdir, scoresdir):
    print("palmetto coherence")
    for file in sorted(modelsdir.rglob("*/iteration*/keys.txt")):
        print(f"--{file.parent}")
        outfile_path = create_outfile_path(file, scoresdir)  # deletes existing file
        top_words = extract_top_words(file)  # used for palmetto coherence - takes a while
        scores = get_coherences(top_words)
        write_to_file(scores, outfile_path)
        #move_to_done(file)


if __name__ == "__main__":
    main(modelsdir, scoresdir)