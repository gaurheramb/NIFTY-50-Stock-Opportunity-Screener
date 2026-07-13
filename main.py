import pandas as pd
import sys

import data
import utils

ATH_FALL_THRESHOLD = 20
OUTPUT_CSV_FILE = "ath_alerts.csv"


def analyze_stocks(stock_list):
    qualifying_stocks = []
    for ticker in stock_list:
        print(f"Fetching data for {ticker}...")
        stock_info = data.fetch_stock_data(ticker)
        if stock_info is None:
            print(f"  Skipping {ticker} (could not fetch data).")
            continue
        current_price = stock_info["current_price"]
        ath = stock_info["ath"]
        percent_fall = utils.calculate_percentage_fall(current_price, ath)
        if percent_fall >= ATH_FALL_THRESHOLD:
            qualifying_stocks.append({
                "Stock": ticker,
                "Current Price": round(current_price, 2),
                "ATH": round(ath, 2),
                "% Below ATH": round(percent_fall, 2),
            })
    return qualifying_stocks


def display_results(qualifying_stocks):
    if not qualifying_stocks:
        print("\nNo stocks are currently 20% or more below their ATH.")
        return pd.DataFrame(columns=["Stock", "Current Price", "ATH", "% Below ATH"])
    df = pd.DataFrame(qualifying_stocks)
    df = df.sort_values(by="% Below ATH", ascending=False).reset_index(drop=True)
    print("\n=== Stocks Trading 20%+ Below Their All-Time High ===\n")
    for _, row in df.iterrows():
        line = (
            f"{row['Stock']:<12} "
            f"Current: {row['Current Price']:<10} "
            f"ATH: {row['ATH']:<10} "
            f"Fall: {row['% Below ATH']}%"
        )
        print(utils.highlight_text(line, condition=True))
    return df


def export_to_csv(df, filename):
    try:
        df.to_csv(filename, index=False)
        print(f"\nResults exported successfully to '{filename}'")
    except Exception as e:
        print(f"\nError while exporting to CSV: {e}")


def main():
    print("Starting Large Cap Stock ATH Alert System...\n")
    try:
        stock_list = data.get_nifty50_list()
    except Exception as e:
        print(f"Fatal error: could not load stock list ({e})")
        sys.exit(1)
    qualifying_stocks = analyze_stocks(stock_list)
    results_df = display_results(qualifying_stocks)
    export_to_csv(results_df, OUTPUT_CSV_FILE)
    print("\nDone.")

if __name__ == "__main__":
    main()