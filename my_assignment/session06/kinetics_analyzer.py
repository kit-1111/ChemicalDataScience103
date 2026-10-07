import numpy as np

def calculate_reaction_rates(dataframe):
    """Calculate reaction rates for each time interval"""
    df = dataframe.copy() 
    conc_change = df.groupby("setup")["conc"].diff() 
    time_change = df.groupby("setup")["time_min"].diff() 
    df["rate"] = -conc_change / time_change #add column rate
    return df

def find_optimal_conditions(dataframe, rates = None):
    """Analyze data to find optimal reaction conditions"""
    df = dataframe.copy()
    yield_change = df.groupby("setup")["%yield"].diff()       
    time_change = df.groupby("setup")["time_min"].diff()         
    df["yield_per_min"] = yield_change / time_change                         
    df["temp_start"] = df.groupby("setup")["temp_C"].shift(1)                         
    best = df.loc[df["yield_per_min"].idxmax()]
    return (f'the best temp. range is from {best["temp_start"]} to {best["temp_C"]}')

def compare_setups(dataframe):
    """Compare performance between setups A and B"""
    mean_yield = dataframe.groupby("setup")["%yield"].mean()
    max_mean_setup = mean_yield.idxmax()
    return max_mean_setup