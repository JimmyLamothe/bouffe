import datetime
from JsonObject import JsonObject
from food_questions import get_name, get_categories, get_duration, get_months

class Food(JsonObject):
    def __init__(self, name): #name = str
        super().__init__(name)
        if not self.file_exists(): #Generates json file on first creation
            self.categories = get_categories() #Categories food belongs to
            if self.seasonal():
                self.months = get_months()
            if self.perishable() and not self.best_before():
                self.duration = get_duration()
                if self.duration == -1: #To allow correction of mistaken entry
                    self.categories.pop('perishable')
            else:
                self.duration = -1
            if self.perishable_opened():
                print('Once opened,')
                self.open_duration = get_duration()
                if not self.open_duration: #To allow correction of mistaken entry
                    self.categories.pop('perishable_opened')
            self.save_dict()

    def get_directory(self):
        return 'json/food/'

    def seasonal(self):
        if 'seasonal' in self.categories:
            return True
        return False

    def perishable(self):
        if 'perishable' in self.categories:
            return True
        return False
    
    def best_before(self):
        if 'best_before' in self.categories:
            return True
        return False

    def perishable_opened(self):
        if 'perishable_opened' in self.categories:
            return True
        return False

    def in_season(self):
        if not self.seasonal():
            return True
        if today.date.month in self.months:
            return True
        return False

    def update(): #Modify as needed when new property is added - Single use only
        import sys, os, json
        for file_string in os.listdir('json/food'):
            if not file_string.endswith('.json'):
                pass
            filepath = 'json/food/' + file_string
            print(filepath)
            print(type(filepath))
            with open(filepath, 'r') as json_file:
                json_dict = json.load(json_file)
                json_dict['name'] = input('Enter name')
                print(json_dict)
                if input('Continue? \n'):
                    with open(filepath, 'w') as json_file:
                        json.dump(json_dict, json_file)
                else:
                    continue


Food.update()
