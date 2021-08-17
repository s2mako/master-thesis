import statistics
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from fitter import Fitter
from scipy import stats

# %%
folder = Path(r"C:\Users\martin\git\master-thesis\6_evaluation\models\mallet\confidence_interval\palmetto")

model_coherences = []

for file in folder.glob("*"):
    topic_coherences = []
    for line in file.open().readlines():
        coherence = line.split("\t")[1]
        topic_coherences.append(float(coherence))
    if len(topic_coherences) == 60:
        model_coherences.append(topic_coherences)

df = pd.DataFrame(model_coherences)
df.tail()

# %% Create Means Series == Topic means
means = df.mean(axis=1)
# %% histogram
sns.set()
ax = sns.displot(data=means, kde=True, bins=12)
ax.set(xlabel="Coherence")
plt.show()
# %% histogram fitting
ax = sns.displot(means, kde=True, bins=12)
ax.set(xlabel="Coherence")
plt.show()
# %% Prepare Data for fitting
coherence = means.values
all_topics = df.values
# %% Fitting Data
f = Fitter(means)
f.fit()
f.summary()
# %% Fitting Data
f = Fitter(df)
f.fit()
f.summary()
#%% get stats with scipy first value of tuple is mean and second is standard deviation
dist = getattr(stats, "gumbel_l")
parameters = dist.fit(means)
stats.kstest(means, "gumbel_l",  parameters)

# %%

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
