import pandas as pd

df = pd.read_csv(r"C:\Users\martin\git\master-thesis\6_evaluation\palmetto\original-500-60.csv", sep="\t")
print(df.mean(axis=1))

#print(df.iloc[:, : 7].to_latex(index=False))
