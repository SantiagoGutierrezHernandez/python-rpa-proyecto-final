def prepend_date_zero(number_string) -> str:
    if len(str(number_string)) < 2:
        return f"0{number_string}"
    return number_string

def date_compare(first, second):
    return abs((first - second).days)