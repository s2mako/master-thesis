import subprocess
from pathlib import Path

MALLET_PATH = r"C:\mallet"  # set to where your "bin/mallet" path is

seglen = 500
topic_count = 20
start = 0
iterations = 20
num_threads = 10  # determines threads used for parallel training

# remember to change backslashes if needed
wdir = Path("../..")

corpusdir = wdir.joinpath("5_corpus", f"seglen-{seglen}")
corpusdir.mkdir(exist_ok=True, parents=True)
mallet_dir = wdir.joinpath("6_evaluation/models/mallet", f"seglen-{seglen}")

topic_dir = mallet_dir.joinpath(f"topics-{topic_count}")


def create_input_files():
    # create MALLETs input files
    for file in corpusdir.glob("*.txt"):
        output = mallet_dir.joinpath(f"{file.stem}.mallet")
        # doesn't need to happen more than once -- usually.
        if output.is_file(): continue
        print(f"--{file.stem}")
        cmd = f"bin\\mallet import-file " \
              f"--input {file.absolute()} " \
              f"--output {output.absolute()} " \
              f"--keep-sequence"
        subprocess.call(cmd, cwd=MALLET_PATH, shell=True)
    print("import finished")


def modeling():
    # start modeling
    for file in mallet_dir.glob("*.mallet"):
        for i in range(start, iterations):
            print("iteration ", str(i))
            print(f"--{file.stem}")
            # output directory
            formatdir = topic_dir.joinpath(f"{file.stem.split('-')[0]}")
            outputdir = formatdir.joinpath(f"iteration-{i}")
            outputdir.mkdir(parents=True, exist_ok=True)
            outputdir = str(outputdir.absolute())
            # output files
            statefile = outputdir + r"\topic-state.gz"
            keysfile = outputdir + r"\keys.txt"
            compfile = outputdir + r"\composition.txt"
            diagnostics_xml = outputdir + r"\diagnostics.xml"
            # building cmd string
            cmd = f"bin\\mallet train-topics " \
                  f"--input {file.absolute()} " \
                  f"--num-topics {topic_count} " \
                  f"--output-state {statefile} " \
                  f"--output-topic-keys {keysfile} " \
                  f"--output-doc-topics {compfile} " \
                  f"--diagnostics-file {diagnostics_xml} " \
                  f"--num-threads {num_threads}"
            # call mallet
            subprocess.call(cmd, cwd=MALLET_PATH, shell=True)
    print("models trained")

#create_input_files()
modeling()