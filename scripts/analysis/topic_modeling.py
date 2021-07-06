# heavily inspired by https://www.machinelearningplus.com/topic-modeling-gensim-python/#14computemodelperplexityandcoherencescore
import zipfile
from pathlib import Path

import gensim
from gensim import corpora
from gensim.models import CoherenceModel, LdaModel
from gensim.utils import SaveLoad
from matplotlib import pyplot as plt
from pprint import pprint
import pickle
from gensim.test.utils import datapath
from zipfile import ZipFile
import tempfile

# ==================================
# Parameters (need to be set)
# ==================================

MALLET_PATH = r"C:\mallet\bin\mallet"  # set to where your "bin/mallet" path is

# LDA parameters
NUM_TOPICS = 1
ITERATIONS = 1
INTERVAL = 10  # topics-10 is MALLET's default
START = 20
LIMIT = NUM_TOPICS
STEP = 10
#
seglen = "500"

format = "tkn"

# ==================================
# Files and folders (don't change)
# ==================================

wdir = Path("../..")
# corpusdir = wdir.joinpath("5_corpus", format)
corpusdir = wdir.joinpath("5_corpus")
modelsdir = wdir.joinpath("6_models")


# ====================================
# FUNCTIONS
# ====================================

def compute_coherence_values(dictionary, corpus, texts):
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

    coherence_values = []
    model_list = []
    for num_topics in range(START, LIMIT, STEP):
        model = gensim.models.wrappers.LdaMallet(mallet_path=MALLET_PATH, corpus=corpus, num_topics=num_topics,
                                                 id2word=dictionary)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values


def tm_mallet(dictionary, corpus):
    print("Starting Topic Modeling (Mallet)...")
    return gensim.models.wrappers.LdaMallet(mallet_path=MALLET_PATH, corpus=corpus, num_topics=NUM_TOPICS,
                                            id2word=dictionary, iterations=ITERATIONS)


def tm_gensim(dictionary, corpus):
    print("Starting Topic Modeling (Gensim)...")
    return LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary)


def read_file(file):
    docs = []
    for l in file.readlines():
        doc = l.split(" ")
        docs.append(doc)
    return docs


def write_to_file(lda_model, texts, filename):
    format = filename.split("-")[0]
    # creating subfolders
    segdir = modelsdir.joinpath(f"seglen-{seglen}")
    segdir.mkdir(exist_ok=True)
    formatdir = segdir.joinpath(format)
    formatdir.mkdir(exist_ok=True)

    # outfile paths
    outfile_model = formatdir.joinpath(f"{format}_{NUM_TOPICS}.bin")
    outfile_texts = formatdir.joinpath(f"texts.txt")  # relevant for coherence scores

    # write files
    lda_model.save(str(outfile_model))
    with outfile_texts.open("w", encoding="utf-8") as oft:
        oft.write(str(texts))


# ====================================
# MAIN
# ====================================

def main():
    print("topic_modeling")
    for file in corpusdir.glob(f"*-{seglen}.txt"):
        with file.open("r") as f:
            print("File: " + file.stem)
            # splitting lines to docs
            texts = read_file(f)
            # build a dictionary
            dictionary = corpora.Dictionary(texts)
            # Turns each document into a bag of words.
            corpus = [dictionary.doc2bow(doc) for doc in texts]
            # creating MALLET model
            lda_model = tm_mallet(dictionary, corpus)
            coh_model = CoherenceModel(model=lda_model, texts=texts, coherence='c_v')
            coh_score = coh_model.get_coherence()
            print(coh_score)
            print(coh_model.get_coherence_per_topic())

            write_to_file(lda_model, texts, file.stem)

            # Compute Coherence Score
            # model_list, coherence_values = compute_coherence_values(dictionary=dictionary, corpus=corpus, texts=texts)
            # # Show graph
            # x = range(START, LIMIT, STEP)
            # plt.plot(x, coherence_values)
            # plt.xlabel("Num Topics")
            # plt.ylabel("Coherence score")
            # plt.legend(("coherence_values"), loc='best')
            # plt.show()
            #
            # # Print the coherence scores
            # for m, cv in zip(x, coherence_values):
            #     print("Num Topics =", m, " has Coherence Value of", round(cv, 4))

            # # Compute Coherence Score
            # print ("Computing coherence...")
            # coherence_model_ldamallet = CoherenceModel(model=mallet_lda, texts=doc_list, dictionary=dictionary, coherence='c_v')
            # #coherence_ldamallet = coherence_model_ldamallet.get_coherence()
            # print('Coherence Score: ', coherence_ldamallet)


#    pickle.dump(mallet_lda, open("mallet_lda.pkl", "wb"))

if __name__ == "__main__":
    main()
