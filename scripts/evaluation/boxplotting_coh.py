#%%
from pathlib import Path

import pandas
import pandas as pd
from matplotlib import pyplot as plt

#%%
def csv2coherence(format):
    palmettodir = Path(r"C:\Users\martin\git\master-thesis\6_evaluation\palmetto")
    rows = []
    for file in palmettodir.rglob(f"{format}/*.csv"):
        seglen = file.parents[2].stem.split("-")[1]
        for line in file.open().readlines():
            if len(line.split("\t")) == 3:
                coherence = line.split("\t")[1]
                rows.append([format, int(seglen), float(coherence)])
            else:
                print("error in " + file.absolute())
    df = pd.DataFrame(rows, columns=["format", "seglen", "coherence"])
    return df
#%%
coh_o = csv2coherence("original")
coh_f = csv2coherence("frq")
coh_s = csv2coherence("src")
coh_t = csv2coherence("tkn")

mega_df = pd.concat([coh_o, coh_f, coh_s, coh_t])
mega_df.head(5)

#%% boxplots
import seaborn as sns
sns.set_theme(style="whitegrid")
ax = sns.boxplot(orient="h", palette="pastel", y=mega_df['format'],
                 x=mega_df['coherence'], hue=mega_df['seglen'])
ax.set_ylabel("Format")
ax.set_xlabel("Kohärenz")
plt.yticks([0,1,2,3], ["original","tdm", "sas","tkn"])
plt.tight_layout()
plt.show()
#%% barplots
import seaborn as sns
sns.set_theme(style="whitegrid")
ax = sns.barplot(data=[{coh_o}, coh_s, coh_t, coh_f])
plt.show()
#%%
sns.histplot(df["original"], kde=True)
sns.histplot(df["tdm"], kde=True, color="red")
plt.show()
#%%
sns.kdeplot(df["original"], shade=True)
sns.kdeplot(df["tdm"], shade=True)
plt.show()
#%%
from scipy import stats
print(stats.ttest_ind(df["original"], df["tdm"]))
print(stats.ttest_ind(df["original"], df["sas"]))
print(stats.ttest_ind(df["original"], df["tkn"]))
