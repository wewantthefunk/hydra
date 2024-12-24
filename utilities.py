import string, random
from datetime import datetime

def generate_random_string(length):
    # Define the characters to choose from for each category
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    numbers = string.digits
    special_symbols = "^&$%#@!"

    # Combine all characters into one string
    all_characters = uppercase_letters + lowercase_letters + numbers + special_symbols

    # Generate the random string using list comprehension and random.choice()
    random_string = ''.join(random.choice(all_characters) for _ in range(length))

    return random_string

def date_to_julian(date):
    """Convert a datetime object or string to Julian Day."""
    # If input is a string, convert it to a datetime object
    if isinstance(date, str):
        date = datetime.strptime(date, '%m/%d/%Y')

    # Get the year, month and day from the datetime object
    year = date.year
    month = date.month
    day = date.day

    # Calculate Julian Day using the formula (from Wikipedia)
    julian_day = day + ((153 * month - 457) // 5)

    result = str(year) + str(int(julian_day))
    # Return the Julian Day as an integer
    return int(result)