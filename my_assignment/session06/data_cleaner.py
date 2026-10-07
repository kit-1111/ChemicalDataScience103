import pandas as pd

def load_and_clean_setup_data(filepath, setup_name):
    """Load and standardize data from one setup"""
    df = pd.read_csv(filepath)

    df = df.rename(columns = { "temperature_C": "temp_C", "temp_fahrenheit": "temp_F",  "concentration_M": "conc", "molarity": "conc",
        "ph_value": "ph", "yield_percent" : "%yield", "product_yield": "%yield",})

    if "temp_F" in df.columns:
        df["temp_C"] = (df["temp_F"] - 32) * 5 / 9 #convert units
        df = df[["time_min","temp_C", "conc", "ph", "%yield"]] #remain the same columns/names in both csv

    df = df.dropna() #For handle missing values 
    df["setup"] = setup_name
    return df

def combine_datasets(setup_a_data, setup_b_data):
    """Combine two datasets into one"""
    list_dfs = [setup_a_data, setup_b_data]
    combined_df = pd.concat(list_dfs, ignore_index=True) #group to dataframe and reset index from 0 to n
    return combined_df
