import datetime
from JsonObject import JsonObject

class Food(JsonObject):
    def __init__(self, name): #name = str
        super().__init__(name)
        if not self.file_exists(): #Generates json file on first creation
            self.duration = Food.get_duration()
            self.save_dict()

    def get_duration():
        duration = 0
        duration_string = input('How many days will this keep? Press Enter if forever.')
        if duration_string:
            try:
                duration = int(duration_string) #If valid entry
                return duration
            except TypeError: #If invalid entry
                return Food.get_duration()
        return duration #If Enter is pressed

    def update(): #Modify as needed when new property is added - Single use only
        import sys, os, json
        for file_string in os.listdir('json'):
            if not file_string.endswith('.json'):
                pass
            filepath = 'json/' + file_string
            print(filepath)
            print(type(filepath))
            with open(filepath, 'r') as json_file:
                json_dict = json.load(json_file)
                if not 'name' in json_dict:
                    json_dict['name'] = input('Enter name: \n')
                print(json_dict)
                if ('Continue? \n'):
                    with open(filepath, 'w') as json_file:
                        json.dump(json_dict, json_file)
                else:
                    continue

class Vegetable(Food):
    def __init__(self, name):
        super().__init__(name)
        if not 'months' in self.__dict__: #Defines vegetable characteristics on first creation
            self.months = Vegetable.get_months()
            self.save_dict()

    def in_season(self):
        if today.date.month in self.months:
            return True
        return False

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
                return Vegetable.get_months()
            else:
                months.append(value)
        if months:        
            pass
        else:
            months = [1,2,3,4,5,6,7,8,9,10,11,12]
        return months
