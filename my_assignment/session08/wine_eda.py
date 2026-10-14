"""
wine_eda.py
-----------
Homework: Exploratory Data Analysis on the Wine dataset.

Goals:
1. Load and inspect the data
2. Perform exploratory analysis
3. Produce some plots for visualisations
4. Apply PCA
5. Apply some simple ML models for classification
6. Summarise results
"""

# Imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# Main analysis function
def main():
    # --- 1. Load data ---
    print("Loading dataset...")
    wine = load_wine()
    df = pd.DataFrame(wine.data, columns = wine.feature_names)
    # add a 'target' column
    df["target"] = wine.target

    # print basic info (shape, first rows, summary statistics)
    pd.set_option("display.max_columns", None) #For display all column instead of "..."
    print("Shape:", df.shape)
    print("Column names:", list(df.columns))
    print(df.head(10)) #fisrt 10
    print(df.describe()) #stat

    # --- 2. Basic exploration ---
    # print class distribution and check for missing values as well as duplicates
    print("................")
    print("Number of wine in each class:")
    value_each_class = df["target"].value_counts()
    print(value_each_class)
    print("Number of missing data:")
    missing_vaule = df.isnull().sum() #True = missing value
    print(missing_vaule)
    print("Number of duplicated data:")
    print(df.duplicated().sum())

    # --- 3. Visualisations ---
    # create and save a pairplot using a few selected features
    features = ["alcohol", "ash", "magnesium", "flavanoids", "target"]
    pairplot = sns.pairplot(df[features], hue = "target")
    plt.savefig("pairplot_selected_feature.png")
    plt.close()

    # create and save a boxplot comparing one feature across classes
    sns.violinplot(x = df["target"], y = df ["alcohol"])
    plt.title("Alochol for each wine class")
    plt.xlabel("Wine class")
    plt.ylabel("Alcohol")
    plt.savefig("violinplot_alcohol.png")
    plt.close()

    # plot and save a heatmap (e.g. 'heatmap.png')
    correlation_matrix = df.corr()
    sns.heatmap(correlation_matrix, cmap = "coolwarm") #coolwarm: red = + blue = -
    plt.title("Correlation matrix")
    plt.savefig("heatmap.png")
    plt.close()

    # --- 4. Scaling and PCA ---
    # separate features (X) and target (y)
    x = df.drop(columns = "target")
    y = df["target"]
    # scale the features using StandardScaler
    scaler = StandardScaler()
    x_scaled = pd.DataFrame(scaler.fit_transform(x), columns = x.columns)
    # apply PCA (2 components)
    pca = PCA(n_components = 2)
    x_pca = pca.fit_transform(x_scaled)
    # create a DataFrame with PCA results and target
    df_pca = pd.DataFrame(x_pca, columns = ["PC1", "PC2"])
    df_pca["target"] = y
    # plot and save a scatterplot of the first two components (color by target)
    sns.scatterplot(data = df_pca, x = "PC1", y = "PC2", hue = "target", s=80)
    plt.title("PCA Visualization")
    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)")
    plt.savefig("PCA Visualization.png")
    plt.close()

    # --- 5. Classification models ---
    # Do a random train-test split (20%) 
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42, stratify = y)
    # Scale training and test features (fit_transform() on X_train, transform() on X_test)
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)
    # Train logistic regression, a decision tree and a random forest (default hyperparameters)
    #Logistic regression
    logreg = LogisticRegression()
    logreg.fit(x_train_scaled, y_train)
 
    #Decision tree
    tree = DecisionTreeClassifier()
    tree.fit(x_train, y_train)

    #Random forest
    forest = RandomForestClassifier()
    forest.fit(x_train, y_train)
    # Compare the label prediction accuracy of the different models.
    summary = pd.DataFrame({
        "Model": ["Logistic Regression", "Decision Tree", "Random Forest"],
        "Train Accuracy": [logreg.score(x_train_scaled, y_train), tree.score(x_train, y_train), forest.score(x_train, y_train)],
        "Test Accuracy": [logreg.score(x_test_scaled, y_test), tree.score(x_test, y_test), forest.score(x_test, y_test)]
    })
    print("summary:")
    print(summary)
    #Investigate feature importance in the Decision Tree and Random Forest.
    Dec_tree_importances = pd.Series(tree.feature_importances_, index = x.columns)
    Dec_tree_importances.sort_values().plot(kind = 'barh')
    plt.title("Feature Importances (Decision Tree)")
    plt.savefig("Feature Importances (Decision Tree).png")
    plt.close()
    forest_importance = pd.Series(forest.feature_importances_, index = x.columns)
    forest_importance.sort_values().plot(kind = "barh")
    plt.title("Feature Importances (Random Forest)")
    plt.savefig("Feature Importances (Random Forest).png")
    plt.close()
    
    # Train and evaluate the three models on the PCA data.
    x_train_pca = pca.fit_transform(x_train_scaled)
    x_test_pca = pca.transform(x_test_scaled)
    logreg_pca = LogisticRegression() #train logreg
    logreg_pca.fit(x_train_pca, y_train)
    
    tree_pca = DecisionTreeClassifier() #train decision tree
    tree_pca.fit(x_train_pca, y_train)

    forest_pca = RandomForestClassifier() #train random forest
    forest_pca.fit(x_train_pca, y_train)


    summary_pca = pd.DataFrame({
    "Model": ["Logistic Regression", "Decision Tree", "Random Forest"],
    "Train Accuracy": [logreg_pca.score(x_train_pca, y_train), tree_pca.score(x_train_pca, y_train), forest_pca.score(x_train_pca, y_train)],
    "Test Accuracy": [logreg_pca.score(x_test_pca, y_test), tree_pca.score(x_test_pca, y_test), forest_pca.score(x_test_pca, y_test)]
})
    print("summary of PCA:")
    print(summary_pca)

# Entry point
if __name__ == "__main__":
    main()