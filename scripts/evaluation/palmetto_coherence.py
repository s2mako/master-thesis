import re

from gensim.utils import SaveLoad
from palmettopy.palmetto import Palmetto
from gensim.test.utils import common_corpus, common_dictionary
from zipfile import ZipFile


def extract_top_words(model):
    """
    return words without gensims markup
    """
    for i, t in enumerate(model.show_topics()):
        yield {f"topic{i + 1}": re.findall("\"(.+?)\"", t[1])}


def get_coherences(top_words, params):
    """
    establishes connection to palmetto endpoint and returns coherence score for each topic
    """
    palmetto = Palmetto()
    print("connecting to palmetto service...")
    for dict in top_words:
        for topic, words in dict.items():
            score = palmetto.get_coherence(words, params["endpoint"])  # I needed to increase timeout in source code
            yield {topic: score}


def write_to_file(scores, outfile_path):
    with outfile_path.open("w", encoding="utf-8") as of:
        for dict in scores:
            for topic, score in dict.items():
                of.write(f"{topic}\t{score}")
                of.write("\n")
                print(f"{topic}: {score}")


def create_outfile_path(in_file, scoresdir, params):
    palmettodir = scoresdir.joinpath("palmetto")
    palmettodir.mkdir(exist_ok=True)
    format = in_file.stem.split("-")[0]
    filename = f"{format}-{params['seglen']}-{params['topic_count']}.csv"
    outfile_path = palmettodir.joinpath(filename)
    if outfile_path.exists():
        print("--warning: file already exists")
    return outfile_path


def get_texts(file):
    file = file.parent.joinpath("texts.txt")
    with file.open("r") as f:
        return f.read()

def main(modelsdir, scoresdir, params):
    print("palmetto coherence")
    for file in modelsdir.glob(f"seglen-{params['seglen']}/**/model_{params['topic_count']}.bin"):
        print(f"--{file.name}")
        outfile_path = create_outfile_path(file, scoresdir, params)  # deletes existing file
        texts = get_texts(file)
        model = SaveLoad.load(str(file.resolve()))  # loads the model
        top_words = extract_top_words(model)  # used for palmetto coherence - takes a while
        scores = get_coherences(top_words, params)
        # scores = yield_score()
        write_to_file(scores, outfile_path)
