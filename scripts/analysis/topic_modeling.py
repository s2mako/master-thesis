import re
from pathlib import Path

import gensim
from gensim import corpora
from gensim.models import CoherenceModel
from matplotlib import pyplot as plt

# ==================================
# Parameters (need to be set)
# ==================================

mallet_path = r"C:\mallet\bin\mallet"
# LDA parameters
num_topics = 70
iterations = 1000
interval = 10  # 10 is MALLET's default
start = 1
limit = 200
step = 10

format = "tkn"

seglen = 50  # segment length

params = {"seglen": seglen, "mallet_path": mallet_path, "num_topics": num_topics,
          "iterations": iterations, "interval": interval, "start": start, "limit": limit, "step": step,
          "format": format}

# ==================================
# Files and folders (don't change)
# ==================================

wdir = Path("../..")
corpusdir = wdir.joinpath("5_corpus", format)


# ====================================
# FUNCTIONS
# ====================================

def compute_coherence_values(dictionary, corpus, texts, params):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    # paramters
    mallet_path = params["mallet_path"]
    start = params["start"]
    limit = params["limit"]
    step = params["step"]

    coherence_values = []
    for num_topics in range(start, limit, step):
        model = gensim.models.wrappers.LdaMallet(mallet_path=mallet_path, corpus=corpus, num_topics=num_topics,
                                                 id2word=dictionary)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    x = range(start, limit, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    plt.show()

    return model, coherence_values


def tm_mallet(doc_list):
    print("Creating BOW-Corpus...")
    # Creates, which is a mapping of word IDs to words.
    words = corpora.Dictionary(doc_list)
    # Turns each document into a bag of words.
    corpus = [words.doc2bow(doc) for doc in doc_list]

    print("Starting Topic Modeling (Mallet)...")

    # creating LDA model using mallet
    mallet_lda = gensim.models.wrappers.LdaMallet(mallet_path=mallet_path, corpus=corpus, num_topics=num_topics,
                                                  id2word=words, iterations=iterations,
                                                  optimize_interval=interval)

    return mallet_lda


def select_folder(dir, params):
    if int(params["seglen"]):
        return dir.glob(f"{str(params['seglen'])}/*.txt")
    else:
        return dir.glob(f"*.txt")


def read_corpus(dir):
    doc_list = []
    for file in dir:
        with file.open("r", encoding="utf-8") as f:
            doc = []
            for word in f.readlines():
               doc.append(word.rstrip("\n"))
        doc_list.append(doc)
    return doc_list

# ====================================
# MAIN
# ====================================

def main(corpusdir, params):
    print("topic_modeling")
    print()
    corpusdir = select_folder(corpusdir, params)
    # splitting segmented text files to docs
    doc_list = read_corpus(corpusdir)
    dictionary = corpora.Dictionary(doc_list)
    # Turns each document into a bag of words.
    corpus = [dictionary.doc2bow(doc) for doc in doc_list]

    model, coherence_values = compute_coherence_values(params=params, dictionary=dictionary, corpus=corpus,
                                                        texts=doc_list)  # Show graph

   # tm_mallet(doc_list)
    # pprint(mallet_lda.show_topics(formatted=False))


if __name__ == "__main__":
    main(corpusdir, params)
