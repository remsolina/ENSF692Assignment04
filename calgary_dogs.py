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
    """Load the Excel data into a DataFrame and set a multi-index on 'Year' and 'Breed'.

    Args:
        filepath (str): The path to the Excel file.

    Returns:
        pd.DataFrame: The loaded DataFrame with a multi-index.
    """
    df = pd.read_excel(filepath)
    df.set_index(['Year', 'Breed'], inplace=True)
    return df

def get_dog_breed(df):
    """Prompt the user to enter a dog breed and validate the input.

    Args:
        df: The DataFrame containing dog breed data.

    Returns:
        str: The validated breed name in uppercase.
    """
    while True:
        try:
            breed = input("Please enter a dog breed: ").strip().upper()
            if breed not in df.index.get_level_values('Breed').str.upper():
                raise KeyError
            return breed
        except KeyError:
            print("Dog breed not found in the data. Please try again.")

def filter_breed_data(df, breed):
    """Filter the DataFrame for the selected breed.

    Args: 
        df: The DataFrame containing dog breed data.
        breed (str): The breed name in uppercase.

    Returns:
        breed_df: The filtered DataFrame containing only the selected breed.
    """
    breed_df = df.xs(breed, level='Breed', drop_level=False)
    return breed_df

def print_years_listed(breed_df, breed):
    """Print the years in which the breed was listed.

    Args:
        breed_df: The DataFrame containing data for the selected breed.
        breed: The breed name in uppercase.
    """
    years_listed = breed_df.index.get_level_values('Year').unique()
    years_listed_str = ', '.join(map(str, years_listed))
    print(f"The {breed} was found in the top breeds for years: {years_listed_str}")

def print_total_registrations(breed_df, breed):
    """Print the total number of registrations for the breed.

    Args:
        breed_df: The DataFrame containing data for the selected breed.
        breed (str): The breed name in uppercase.
    """
    total_breeds = breed_df['Total'].sum()
    print(f"There have been {total_breeds} {breed} dogs registered total.")

def print_percentages(df, breed_df, breed):
    """Print the percentage of the breed in top breeds for each year and overall.

    Args:
        df: The DataFrame containing dog breed data.
        breed_df: The DataFrame containing data for the selected breed.
        breed (str): The breed name in uppercase.
    """
    total_breeds_all_years = df.groupby('Year')['Total'].sum()
    percentages = {}

    for year in total_breeds_all_years.index:
        total_in_year = breed_df.loc[year, 'Total'].sum()
        if total_breeds_all_years[year] > 0:  # Avoid division by zero
            percentages[year] = total_in_year / total_breeds_all_years[year] * 100

    for year, percentage in percentages.items():
        print(f"The {breed} was {percentage:.6f}% of top breeds in {year}")

    total_all_years = total_breeds_all_years.sum()
    if total_all_years > 0:  # Avoid division by zero
        total_breeds = breed_df['Total'].sum()
        percentage_all_years = total_breeds / total_all_years * 100
        print(f"The {breed} was {percentage_all_years:.6f}% of top breeds across all years")

def print_popular_months(breed_df, breed):
    """Print the most popular month(s) for the breed.

    Args:
        breed_df: The DataFrame containing data for the selected breed.
        breed (str): The breed name in uppercase.
    """
    months_totals = breed_df.groupby('Month')['Month'].count()
    max_monthly_totals = months_totals.max()
    popular_months = months_totals[months_totals == max_monthly_totals].index.tolist()
    print(f"Most popular month(s) for {breed} dogs: {' '.join(map(str, popular_months))}")

def main():
    """Main function to execute the program."""
    # Import data here
    filepath = 'CalgaryDogBreeds.xlsx'
    df = load_data(filepath)

    # User input stage
    breed = get_dog_breed(df)
    
    # Data anaylsis stage
    breed_df = filter_breed_data(df, breed)
    print_years_listed(breed_df, breed)
    print_total_registrations(breed_df, breed)
    print_percentages(df, breed_df, breed)
    print_popular_months(breed_df, breed)

if __name__ == "__main__":
    main()
