from gensim.utils import SaveLoad

from gensim.models.coherencemodel import CoherenceModel


def get_coherence(model):
    cm = CoherenceModel(model=model, coherence='cv')
    print(cm.get_coherence())


def create_outfile_path(in_file, scoresdir, params):
    palmettodir = scoresdir.joinpath("palmetto")
    palmettodir.mkdir(exist_ok=True)
    format = in_file.stem.split("-")[0]
    filename = f"{format}-{params['topic_count']}-{params['seglen']}.csv"
    outfile_path = palmettodir.joinpath(filename)
    if outfile_path.exists():
        print("--warning: file already exists")
    return outfile_path


def main(modelsdir, scoresdir, params):
    print("gensim coherence")
    for file in modelsdir.glob(f"*-{params['topic_count']}-{params['seglen']}.bin"):
        print(f"--{file.name}")
        #outfile_path = create_outfile_path(file, scoresdir, params)  # deletes existing file
        model = SaveLoad.load(str(file.resolve()))
        scores = get_coherence(model)
        # scores = yield_score()
        #write_to_file(scores, outfile_path)