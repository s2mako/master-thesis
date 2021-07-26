# start modeling
import subprocess
from pathlib import Path

MALLET_PATH = r"C:\mallet"  # set to where your "bin/mallet" path is

seglen = 500
topic_count = 60
num_threads = 12

for i in range(0,99):
    file = Path(r"C:\Users\martin\git\master-thesis\6_evaluation\models\mallet\seglen-500\original-500.mallet")
    print(f"--{file.stem}")
    # output directory
    outputdir = Path(r"C:\Users\martin\git\master-thesis\6_evaluation\models\mallet\confidence_interval")
    # output files
    keysfile = str(outputdir) + r"\keys_" + str(i) + ".txt"
    diagnostics_xml = str(outputdir) + r"\diagnostics_" + str(i) + ".xml"
    # building cmd string
    cmd = f"bin\\mallet train-topics " \
          f"--input {file.absolute()} " \
          f"--num-topics {topic_count} " \
          f"--output-topic-keys {keysfile} " \
          f"--diagnostics-file {diagnostics_xml} " \
          f"--num-threads {num_threads}"
    # call mallet
    subprocess.call(cmd, cwd=MALLET_PATH, shell=True)
    print("models trained")

