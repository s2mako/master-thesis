from pathlib import Path
import statistics
import matplotlib.pyplot as plt

folder = Path(r"C:\Users\martin\git\master-thesis\6_evaluation\models\mallet\confidence_interval\palmetto")

model_coherences = []

for file in folder.glob("*"):
    topic_coherences = []
    for line in file.open().readlines():
        coherence = line.split("\t")[1]
        topic_coherences.append(float(coherence))
    model_coherences.append(topic_coherences)

means = [statistics.mean(mc) for mc in model_coherences]
print("Means: ", means)
print("Min: ", sorted(means)[1])
print("Max: ", max(means))

overall_mean = statistics.mean(means)
print("Overall Mean: ", overall_mean)

x = [i for i in range(len(means))]
plt.figure(1)
plt.plot(x, means, "bo", label="Modellkohärenz")
plt.axhline(y=overall_mean, color="red", linestyle="--", label="Durchschnitt")
plt.xlabel("Topic-Nummer")
plt.ylabel("Kohärenz")


plt.legend()



plt.savefig(r"C:\Users\martin\git\master-thesis\figures\confidence_interval.png")

plt.show()
