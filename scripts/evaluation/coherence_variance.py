# gensim
from pathlib import Path

import gensim
from gensim import corpora
from gensim.models import LdaMulticore
from gensim.models.coherencemodel import CoherenceModel


def main():
    path = Path(r"C:\Users\martin\git\master-thesis\6_evaluation\coherence-variance")
    coh_models = {}
    for file in path.glob("coh*.bin"):
        print(file.stem)
        coh_models.update({file.stem: CoherenceModel.load(str(file)).get_coherence()})

    for name, coherence in coh_models.items():
        print(name, " ", coherence)

if __name__ == "__main__":
    main()
