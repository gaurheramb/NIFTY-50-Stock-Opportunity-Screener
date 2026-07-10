"""
main.py
--------
Entry point for the Large Cap Stock ATH Alert System.

This script:
1. Gets the list of NIFTY 50 stocks (from data.py)
2. Fetches current price + all-time high for each stock (from data.py)
3. Calculates % fall from ATH (from utils.py)
4. Filters stocks that are at least 20% below their ATH
5. Displays results in a pandas DataFrame with color highlighting
6. Exports the final results to a CSV file

NOTE: data.py and utils.py are currently placeholders (empty).
This file assumes the following functions will exist there:

    data.py:
        - get_nifty50_list() -> list[str]
        - fetch_stock_data(ticker: str) -> dict | None

    utils.py:
        - calculate_percentage_fall(current_price, ath) -> float
        - highlight_text(text, condition) -> str   # for terminal colors

Once you confirm, we'll implement these in data.py and utils.py so this
script runs end-to-end.
"""

import pandas as pd          # For creating and displaying the results table
import sys                   # For exiting gracefully on critical errors

import data                  # Our custom module: handles fetching stock data
import utils                 # Our custom module: handles calculations & formatting


# ----------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------
ATH_FALL_THRESHOLD = 20      # % fall from ATH required to qualify as an "alert"
OUTPUT_CSV_FILE = "ath_alerts.csv"  # File where results will be saved


def analyze_stocks(stock_list):
    """
    Loop through every stock in stock_list, fetch its data, calculate the
    percentage fall from ATH, and collect only the stocks that qualify
    (i.e., are at least ATH_FALL_THRESHOLD % below their all-time high).

    Parameters:
        stock_list (list[str]): List of NIFTY 50 stock ticker symbols.

    Returns:
        list[dict]: A list of dictionaries, one per qualifying stock,
                     each containing Stock, Current Price, ATH, % Below ATH.
    """
    qualifying_stocks = []  # This will store only the stocks that pass our filter

    # Go through each stock one at a time
    for ticker in stock_list:
        print(f"Fetching data for {ticker}...")  # Progress indicator for the user

        # Ask data.py to fetch the price info for this stock.
        # This function is expected to handle its own API/network errors
        # and return None if something goes wrong (so this loop can skip it).
        stock_info = data.fetch_stock_data(ticker)

        # If fetching failed (bad ticker, no internet, API issue), skip this stock
        if stock_info is None:
            print(f"  Skipping {ticker} (could not fetch data).")
            continue

        current_price = stock_info["current_price"]
        ath = stock_info["ath"]

        # Calculate how far the current price has fallen from the ATH, in %
        percent_fall = utils.calculate_percentage_fall(current_price, ath)

        # Only keep stocks that have fallen by at least our threshold (20%)
        if percent_fall >= ATH_FALL_THRESHOLD:
            qualifying_stocks.append({
                "Stock": ticker,
                "Current Price": round(current_price, 2),
                "ATH": round(ath, 2),
                "% Below ATH": round(percent_fall, 2),
            })

    return qualifying_stocks


def display_results(qualifying_stocks):
    """
    Convert the list of qualifying stocks into a pandas DataFrame,
    print it to the terminal with color highlighting, and return the
    DataFrame so it can be exported to CSV.

    Parameters:
        qualifying_stocks (list[dict]): Output from analyze_stocks().

    Returns:
        pandas.DataFrame: The results in tabular form.
    """
    # If nothing qualified, tell the user clearly instead of showing an empty table
    if not qualifying_stocks:
        print("\nNo stocks are currently 20% or more below their ATH.")
        return pd.DataFrame(columns=["Stock", "Current Price", "ATH", "% Below ATH"])

    # Build a DataFrame from our list of dictionaries.
    # Each dictionary becomes one row; keys become column names.
    df = pd.DataFrame(qualifying_stocks)

    # Sort so the stocks that have fallen the MOST appear at the top
    df = df.sort_values(by="% Below ATH", ascending=False).reset_index(drop=True)

    print("\n=== Stocks Trading 20%+ Below Their All-Time High ===\n")

    # Print each row manually so we can apply color formatting per row
    for _, row in df.iterrows():
        line = (
            f"{row['Stock']:<12} "
            f"Current: {row['Current Price']:<10} "
            f"ATH: {row['ATH']:<10} "
            f"Fall: {row['% Below ATH']}%"
        )
        # utils.highlight_text will wrap 'line' in terminal color codes
        # if the condition (here, always True since it already qualified) is met
        print(utils.highlight_text(line, condition=True))

    return df


def export_to_csv(df, filename):
    """
    Save the results DataFrame to a CSV file.

    Parameters:
        df (pandas.DataFrame): The results to save.
        filename (str): Name of the output CSV file.
    """
    try:
        df.to_csv(filename, index=False)
        print(f"\nResults exported successfully to '{filename}'")
    except Exception as e:
        # Catch any file-write issues (permissions, disk space, etc.)
        print(f"\nError while exporting to CSV: {e}")


def main():
    """
    Main function that ties everything together:
    1. Get the stock list
    2. Analyze each stock
    3. Display results
    4. Export results to CSV
    """
    print("Starting Large Cap Stock ATH Alert System...\n")

    # Step 1: Get the list of NIFTY 50 stock tickers from data.py
    try:
        stock_list = data.get_nifty50_list()
    except Exception as e:
        # If we can't even get the stock list, there's no point continuing
        print(f"Fatal error: could not load stock list ({e})")
        sys.exit(1)  # Exit the program with an error code

    # Step 2: Analyze all stocks and find the ones that qualify
    qualifying_stocks = analyze_stocks(stock_list)

    # Step 3: Display the results in a clean, colored table
    results_df = display_results(qualifying_stocks)

    # Step 4: Export results to CSV (even if empty, for consistency)
    export_to_csv(results_df, OUTPUT_CSV_FILE)

    print("\nDone.")


# This ensures main() only runs when this file is executed directly,
# not when it's imported as a module elsewhere.
if __name__ == "__main__":
    main()