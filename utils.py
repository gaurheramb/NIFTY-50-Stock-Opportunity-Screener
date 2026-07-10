"""
utils.py
--------
Small, reusable HELPER functions that don't belong to "fetching data"
(that's data.py's job) or "orchestrating the program" (that's main.py's job).

Specifically:
1. calculate_percentage_fall() - the math for how far a stock has fallen from ATH.
2. highlight_text() - wraps text in ANSI color codes for terminal highlighting.
"""

# ----------------------------------------------------------------------
# ANSI COLOR CODES
# ----------------------------------------------------------------------
# These are special character sequences that most terminals understand as
# "change the text color from here" rather than literal text to display.
# We don't need an external library (like colorama) for basic colors on
# Linux/Mac terminals, which keeps our requirements.txt smaller.
GREEN = "\033[92m"   # Used to highlight qualifying stocks (the "alert" color)
RESET = "\033[0m"    # Resets the color back to the terminal's default


def calculate_percentage_fall(current_price, ath):
    """
    Calculate how far the current price has fallen from the all-time high,
    expressed as a percentage.

    Formula:
        % fall = ((ATH - Current Price) / ATH) * 100

    Example:
        ATH = 1000, Current Price = 800
        % fall = ((1000 - 800) / 1000) * 100 = 20.0

    Parameters:
        current_price (float): The stock's current/latest price.
        ath (float): The stock's all-time high price.

    Returns:
        float: The percentage fall from ATH. Returns 0.0 if ath is 0 or
               invalid, to avoid a divide-by-zero crash.
    """
    # Defensive check: if ATH is 0 or negative (shouldn't normally happen,
    # but data can be messy), avoid a ZeroDivisionError and just return 0.
    if not ath or ath <= 0:
        return 0.0

    percentage_fall = ((ath - current_price) / ath) * 100

    # A stock currently AT or ABOVE its ATH would give a negative or zero
    # result here, which is correct — it simply won't pass the 20% filter
    # in main.py. We don't need to clamp it; negative just means "at/above ATH".
    return percentage_fall


def highlight_text(text, condition):
    """
    Wrap a line of text in green ANSI color codes IF the given condition
    is True. Used to visually highlight qualifying stocks in the terminal
    output so they stand out from regular text.

    Parameters:
        text (str): The text to potentially highlight.
        condition (bool): Whether to apply the highlight color.
                           (In this project, every row printed already
                           qualified, so condition is always True — but
                           keeping it as a parameter makes this function
                           reusable if you later want conditional coloring,
                           e.g. different colors for different fall ranges.)

    Returns:
        str: The original text, wrapped in color codes if condition is True,
             or unchanged if condition is False.
    """
    if condition:
        return f"{GREEN}{text}{RESET}"
    return text