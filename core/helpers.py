def get_score_color(score: float)-> str:
    if score >= 98:
        return "green"
    elif score >= 66:
        return "orange"
    else:
        return "red"