import re

from pathlib import Path
import gensim
from gensim import corpora
from gensim.models import CoherenceModel, LdaModel
from gensim.utils import SaveLoad
from palmettopy.palmetto import Palmetto

coherence = "palmetto"  # "palmetto" | "gensim" | "all"
endpoint = "cv"

def extract_top_words(model):
    top_words = {}
    for i, t in enumerate(model.show_topics()):
        top_words.update({i+1: re.findall("\"(.+?)\"", t[1])})
    return top_words


def get_coherence(top_words):
    palmetto = Palmetto()
    try:
        for topic, words in top_words.items():
            print(f"topic {topic}: {palmetto.get_coherence(words, endpoint)}")
    except:
        print("palmetto's service not responding")


def main(scoresdir, params):
    topic_count = params[""]
    for file in scoresdir.glob("*.bin"):
        model = SaveLoad.load(file)
        top_words = extract_top_words(model)  # used for palmetto coherence - takes a while
        score = get_coherence(top_words)


main(r"C:\Users\martin\git\master-thesis\6_models\model-topics-10-frq-seglen-500.bin")