"""
wine_eda_solutions.py
-----------
Solution for Exploratory Data Analysis on the Wine dataset.

Goals:
1. Load and inspect the data
2. Perform exploratory analysis
3. Produce some plots for visualisations
4. Apply PCA
5. Apply some simple ML models for classification
6. Summarise results
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
RANDOM_STATE = 42
TEST_SIZE = 0.2
N_PCA_COMPONENTS = 2
SELECTED_FEATURES = ["alcohol", "flavanoids", "malic_acid", "color_intensity", "proline"]
TARGET_COL = "target"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
def load_data() -> pd.DataFrame:
    """Load the wine dataset as a DataFrame including a 'target' column."""
    wine = load_wine()
    df = pd.DataFrame(wine.data, columns=wine.feature_names)
    df[TARGET_COL] = wine.target
    return df


def split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Separate the feature matrix X from the target vector y."""
    return df.drop(TARGET_COL, axis=1), df[TARGET_COL]


# ---------------------------------------------------------------------------
# Exploration (console output)
# ---------------------------------------------------------------------------
def print_overview(df: pd.DataFrame) -> None:
    """Print shape, head, info, summary statistics, class counts, missing values."""
    print(f"Shape: {df.shape}")
    print("\nFirst five rows:")
    print(df.head(), "\n")

    print("Info on dataset:")
    df.info()  # prints directly, returns None
    print()

    print("Summary statistics:")
    print(df.describe(), "\n")

    print("Class distribution:")
    print(df[TARGET_COL].value_counts(), "\n")

    print("Missing values:")
    print(df.isna().sum(), "\n")


def print_group_statistics(df: pd.DataFrame) -> None:
    """Print mean, standard deviation and variance of all features per class."""
    stats = {
        "Mean feature values per target": "mean",
        "Standard deviation for feature values per target": "std",
        "Variance of feature values per target": "var",
    }
    grouped = df.groupby(TARGET_COL)
    for title, agg in stats.items():
        print(f"\n{title}:")
        print(grouped.agg(agg))


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------
def _save_current_figure(path: Path) -> None:
    """Tighten layout, save the current matplotlib figure and close it."""
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    print(f"Saved {path}")


def plot_correlation_heatmap(df: pd.DataFrame, path: Path) -> None:
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(numeric_only=True), cmap="coolwarm", center=0)
    plt.title("Correlation Heatmap - Wine Dataset")
    _save_current_figure(path)


def plot_pairplot(df: pd.DataFrame, features: list[str], path: Path) -> None:
    grid = sns.pairplot(df, vars=features, hue=TARGET_COL, palette="Set1")
    grid.savefig(path)
    plt.close(grid.figure)
    print(f"Saved {path}")


def plot_boxplot(df: pd.DataFrame, feature: str, path: Path) -> None:
    plt.figure(figsize=(8, 5))
    sns.boxplot(x=TARGET_COL, y=feature, data=df)
    plt.title(f"{feature.capitalize()} Content by Wine Class")
    _save_current_figure(path)


def plot_pca_scatter(pca_df: pd.DataFrame, path: Path) -> None:
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x="PC1", y="PC2", hue=TARGET_COL, data=pca_df, palette="Set1")
    plt.title("PCA (2 Components) - Wine Dataset")
    _save_current_figure(path)


# ---------------------------------------------------------------------------
# Preprocessing
# ---------------------------------------------------------------------------
def scale_features(X: pd.DataFrame):
    """Standardise features (zero mean, unit variance). Returns (X_scaled, scaler)."""
    scaler = StandardScaler()
    return scaler.fit_transform(X), scaler


def run_pca(X_scaled, y: pd.Series, n_components: int = N_PCA_COMPONENTS):
    """Fit PCA and return (X_pca, pca_df, pca) where pca_df holds PCs + target."""
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_scaled)

    columns = [f"PC{i + 1}" for i in range(n_components)]
    pca_df = pd.DataFrame(X_pca, columns=columns)
    pca_df[TARGET_COL] = y.values
    return X_pca, pca_df, pca


def print_pca_variance(pca: PCA) -> None:
    print("\nExplained variance ratio (PCA):")
    print(pca.explained_variance_ratio_)
    print(f"Cumulative variance explained: {pca.explained_variance_ratio_.sum():.3f}\n")


# ---------------------------------------------------------------------------
# Modelling
# ---------------------------------------------------------------------------
def get_models() -> dict:
    """Return a fresh dict of unfitted classifiers (new instances on every call)."""
    return {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(max_depth=3, random_state=RANDOM_STATE),
        "Random Forest Classifier": RandomForestClassifier(
            n_estimators=100,  # number of trees in the forest
            max_depth=None,    # let the trees expand fully
            random_state=RANDOM_STATE,
        ),
    }


def evaluate_models(X, y, label: str, models: dict | None = None) -> dict:
    """
    Split the data, then fit and evaluate each model.

    Prints train/test accuracy and the confusion matrix per model and
    returns {model_name: {"train_acc": ..., "test_acc": ..., "confusion_matrix": ...}}.
    """
    models = models if models is not None else get_models()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        train_acc = model.score(X_train, y_train)
        test_acc = model.score(X_test, y_test)
        cm = confusion_matrix(y_test, y_pred)

        print(f"{name} - {label} train accuracy: {train_acc}")
        print(f"{name} - {label} test accuracy: {test_acc}")
        print(f"{name} - {label} confusion matrix:")
        print(cm, "\n")

        results[name] = {"train_acc": train_acc, "test_acc": test_acc, "confusion_matrix": cm}
    return results


# ---------------------------------------------------------------------------
# Main workflow
# ---------------------------------------------------------------------------
def main(output_dir: str | Path = ".") -> None:
    # Make sure wide DataFrames are not truncated in the console output
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load data
    print("Loading dataset...")
    df = load_data()
    print("\nData loaded successfully.")

    # 2. Exploration
    print_overview(df)
    print_group_statistics(df)

    # 3. Correlation analysis and visualisations
    plot_correlation_heatmap(df, output_dir / "heatmap.png")
    plot_pairplot(df, SELECTED_FEATURES, output_dir / "pairplot.png")
    plot_boxplot(df, "flavanoids", output_dir / "boxplot.png")

    # 4. Scaling and PCA
    X, y = split_features_target(df)
    X_scaled, _ = scale_features(X)
    X_pca, pca_df, pca = run_pca(X_scaled, y)
    plot_pca_scatter(pca_df, output_dir / "pca_scatter.png")
    print_pca_variance(pca)

    # 5. Classification on original (scaled) data
    print("--------------------------------------------")
    print("Classification models on original data.\n")
    evaluate_models(X_scaled, y, label="original")

    # 6. Classification on PCA-reduced data
    print("--------------------------------------------")
    print("Classification models on principal components.\n")
    evaluate_models(X_pca, y, label="PC")

    print(f"\nAnalysis complete. Figures saved to {output_dir.resolve()}")


if __name__ == "__main__":
    main()