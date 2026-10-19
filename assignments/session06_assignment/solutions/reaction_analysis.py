from kinetics_analyzer_solution import (
    calculate_reaction_rates,
    compare_setups,
    find_optimal_conditions,
)

from data_cleaner_solution import combine_datasets, load_and_clean_setup_data


def main():
    """Analyses the reaction data from two different setups."""
    
    # Load and clean data
    setup_a = load_and_clean_setup_data('data/setup_A.csv', 'A')
    setup_b = load_and_clean_setup_data('data/setup_B.csv', 'B')
    combined_data = combine_datasets(setup_a, setup_b)
    
    # Analyze data
    rates = calculate_reaction_rates(combined_data)
    optimal_conditions = find_optimal_conditions(combined_data)
    setup_comparison = compare_setups(combined_data)
    
    # Display results
    print("=== Kinetic Analysis Results ===")
    print(f"Optimal conditions: {optimal_conditions}")
    print(f"Setup comparison: {setup_comparison}")

if __name__ == "__main__":
    main()
