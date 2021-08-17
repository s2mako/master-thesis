from pathlib import Path

import matplotlib

from library import get_topic_dfs
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
matplotlib.use('module://backend_interagg')

path = Path(r"C:\Users\martin\git\master-thesis\6_evaluation\models\mallet\confidence_interval\xml")
dfs = get_topic_dfs(path)

topic_count = [x for x in range(0, len(dfs))]
dfs = pd.concat(dfs, keys=topic_count)
groups = dfs.groupby(level=0)
means = groups.mean()

min = means.min()
max = means.max()

concat = pd.concat([means.min(), means.max()], axis=1).set_axis(["min", "max"], axis=1)

sns.set_style("white")
sns.set_context("paper", font_scale=2)
sns.displot(data=means, x="min", kind="hist", bins=100, aspect=1.5)
plt.show()


#%%
concat = concat.round(decimals=2)
concat["%"] = 100 - ((concat["min"] / concat["max"]) * 100)
concat = concat.round(decimals=2)



#concat = concat.pct_change(axis=0, fill_method="bfill")

latex = concat.style.to_latex(position_float="centering", hrules=True,
                              caption="Extrema für die Durchschnittswerte aller Topics. Punkte entsprichen deutschen Dezimal-Kommata.",
                              label="tab:confidence")
latex = concat.to_latex()

print(latex)




