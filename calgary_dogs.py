# calgary_dogs.py
# AUTHOR NAME: Remi Oyediji
#
# A terminal-based application for computing and printing statistics based on given input.
# Detailed specifications are provided via the Assignment 4 README file.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.

import pandas as pd

def load_data(filepath):
    """
    Load the Excel file into a DataFrame.
    """
    return pd.read_excel(filepath)

def get_breed_from_user(df):
    """
    Prompt the user to input a dog breed until a valid breed is entered.
    """
    while True:
        try:
            breed = input("Please enter a dog breed: ").strip().upper()
            if breed not in df['Breed'].str.upper().values:
                raise KeyError
            return breed
        except KeyError:
            print("Dog breed not found in the data. Please try again.")

def calculate_statistics(df, breed):
    """
    Calculate and print various statistics for the given dog breed.
    """
    # Filter the DataFrame for the specified breed
    breed_mask = df['Breed'].str.upper() == breed
    breed_df = df[breed_mask]
    
    # List the years the breed was found in the top breeds
    years_listed = breed_df['Year'].unique()
    years_listed_str = ', '.join(str(year) for year in years_listed)
    print(f"The {breed} was found in the top breeds for years {years_listed_str}")
    
    # Calculate total registrations for the breed
    total_breeds = breed_df['Total'].sum()
    print(f"There have been {total_breeds} {breed} dogs registered total.")
    
    # Calculate total registrations for each year
    total_breeds_2021 = sum(df[df['Year'] == 2021]['Total'])
    total_breeds_2022 = sum(df[df['Year'] == 2022]['Total'])
    total_breeds_2023 = sum(df[df['Year'] == 2023]['Total'])
    total_in_2021 = sum(breed_df[breed_df['Year'] == 2021]['Total'])
    total_in_2022 = sum(breed_df[breed_df['Year'] == 2022]['Total'])
    total_in_2023 = sum(breed_df[breed_df['Year'] == 2023]['Total'])
    total_all_years = total_breeds_2021 + total_breeds_2022 + total_breeds_2023
    
    # Calculate percentage of breed registrations for each year
    percentage_2021 = total_in_2021 / total_breeds_2021 * 100 if total_breeds_2021 > 0 else 0
    percentage_2022 = total_in_2022 / total_breeds_2022 * 100 if total_breeds_2022 > 0 else 0
    percentage_2023 = total_in_2023 / total_breeds_2023 * 100 if total_breeds_2023 > 0 else 0
    percentage_all_years = total_breeds / total_all_years * 100 if total_all_years > 0 else 0
    
    print(f"The {breed} was {percentage_2021:.6f}% of top breeds in 2021")
    print(f"The {breed} was {percentage_2022:.6f}% of top breeds in 2022")
    print(f"The {breed} was {percentage_2023:.6f}% of top breeds in 2023")
    print(f"The {breed} was {percentage_all_years:.6f}% of top breeds across all years")

    # Find the most popular months for the breed
    months_totals = breed_df.groupby('Month')['Month'].count()
    max_monthly_totals = months_totals.max()
    popular_months = months_totals[months_totals == max_monthly_totals].index.tolist()
    
    print(f"Most popular month(s) for {breed} dogs: {' '.join(str(month) for month in popular_months)}")

def main():
    filepath = 'CalgaryDogBreeds.xlsx'
    df = load_data(filepath)
    breed = get_breed_from_user(df)
    calculate_statistics(df, breed)

if __name__ == "__main__":
    main()
