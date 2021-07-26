from pathlib import Path

from gensim.utils import SaveLoad

from gensim.models.coherencemodel import CoherenceModel

measure = "c_v"

# ==================================
# Files and folders
# ==================================

wdir = Path("../..")
modelsdir = wdir.joinpath("7_evaluation", "gensim", "models")
seglen = 500
topic_count = 1


# ====================================
# FUNCTIONS
# ====================================

def create_outfile_path(in_file, scoresdir, params):
    palmettodir = scoresdir.joinpath("palmetto")
    palmettodir.mkdir(exist_ok=True)
    format = in_file.stem.split("-")[0]
    filename = f"{format}-{params['topic_count']}-{params['seglen']}.csv"
    outfile_path = palmettodir.joinpath(filename)
    if outfile_path.exists():
        print("--warning: file already exists")
    return outfile_path


# ====================================
# MAIN
# ====================================

def main():
    print("gensim coherence")
    for file in modelsdir.glob(f"*_{seglen}-{topic_count}*.bin"):
        print(f"--{file.name}")
        model = SaveLoad.load(str(file))
        print(model.get_coherence())
        # write_to_file(scores, outfile_path)

if __name__ == "__main__":
    main()
