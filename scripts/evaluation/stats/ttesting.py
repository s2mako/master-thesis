# %%
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels as sm
from scipy import stats

#%%
def csv2df(format, seglens, tcount):
    palmettodir = Path(r"C:\Users\martin\git\master-thesis\6_evaluation\palmetto")
    model_coherences = []
    for s in seglens:
        path = palmettodir.joinpath(f"seglen-{str(s)}", f"topics-{str(tcount)}", format)
        for file in path.glob("*"):
            topic_coherences = [str(s)]
            for line in file.open().readlines():
                if len(line.split("\t")) == 3:
                    coherence = line.split("\t")[1]
                    topic_coherences.append(float(coherence))
                else:
                    print("error in " + file.absolute())
            model_coherences.append(topic_coherences)
    columns = ["seglen"] + [f"topic{x}" for x in range(tcount)]
    df = pd.DataFrame(model_coherences, columns=columns)
    df["mean"] = df.loc[:, [c for c in df.columns if "topic" in c]].mean(axis=1)
    return df
#%%
def csv2coherence(format):
    palmettodir = Path(r"C:\Users\martin\git\master-thesis\6_evaluation\palmetto")
    all_coh = []
    for file in palmettodir.rglob(f"{format}/*.csv"):
        topic_coherences = []
        for line in file.open().readlines():
            if len(line.split("\t")) == 3:
                coherence = line.split("\t")[1]
                topic_coherences.append(float(coherence))
            else:
                print("error in " + file.absolute())
        all_coh.extend(topic_coherences)
    return all_coh
#%%
def plot_kdes(format1, format2, title, labels, ci1=False, ci2=False):
    ax1 = sns.kdeplot(format1, shade=True, label=labels[0])
    ax2 = sns.kdeplot(format2, shade=True, label=labels[1])
    if ci1:
        plt.axvline(ci1[0], 0, ax1.get_ylim()[1], ls="--", color="red", linewidth=0.8)  # lower bound ci
        plt.axvline(ci1[1], 0, ax1.get_ylim()[1], ls="--", color="red", label="ci original boundaries", linewidth=0.8)
    if ci2:
        plt.axvline(ci2[0], 0, ax1.get_ylim()[1], ls="--", color="black", linewidth=0.8)  # lower bound ci
        plt.axvline(ci2[1], 0, ax1.get_ylim()[1], ls="--", color="black", label="ci tdm boundaries", linewidth=0.8)  # upper bound ci
    plt.title(title)
    plt.xlabel("Coherence")
    plt.legend()
    plt.tight_layout()
    plt.show()
# %% histogram + KDE
def histogram(data, title, ci):
    means = data["mean"]
    ax = sns.kdeplot(data=means, shade=True)
    ax.set(xlabel="Coherence", title=title)
    plt.axvline(ci[0], 0, ax.get_ylim()[1], ls="--", color="red") # lower bound ci
    plt.axvline(ci[1], 0, ax.get_ylim()[1], ls="--", color="red", label="ci boundaries") # upper bound ci
    plt.tight_layout()
    plt.legend()
    plt.show()
# %% histogram + KDE
def hist_list(data, title, ci):
    ax = sns.kdeplot(data=data, shade=True)
    ax.set(xlabel="Coherence", title=title)
    plt.axvline(ci[0], 0, ax.get_ylim()[1], ls="--", color="red") # lower bound ci
    plt.axvline(ci[1], 0, ax.get_ylim()[1], ls="--", color="red", label="ci boundaries") # upper bound ci
    plt.tight_layout()
    plt.legend()
    plt.show()
# %%
def CI(data_as_df, level_of_confidence):
    n = len(data_as_df)
    mean = data_as_df.mean()
    sem = stats.sem(data_as_df)
    z = stats.t.ppf((1 + level_of_confidence) / 2, n - 1)
    h = sem * z
    lower = mean - h
    upper = mean + h
    return (lower, upper)
#%% Full Dataframes
seglens = [500, 1000, 1500, 2000]
df_o = csv2df("original", seglens, 20)
df_o.to_csv(r"C:\Users\martin\git\master-thesis\6_evaluation\tables\coh_original.csv")

df_frq = csv2df("frq", seglens, 20)
df_o.to_csv(r"C:\Users\martin\git\master-thesis\6_evaluation\tables\tdm_original.csv")

