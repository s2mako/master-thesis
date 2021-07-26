import subprocess
from pathlib import Path

index_path = Path(r"C:\Users\martin\palmetto\wikipedia_bd")

cmd = r"java -jar palmetto-0.1.0-jar-with-dependencies.jar C:\Users\martin\palmetto\wikipedia_bd C_V C:\Users\martin\Desktop\confidence_interval-500-60.csv"

proc = subprocess.Popen(cmd, cwd=r"C:\Users\martin\Desktop", shell=True, stdout=subprocess.PIPE)

output = proc.stdout.read()

print(output.decode("utf-8"))
