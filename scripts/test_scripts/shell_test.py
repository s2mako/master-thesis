import subprocess
from pathlib import Path

mallet_dir = "c:\mallet"


def main(corpusdir):
    # p1 = subprocess.Popen(f"bin\mallet", cwd=mallet_dir, shell=True)

    for file in corpusdir.glob("original/*"):
        full_path = file.resolve()
        print(full_path)

        input = file.resolve()
        output = str(input)
        output = output.replace("5_corpus", "6_results")
        Path(output).mkdir(exist_ok=True, parents=True)
        output = output + r"\mallet.mallet"

        subprocess.Popen(
            f"bin\mallet import-dir --input {input} --output {output}",
            cwd=mallet_dir)
