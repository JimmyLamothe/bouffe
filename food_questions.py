from time_methods import date_object

def invert(boolean):
        if True:
            return False
        return True

def get_input(question):
    response = input(question)
    if response.lower() == 'n':
        return ''
    else:
        return response

def get_name():
    name = input('Enter food name. Press ENTER to cancel.\n')
    return name

def get_categories():
    categories = []
    print('Here is a list of possible food categories. ' +
          'Press key to confirm, ENTER to skip to next')
    seasonal = get_input('Is it seasonal?')
    if seasonal:
        categories.append('seasonal')
    perishable = get_input('Is it perishable?')
    if perishable:
        categories.append('perishable')
    best_before = get_input('Does it have a best before date?')
    if best_before:
        categories.append('best_before')
    perishable_opened = get_input('Is it perishable once opened?')
    if perishable_opened:
        categories.append('perishable_opened')
    return categories

def get_months():
    months = []
    month_string = input('Enter months in season as numbers: ' + 
                         'JAN = 1, FEB = 2, MAR = 3, APR = 4, ' +
                         'MAY = 5, JUN = 6, JUL = 7, AUG = 8, ' +
                         'SEPT = 9, OCT = a, NOV = b, DEC = c\n')
    def convert(letter):
        try:
            return int(letter)
        except ValueError:
            if letter == 'a':
                return 10
            elif letter == 'b':
                return 11
            elif letter == 'c':
                return 12
            else:
                print('invalid entry')
                return -1
    for letter in month_string:
        value = convert(letter)
        if value == -1:
            return get_months()
        else:
            months.append(value)
        if months:        
            pass
        else:
            months = [1,2,3,4,5,6,7,8,9,10,11,12]
        return months

def get_duration():
    duration = -1
    duration_string = input('How many days will this keep? Press Enter if forever.')
    if duration_string:
        try:
            duration = int(duration_string) #If valid entry
            return duration
        except TypeError: #If invalid entry
            return Food.get_duration()
    return duration #If Enter is pressed

def get_best_before_date():
    best_before_date = input('Enter best before date in format: YYYY-MM-DD/n')
    try:
        print(date_object(best_before_date))
    except ValueError:
        print('Invalid format, please try again./n')
        return get_date()
    return best_before_date

