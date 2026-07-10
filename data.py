"""
data.py
--------
Handles everything related to GETTING data:
1. The list of NIFTY 50 stock tickers.
2. Fetching current price + all-time high (ATH) for a given ticker using yfinance.

This is the ONLY file that talks to the internet / yfinance. If yfinance's
API changes in the future, this is the only file you'd need to touch.
"""

import yfinance as yf   # Library used to pull stock price data from Yahoo Finance


# ----------------------------------------------------------------------
# NIFTY 50 STOCK LIST
# ----------------------------------------------------------------------
# yfinance needs the ".NS" suffix for stocks listed on the National Stock
# Exchange of India (NSE). This is a static list because NIFTY 50
# constituents change only occasionally (a few times a year, via index
# rebalancing) — hardcoding avoids depending on a fragile scraping step
# just to get 50 well-known tickers.
NIFTY_50_TICKERS = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS",
    "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS",
    "BEL.NS", "BHARTIARTL.NS", "CIPLA.NS", "COALINDIA.NS",
    "DRREDDY.NS", "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS",
    "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS",
    "HINDUNILVR.NS", "ICICIBANK.NS", "INDUSINDBK.NS", "INFY.NS",
    "ITC.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS",
    "M&M.NS", "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS",
    "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS",
    "SBIN.NS", "SHRIRAMFIN.NS", "SUNPHARMA.NS", "TATACONSUM.NS",
    "TATAMOTORS.NS", "TATASTEEL.NS", "TCS.NS", "TECHM.NS",
    "TITAN.NS", "TRENT.NS", "ULTRACEMCO.NS", "UPL.NS",
    "WIPRO.NS", "LTIM.NS",
]


def get_nifty50_list():
    """
    Return the list of NIFTY 50 stock tickers (NSE format, with ".NS" suffix).

    This function exists (rather than main.py just importing the constant
    directly) so that later you could swap this out for a live-scraped
    list from NSE's website without changing anything in main.py.

    Returns:
        list[str]: Ticker symbols, e.g. ["RELIANCE.NS", "TCS.NS", ...]
    """
    return NIFTY_50_TICKERS


def fetch_stock_data(ticker):
    """
    Fetch the current price and all-time high (ATH) for a single stock.

    How ATH is calculated:
        We download the FULL price history available for the ticker
        (period="max") and take the highest "Close" price ever recorded.
        This is an approximation of ATH based on closing prices — using
        intraday highs would require different data and is unnecessary
        for a beginner-to-intermediate project like this.

    How current price is fetched:
        We take the most recent closing price from the same history pull,
        which avoids making a second network call just for the latest price.

    Parameters:
        ticker (str): Stock ticker symbol, e.g. "RELIANCE.NS"

    Returns:
        dict | None:
            On success: {"current_price": float, "ath": float}
            On failure: None (so the caller in main.py can skip this stock
                        instead of the whole program crashing)
    """
    try:
        # Create a yfinance Ticker object — this doesn't hit the network yet,
        # it just prepares a handle we can query.
        stock = yf.Ticker(ticker)

        # Download the full historical price data for this stock.
        # period="max" means "give me everything you have, since listing".
        # This single call gives us both the ATH (max of all closes) and
        # the current price (last close), so we don't need two API calls.
        history = stock.history(period="max")

        # If yfinance returns an empty DataFrame, the ticker was likely
        # invalid, delisted, or there was a temporary data issue.
        if history.empty:
            print(f"  Warning: No data returned for {ticker}.")
            return None

        # The "Close" column holds closing prices for every trading day
        # in the history. Current price = the most recent day's close.
        current_price = history["Close"].iloc[-1]

        # All-time high = the highest closing price across the entire history.
        ath = history["Close"].max()

        return {
            "current_price": float(current_price),
            "ath": float(ath),
        }

    except Exception as e:
        # This catches ALL possible failure types for a robust, beginner-
        # friendly project:
        #   - No internet connection
        #   - Yahoo Finance API being temporarily down or rate-limiting us
        #   - Invalid/delisted ticker symbol
        #   - Any unexpected parsing error
        # Instead of crashing the whole program, we log it and return None,
        # so main.py's loop can simply skip this one stock and continue.
        print(f"  Error fetching data for {ticker}: {e}")
        return None