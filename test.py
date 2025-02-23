from datetime import datetime

def string_to_date(date_string):
    parts = date_string.strip().split()
    current_year = datetime.now().year
    date = f"{parts[0]} {parts[2]}{current_year}"
    date_format = "%H:%M %d.%m.%Y"
    date_object = datetime.strptime(date, date_format)
    
    # Adjust year if the date is more than 3 days ahead
    today = datetime.now()
    if abs((date_object - today).days) > 3:
        date_object = date_object.replace(year=current_year + 1)
    
    return date_object

# Example usage
date_string = ' 04:30 Ned 23.02. '
date_object = string_to_date(date_string)
print(date_object)  
print(type(date_object))