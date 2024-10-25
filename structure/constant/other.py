def get_day_of_week(day: int) -> str:
    arr = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    return arr[day - 1] if 0 < day < 7 else 'None'