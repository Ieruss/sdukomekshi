def get_gpa(score):
    if not score.isdigit():
        return 'None'
    score = int(score)
    if 95 <= score <= 100:
        return 4.0
    elif 90 <= score <= 94:
        return 3.67
    elif 85 <= score <= 89:
        return 3.33
    elif 80 <= score <= 84:
        return 3.0
    elif 75 <= score <= 79:
        return 2.67
    elif 70 <= score <= 74:
        return 2.33
    elif 65 <= score <= 69:
        return 2.0
    elif 60 <= score <= 64:
        return 1.67
    elif 55 <= score <= 59:
        return 1.33
    elif 50 <= score <= 54:
        return 1.0
    elif 25 <= score <= 49:
        return 0.0
    else:
        return 0.0