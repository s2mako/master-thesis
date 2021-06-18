import re
from multiprocessing.pool import Pool

import gensim
import spacy
from spacy.lang.en import STOP_WORDS

# ====================================
# NLP Model
# ====================================
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
nlp.max_length = 10000000


# ====================================
# FUNCTIONS
# ====================================

def split(file):
    return file.read().split("<SEG>")


def ngrams(text):
    # creating bigrams. i.e. "new_york"
    bigram = gensim.models.Phrases(text, min_count=5, threshold=100)
    trigram = gensim.models.Phrases(bigram[text], threshold=100)
    text = [trigram[line] for line in text]
    return text


# default spaCy NER recognizes Persons automatically
def remove_entities(doc):
    ents_to_remove = ["PERSON"]  # "LOC" | "PERSON" ...
    print("NER...")
    # find person entities and add them to the stop words
    removed_ents = []
    for ent in doc.ents:
        if ent.label_ in ents_to_remove:
            removed_ents.append(ent.text.lower())
    print(removed_ents)
    return removed_ents


def add_stopwords(stoplistfile):
    with open(stoplistfile, "r", encoding="utf-8") as f:
        for sw in f.readlines():
            STOP_WORDS.add(sw.strip("\n"))


def create_docs(texts):
    """
    Streaming every txt file in nlp pipe
    """
    return [doc for doc in nlp.pipe(texts)]


def remove_stopwords(doc):
    """
    returns list of tokens without stop words
    """
    # Use token.lemma_ to return strings, which we'll need for Gensim.
    lemma_list = []
    for token in doc:
        lemma = token.lemma_.lower()
        if token.pos_ == "NOUN":
            if lemma in STOP_WORDS or token.is_punct or token.like_num or token.is_space:
                continue
            else:
                lemma_list.append(token.lemma_.lower())
    return lemma_list


def remove_quotes(texts):
    for text in texts:
        yield text.replace('\"', ' ').replace("`", " ")


def segmenting(doc, params):
    if params["format"] == "original" or params["format"] == "tkn":
        doc = doc[0]
        segments = [doc[i: i + params["seglen"]] for i in range(0, len(doc), params["seglen"])]
        return segments
    else:
        return doc


def clean_text(raw_text):
    # define the pattern to keep
    pat = r'[^a-zA-z0-9.,!?/:;\"\'\s]'
    return re.sub(pat, '', raw_text)


def write_to_file(doc, file, corpusdir):
    corpusdir.mkdir(exist_ok=True, parents=True)
    for i, seg in enumerate(doc):
        outfile = corpusdir.joinpath(file.stem + f"_{str(i + 1)}.txt")
        with outfile.open("w", encoding="utf-8") as f:
            linebreak = ""
            for word in seg:
                f.write(linebreak)
                f.write(clean_text(word))
                linebreak = "\n"


# ====================================
# MAIN
# ====================================

def main(sourcedir, corpusdir, stoplistfile, params):
    print("preprocess_tm")
    print(f"====from {params['format']}====")
    add_stopwords(stoplistfile)
    nlp.add_pipe(remove_stopwords)
    for file in sourcedir.glob("*.txt"):
        print(f"--{file.stem}")
        with file.open("r") as f:
            filter(f)
            texts = split(f)
            texts = remove_quotes(texts)
            docs = create_docs(texts)
            docs = segmenting(docs, params)
            write_to_file(docs, file, corpusdir)


# text = ngrams(tokens)
# tm_mallet(doc_list, False)


if __name__ == "__main__":
    pool = Pool()
    pool.map(main, corpusdir, seglen)
