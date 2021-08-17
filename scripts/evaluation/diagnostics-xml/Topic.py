from dataclasses import dataclass

@dataclass
class Topic:
    id: str
    tokens: int
    document_entropy: float
    word_length: float
    coherence: float
    uniform_dist: float
    corpus_dist: float
    eff_num_words: float
    token_doc_diff: float
    rank_1_docs: float
    allocation_ratio: float
    allocation_count: float
    exclusivity: float

