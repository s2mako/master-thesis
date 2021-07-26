# ==================================
# Parameters (need to be set)
# ==================================
import re
import shutil

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
            if int(topic) > 19:
                # Try again when connection fails
                for i in range(0, 10):
                    try:
                        print("calculating ", topic, "...")
                        score = palmetto.get_coherence(words[:10], endpoint)
                        print(score, words[:10])
                        break
                    except:
                        print("next try: ", str(i+1))
                        continue
                yield {topic: [score, words[:10]]}
            else:
                continue


def write_to_file(scores, outfile_path):
    for dict in scores:
        with outfile_path.open("a", encoding="utf-8") as of:
            for topic, values in dict.items():
                coherence = values[0]
                words = " ".join(values[1])
                of.write(f"{topic}\t{coherence}\t{words}")
                of.write("\n")
                print(f"{topic}\t{coherence}\t{words}")


def create_outfile_path(in_file, scoresdir, i):
    palmettodir = scoresdir.joinpath("palmetto")
    palmettodir.mkdir(exist_ok=True)
    format = in_file.parent.name
    filename = f"{format}-{seglen}-{topic_count}_{i}.csv"
    outfile_path = palmettodir.joinpath(filename)
    return outfile_path

# ==================================
# Main
# ==================================

def move_to_done(file):
    to_folder = Path(r"C:\Users\martin\git\master-thesis\6_evaluation\models\mallet\confidence_interval\done")
    shutil.copy(file, to_folder)
    file.unlink()


def main(modelsdir, scoresdir):
    print("palmetto coherence")
    for file in modelsdir.glob(f"keys_*.txt"):
        i = file.stem.split("_")[1]
        print(f"--{file.parent}")
        outfile_path = create_outfile_path(file, scoresdir, i)  # deletes existing file
        top_words = extract_top_words(file)  # used for palmetto coherence - takes a while
        scores = get_coherences(top_words)
        write_to_file(scores, outfile_path)
        move_to_done(file)


input = Path(r"C:\Users\martin\git\master-thesis\6_evaluation\models\mallet\confidence_interval")
main(input, input)