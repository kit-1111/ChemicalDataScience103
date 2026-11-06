import numpy as np, pandas as pd
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import Descriptors, Draw, PandasTools, rdFingerprintGenerator
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

ROOT = Path(__file__).resolve().parents[0]
DATA = ROOT/"data"

delaney = pd.read_csv(DATA / "delaney.csv")
ecoli = pd.read_csv(DATA / "ecoli_mics_sample.csv")
print(delaney.columns.tolist())
print(ecoli.columns.tolist())

delaney = delaney.rename(columns={"logS": "target"})

ecoli = ecoli.dropna(subset=["smiles", "mic"]).copy()
ecoli["target"] = pd.to_numeric(ecoli["mic"], errors="coerce")
ecoli = ecoli.dropna(subset=["target"]).reset_index(drop=True)

MOTIFS = {
    "aromatic_6_ring":   "a1aaaaa1",
    "ketone":            "[#6][CX3](=O)[#6]",
    "carboxylic_acid":   "[CX3](=O)[OX2H1]",
    "ester":             "[#6][CX3](=O)[OX2][#6]",
    "amide":             "[NX3][CX3](=[OX1])[#6]",
    "alcohol_or_phenol": "[OX2H][#6]",
    "amine_NH":          "[NX3;H2,H1;!$(NC=O)]",
    "halogen":           "[F,Cl,Br,I]",
    "nitro":             "[N+](=O)[O-]",
    "carbon_chain_ge4":  "[CH2;!R][CH2;!R][CH2;!R][CH2;!R]",
}
PATTERNS = {name: Chem.MolFromSmarts(s) for name, s in MOTIFS.items()}

def custom_fingerprint(mol):
    """1 if the motif is present, else 0 -> e.g. [0, 0, 1, 1, 1, 0, 1, 0, 1, 0]"""
    return [int(mol.HasSubstructMatch(p)) for p in PATTERNS.values()]

MORGAN = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)

def morgan_fingerprint(mol):
    return MORGAN.GetFingerprintAsNumPy(mol)

def make_descriptor_df(mols):
    descr_df = pd.DataFrame([Descriptors.CalcMolDescriptors(m) for m in mols])
    descr_df = descr_df.replace([np.inf, -np.inf], np.nan)
    descr_df = descr_df.dropna(axis=1, how="all")        
    descr_df = descr_df.loc[:, descr_df.nunique() > 1]   # constant columns carry no information
    return descr_df.fillna(descr_df.median())           

def process_dataset(df):
    df = df.copy()
    PandasTools.AddMoleculeColumnToFrame(df, smilesCol="smiles", molCol="ROMol")
    df = df[df["ROMol"].notna()].reset_index(drop=True)
    df["Image"] = df["ROMol"].apply(lambda m: Draw.MolToImage(m, size=(200, 200)))
    df["CustomFP"] = df["ROMol"].apply(custom_fingerprint)
    df["MorganFP"] = df["ROMol"].apply(morgan_fingerprint)
    descr_df = make_descriptor_df(df["ROMol"])
    return df, descr_df

def random_forest(X, y, label):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    rf.fit(X_train, y_train)

    pred_train = rf.predict(X_train)
    pred_test = rf.predict(X_test)

    print(f"- {label} -")
    print("Train R2:", r2_score(y_train, pred_train))
    print("Test  R2:", r2_score(y_test, pred_test))
    print("Test RMSE:", mean_squared_error(y_test, pred_test) ** 0.5)
    print("Test MAE:", mean_absolute_error(y_test, pred_test))
    return {"features": label,
            "train_R2": r2_score(y_train, pred_train), "test_R2": r2_score(y_test, pred_test),
            "test_RMSE": mean_squared_error(y_test, pred_test) ** 0.5,
            "test_MAE": mean_absolute_error(y_test, pred_test)}

def compare_feature_sets(df, descr_df, dataset_name):
    y = df["target"]
    results = [
        random_forest(np.vstack(df["CustomFP"]), y, "custom fingerprint"),
        random_forest(np.vstack(df["MorganFP"]), y, "Morgan fingerprint"),
        random_forest(descr_df, y, "RDKit descriptors"),     # for descriptors: X = descr_df
    ]
    return pd.DataFrame(results).assign(dataset=dataset_name)

delaney_df, delaney_descr = process_dataset(delaney)
res_delaney = compare_feature_sets(delaney_df, delaney_descr, "Delaney logS")

ecoli_df, ecoli_descr = process_dataset(ecoli)
res_ecoli = compare_feature_sets(ecoli_df, ecoli_descr, "E. coli MIC")

results = pd.concat([res_delaney, res_ecoli], ignore_index=True)
print(results.round(3).to_string(index=False))
