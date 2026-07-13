GREEN = "\033[92m"
RESET = "\033[0m"


def calculate_percentage_fall(current_price, ath):
    if not ath or ath <= 0:
        return 0.0
    percentage_fall = ((ath - current_price) / ath) * 100
    return percentage_fall


def highlight_text(text, condition):
    if condition:
        return f"{GREEN}{text}{RESET}"
    return text