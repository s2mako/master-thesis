#%%
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt


def read_diagnostics_xml(format):
    malletdir = Path(r"C:\Users\martin\git\master-thesis\6_evaluation\models\mallet")
    dfs = []
    for file in malletdir.rglob(f"{format}/iteration*/diagnostics.xml"):
       dfs.append(pd.read_xml(file))
    return pd.concat(dfs)
#%%
diagnostics_o = read_diagnostics_xml("original")
diagnostics_f = read_diagnostics_xml("frq")
diagnostics_s = read_diagnostics_xml("src")
diagnostics_t = read_diagnostics_xml("original")
#%% document_entropy
import seaborn as sns
sns.set_theme(style="whitegrid")
ax = sns.boxplot(data=[diagnostics_o["document_entropy"], diagnostics_f["document_entropy"],
                       diagnostics_s["document_entropy"],diagnostics_t["document_entropy"]], color="seagreen",
                 orient="h")
plt.yticks([0, 1, 2, 3], ["original", "tdm", "sas", "tkn"])
ax.set_ylabel("Format")
ax.set_xlabel("document_entropy")
plt.tight_layout()
plt.show()
plt.groupby([]).describe()
#%% corpus_dist
import seaborn as sns
sns.set_theme(style="whitegrid")
ax = sns.boxplot(data=[diagnostics_o["corpus_dist"], diagnostics_f["corpus_dist"],
                       diagnostics_s["corpus_dist"],diagnostics_t["corpus_dist"]], color="seagreen",
                 orient="h")
plt.yticks([0, 1, 2, 3], ["original", "tdm", "sas", "tkn"])
ax.set_ylabel("Format")
ax.set_xlabel("corpus_dist")
plt.tight_layout()
plt.show()
#%% uniform_dist
import seaborn as sns
sns.set_theme(style="whitegrid")
ax = sns.boxplot(data=[diagnostics_o["uniform_dist"], diagnostics_f["uniform_dist"],
                       diagnostics_s["uniform_dist"],diagnostics_t["uniform_dist"]], color="seagreen",
                 orient="h")
plt.yticks([0, 1, 2, 3], ["original", "tdm", "sas", "tkn"])
ax.set_ylabel("Format")
ax.set_xlabel("uniform_dist")
plt.tight_layout()
plt.show()
#%%
sns.kdeplot(diagnostics_o["uniform_dist"], label="original", shade=True)
sns.kdeplot(diagnostics_f["uniform_dist"], label="tdm", shade=True)
sns.kdeplot(diagnostics_s["uniform_dist"], label="sas", shade=True)
sns.kdeplot(diagnostics_t["uniform_dist"], label="tkn", shade=True)
plt.legend()
plt.show()
#%% stats
print("original")
print(diagnostics_o["document_entropy"].min())
print(diagnostics_o["document_entropy"].max())
print(diagnostics_o["document_entropy"].mean())
print(diagnostics_o["document_entropy"].quantile([0.25,0.5,0.75]))
print("tdm")
print(diagnostics_f["document_entropy"].min())
print(diagnostics_f["document_entropy"].max())
print(diagnostics_f["document_entropy"].mean())
print(diagnostics_f["document_entropy"].quantile([0.25,0.5,0.75]))
print("sas")
print(diagnostics_s["document_entropy"].min())
print(diagnostics_s["document_entropy"].max())
print(diagnostics_s["document_entropy"].mean())
print(diagnostics_s["document_entropy"].quantile([0.25,0.5,0.75]))
print("tkn")
print(diagnostics_t["document_entropy"].min())
print(diagnostics_t["document_entropy"].max())
print(diagnostics_t["document_entropy"].mean())
print(diagnostics_t["document_entropy"].quantile([0.25,0.5,0.75]))
#%% stats
print("original")
print(diagnostics_o["uniform_dist"].min())
print(diagnostics_o["uniform_dist"].max())
print(diagnostics_o["uniform_dist"].mean())
print(diagnostics_o["uniform_dist"].quantile([0.25,0.5,0.75]))
print("tdm")
print(diagnostics_f["uniform_dist"].min())
print(diagnostics_f["uniform_dist"].max())
print(diagnostics_f["uniform_dist"].mean())
print(diagnostics_f["uniform_dist"].quantile([0.25,0.5,0.75]))
print("sas")
print(diagnostics_s["uniform_dist"].min())
print(diagnostics_s["uniform_dist"].max())
print(diagnostics_s["uniform_dist"].mean())
print(diagnostics_s["uniform_dist"].quantile([0.25,0.5,0.75]))
print("tkn")
print(diagnostics_t["uniform_dist"].min())
print(diagnostics_t["uniform_dist"].max())
print(diagnostics_t["uniform_dist"].mean())
print(diagnostics_t["uniform_dist"].quantile([0.25,0.5,0.75]))
#%% stats
print("original")
print(diagnostics_o["corpus_dist"].min())
print(diagnostics_o["corpus_dist"].max())
print(diagnostics_o["corpus_dist"].mean())
print(diagnostics_o["corpus_dist"].quantile([0.25,0.5,0.75]))
print("tdm")
print(diagnostics_f["corpus_dist"].min())
print(diagnostics_f["corpus_dist"].max())
print(diagnostics_f["corpus_dist"].mean())
print(diagnostics_f["corpus_dist"].quantile([0.25,0.5,0.75]))
print("sas")
print(diagnostics_s["corpus_dist"].min())
print(diagnostics_s["corpus_dist"].max())
print(diagnostics_s["corpus_dist"].mean())
print(diagnostics_s["corpus_dist"].quantile([0.25,0.5,0.75]))
print("tkn")
print(diagnostics_t["corpus_dist"].min())
print(diagnostics_t["corpus_dist"].max())
print(diagnostics_t["corpus_dist"].mean())
print(diagnostics_t["corpus_dist"].quantile([0.25,0.5,0.75]))
#%% ttest
from scipy.stats import stats

print(stats.ttest_ind(diagnostics_o["document_entropy"], diagnostics_f["document_entropy"]))
print(stats.ttest_ind(diagnostics_o["document_entropy"], diagnostics_s["document_entropy"]))
print(stats.ttest_ind(diagnostics_o["document_entropy"], diagnostics_t["document_entropy"]))
#%% ttest
from scipy.stats import stats

print(stats.ttest_ind(diagnostics_o["uniform_dist"], diagnostics_f["uniform_dist"]))
print(stats.ttest_ind(diagnostics_o["uniform_dist"], diagnostics_s["uniform_dist"]))
print(stats.ttest_ind(diagnostics_o["uniform_dist"], diagnostics_t["uniform_dist"]))
#%% ttest
from scipy.stats import stats

print(stats.ttest_ind(diagnostics_o["corpus_dist"], diagnostics_f["corpus_dist"]))
print(stats.ttest_ind(diagnostics_o["corpus_dist"], diagnostics_s["corpus_dist"]))
print(stats.ttest_ind(diagnostics_o["corpus_dist"], diagnostics_t["corpus_dist"]))


