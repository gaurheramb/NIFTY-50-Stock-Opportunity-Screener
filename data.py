import yfinance as yf
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
    return NIFTY_50_TICKERS


def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="max")
        if history.empty:
            print(f"  Warning: No data returned for {ticker}.")
            return None
        current_price = history["Close"].iloc[-1]
        ath = history["Close"].max()
        return {
            "current_price": float(current_price),
            "ath": float(ath),
        }
    except Exception as e:
        print(f"  Error fetching data for {ticker}: {e}")
        return None