df_tkn = csv2df("tkn", seglens, 20)
df_o.to_csv(r"C:\Users\martin\git\master-thesis\6_evaluation\tables\tkn_original.csv")

df_src = csv2df("src", seglens, 20)
df_o.to_csv(r"C:\Users\martin\git\master-thesis\6_evaluation\tables\src_original.csv")
#%% all coherences per model
coh_o = csv2coherence("original")
coh_f = csv2coherence("frq")
coh_s = csv2coherence("src")
coh_t = csv2coherence("tkn")
#%% CIs
ci_o = CI(df_o["mean"], 0.95)
ci_f = CI(df_frq["mean"], 0.95)
ci_t = CI(df_tkn["mean"], 0.95)
ci_s = CI(df_src["mean"], 0.95)
print("CI of originals: " + str(ci_o))
print("CI of tdm: " + str(ci_f))
print("CI of tkn: " + str(ci_t))
print("CI of src: " + str(ci_s))
#%% ci
import statsmodels.stats.api as sms

ci_coh_o = sms.DescrStatsW(coh_o).tconfint_mean()
#%% hist-kde-ci
histogram(df_o, "bla", ci_o)
#%% hist-kde-ci
hist_list(coh_o, "bla", ci_coh_o)
#%% plotting kdes
# original - tdm
labels = ["original", "tdm"]
plot_kdes(df_o["mean"], df_frq["mean"], "Kohärenz Original-TDM", labels, ci_o, ci_f)
#%%
# original - tkn
labels = ["original", "tkn"]
plot_kdes(df_o["mean"], df_tkn["mean"], "Kohärenz Original-TKN", labels, ci_o)
#%%
# original - sas
labels = ["original", "sas"]
plot_kdes(df_o["mean"], df_src["mean"], "Kohärenz Original-SAS", labels, ci_o)
#%%
labels = ["original", "sas"]
plot_kdes(coh_o, coh_f, "Kohärenz Original-SAS", labels, ci_coh_o)
#%%
stats.ttest_ind(df_o["mean"], df_frq["mean"])
#%%
stat, pvalue = stats.ttest_ind(df_o["mean"], df_tkn["mean"])
#%% ttest sm
sm.stats.weightstats.ttest_ind(df_o["mean"], df_tkn["mean"])

#%%
stats.ttest_ind(df_o["mean"], df_o["mean"])

#%%
ax = sns.displot(df_src["mean"], kde=True)
ax.set(xlabel="Coherence")
plt.axvline(ci_o[0], 0, ax.get_ylim()[1], ls="--", color="red") # lower bound ci
plt.axvline(ci_o[1], 0, ax.get_ylim()[1], ls="--", color="red", label="ci boundaries") # upper bound ci
plt.tight_layout()
plt.legend()
plt.show()
#%% ci
import statsmodels.stats.api as sms

sms.DescrStatsW(df_frq["mean"]).tconfint_mean()

#%%
print(df_o.loc[df_o["mean"] == 0.34802], " max=" + str(df_o["mean"].max()))
#%%
row6 = df_o.iloc[[6]]
print("max ", row6.max(axis=1))
print("min ", row6.mean(axis=1))
print("min ", row6.min(axis=1))
#%%
print(df_o.loc[df_o["mean"] == 0.34802], " max=" + str(df_o["mean"].max()))
#%%
row6 = df_frq.iloc[[4]]
print("max ", row6.max(axis=1))
print("min ", row6.mean(axis=1))
print("min ", row6.min(axis=1))
#%%
df_src["mean"].mean()
#%%
def csv2coherence():
    palmettodir = Path(r"C:\Users\martin\git\master-thesis\6_evaluation\palmetto")
    df = pd.DataFrame()
    for file in palmettodir.rglob(f".csv"):
        for line in file.open().readlines():
            topic_coherences = []
            if len(line.split("\t")) == 3:
                coherence = line.split("\t")[1]
                topic_coherences.append(float(coherence))
            else:
                print("error in " + file.absolute())
            s = pd.DataFrame(topic_coherences, columns=[file.parent.stem])
        df = df + s
    return df
#%%
coh_o = csv2coherence()
#%% boxplots


import seaborn as sns

sns.set_theme(style="whitegrid")


ax = sns.boxplot(x=tips["total_bill"])
