#For create E_coil_300 from chEMBL
import numpy as np, pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent    
DATA = ROOT / "data"

df = pd.read_csv(DATA / "E_coil.csv", sep=";", low_memory=False) #low_memory=False avoids the mixed-type warning
print(df.shape)
cols = ['Molecule ChEMBL ID','Smiles','Standard Type','Standard Relation',
        'Standard Value','Standard Units','Assay ChEMBL ID','Molecular Weight'] 
df = df[cols].copy()
df.columns = ["chembl_id","smiles","type","relation","value","units","assay_id","mw"]

print("missing smiles:", df.smiles.isna().sum()) #drop molecule without smiles
df = df.dropna(subset=["smiles"])

print(df.type.value_counts())
print(df.relation.value_counts())
print(df.units.value_counts())

df = df[df.mw.between(200, 400)] #molecular weight between 200 to 400
print(df.shape)

sample = df.sample(n=300, random_state=42) #300 random data 
sample.to_csv(DATA / "E_coil_300.csv", index=False)
print("300 samples are done.")
print("--------------------------------------------")
#********************************************************************
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
#merge and clean
act = pd.read_csv(DATA / "E_coil_300.csv")
desc = pd.read_csv(DATA / "antibio_pubchem_descr.csv")
print(act.shape, desc.shape)
act = act[act.type == "MIC"].copy() #copy of MIC data only
print("MIC:", act.shape)

act["relation"] = act.relation.str.strip("'")
act = act[act.relation == "="]          # "=" is the exact value of MIC
print("relation '=':", act.shape)

act = act[act.units.isin(["ug.mL-1", "nM"])].copy() #data in ug/ml and nM is keep 
print(act.units.value_counts())
act["mic_ugml"] = np.where(act.units == "nM", act.value * act.mw / 1e6, act.value) #convert nM to ug/ml
act = act[act.mic_ugml > 0] 
act["log_mic"] = np.log10(act.mic_ugml)
print("usable:", act.shape)
#take median per molecule for one smiles
act = act.groupby("smiles", as_index=False).agg(mic_ugml=("mic_ugml", "median"), log_mic=("log_mic", "median"))

print("duplicate smiles in pubchem:", desc.smiles.duplicated().sum()) #avoid duplicate in smiles and rows when merge
desc = desc.drop_duplicates(subset="smiles")

merged = pd.merge(act, desc, on="smiles", how="inner")  
print("merged:", merged.shape)
print("duplicates:", merged.duplicated().sum())
print(merged.isna().sum())

dfclean = merged.dropna().copy()          #clean the data
print("clean:", dfclean.shape)
dfclean.to_csv(DATA / "antibio_clean.csv", index=False)

#EDA
print(dfclean.describe())
sns.pairplot(dfclean[["log_mic", "XLogP", "TPSA", "MolecularWeight"]])
plt.savefig(DATA/ "pairplot.png", dpi=150)
plt.close("all")

sns.scatterplot(x=dfclean.XLogP, y=dfclean.log_mic)
plt.xlabel("lipophilicity (XLogP)")
plt.ylabel("log10 MIC (ug/mL, lower = better)")
plt.savefig(DATA/ "scatter_xlogp_mic.png", dpi=150)
plt.close("all")

#10 most molecules
from rdkit import Chem
from rdkit.Chem import Draw
best = dfclean.nsmallest(10, "mic_ugml")
mols = [Chem.MolFromSmiles(s) for s in best.smiles]
img = Draw.MolsToGridImage(mols, molsPerRow=5, legends=[f"{v:.3f}" for v in best.mic_ugml])
img.save(DATA / "best10.png")

#Hypothesis: higher XLogP gives a lower MIC (which is better)
thr = 3          
dfclean["high_logp"] = dfclean.XLogP > thr
high = dfclean[dfclean.high_logp].log_mic
low = dfclean[~dfclean.high_logp].log_mic
print("size:", high.size, low.size)
print("mean:", high.mean(), low.mean())
print("var:", high.var(), low.var())
#H0: both groups have the same mean
t, p = stats.ttest_ind(high, low, equal_var=False, nan_policy="omit")
print(f"t = {t:.2f}, p = {p:.6f}")

# repeat for under 10 ug L-1
dfclean["mic_ugL"] = dfclean.mic_ugml * 1000      # ug/mL -> ug/L

strong = dfclean[dfclean.mic_ugL < 10]            
print("strong (10 ug/L):", len(strong))

hi = strong[strong.XLogP > thr].log_mic
lo = strong[strong.XLogP <= thr].log_mic
print("group sizes (high, low):", hi.size, lo.size)
if hi.size < 3 or lo.size < 3:
    print("too few molecules for a reliable t-test")
else:
    t, p = stats.ttest_ind(hi, lo, equal_var=False, nan_policy="omit")
    print(f"t = {t:.2f}, p = {p:.6f}")
