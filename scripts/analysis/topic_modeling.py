# Imports
import time
from pathlib import Path

# gensim
import gensim
from gensim import corpora
from gensim.models import LdaMulticore
from gensim.models.coherencemodel import CoherenceModel

MALLET_PATH = r"C:\mallet\bin\mallet"  # set to where your "bin/mallet" path is


# TM Parameters
type = "gensim"  # "mallet" | "gensim" | "all"
seglen = 500
topic_count = 50
measure = "c_v"
# coherence graph
create_coherence_graph = True

#%% md

#Files and Folders

#%%

wdir = Path("../..")

coherence_models_dir = wdir.joinpath("7_evaluation", "gensim", "models")
corpusdir = wdir.joinpath("5_corpus")
evaluationdir = wdir.joinpath("6_evaluation")
coherencedir = wdir.joinpath("7_evaluation", "gensim")

# Functions
## Topic Modeling

def create_tm(dictionary, corpus, type, topic_count):
    if type == "mallet":
        print("--Starting Topic Modeling (Mallet)...")
        return gensim.models.wrappers.LdaMallet(mallet_path=MALLET_PATH, corpus=corpus, num_topics=topic_count,
                                                id2word=dictionary)
    elif type == "gensim":
        print("--Starting Topic Modeling (Gensim)...")
        return LdaMulticore(corpus, num_topics=topic_count, id2word=dictionary, workers=12)


def read_file(file):
    docs = []
    for l in file.open("r", "utf-8").readlines():
        doc = l.split(" ")
        docs.append(doc)
    return docs


def save_tm_model(lda_model, filename, type, topic_count):
    format = filename.split("-")[0]
    # creating subfolders
    modelsdir = evaluationdir.joinpath("models", type)
    segdir = modelsdir.joinpath(f"seglen-{seglen}")
    topicsdir = segdir.joinpath(f"topics-{topic_count}")
    topicsdir.mkdir(exist_ok=True, parents=True)
    formatdir = topicsdir.joinpath(format)
    formatdir.mkdir(exist_ok=True, parents=True)
    # outfile path
    outfile_model = formatdir.joinpath(f"tm.bin")
    # write file
    lda_model.save(str(outfile_model))
    print(f"--saved TM to: {outfile_model}")


def save_coherence_model(lda_model, texts, filename, type, measure):
    coh_model = CoherenceModel(model=lda_model, texts=texts, coherence=measure)
    format = filename.split("-")[0]
    # creating subfolders
    modelsdir = evaluationdir.joinpath("models", type)
    segdir = modelsdir.joinpath(f"seglen-{seglen}")
    topicsdir = segdir.joinpath(f"topics-{topic_count}")
    formatdir = topicsdir.joinpath(format)
    formatdir.mkdir(exist_ok=True, parents=True)
    # outfile path
    outfile_model = formatdir.joinpath(f"coh-{measure.replace('_', '')}.bin")
    coh_model.save(str(outfile_model))
    print(f"--saved Coherence to: {outfile_model}")

# Start TM
corpus_files = corpusdir.glob(f"*-{seglen}.txt")



def main():
    time_start = time.time()
    for file in corpus_files:
        print("File: " + file.stem)
        # splitting lines to docs
        documents = read_file(file)
        # build a dictionary
        print("--Creating Dictionary")
        dictionary = corpora.Dictionary(documents)
        # Turns each document into a bag of words.
        print("--Creating Doc2Bow")
        corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in documents]
        lda_model = create_tm(dictionary, corpus, type, topic_count)
        save_tm_model(lda_model, file.stem, type, topic_count)
        # create coherence model
        save_coherence_model(lda_model, documents, file.stem, type, measure)
    print("Finished Modeling")
    end = time.time()
    print(f"Elapsed timed: {end - time_start}")


if __name__ == "__main__":
    main()


