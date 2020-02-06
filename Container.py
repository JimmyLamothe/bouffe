import time_methods as time
from JsonObject import JsonObject
from Food import Food
from food_info import food_list, print_food_list

class Container(JsonObject):
    def __init__(self, name):
        super().__init__(name)
        if not self.file_exists(): #Generates json file on first creation
            self.contents = {} #Food[[Portions, Date]] - Str[[Int,Str]]
            self.save_dict()
            self.fill_fridge()

    def add_food(self):
        food_name = input('Enter food:\n')
        if not food_name:
            return True #Stop when fridge is full
        if food_name not in food_list:
            confirm = input('Create new food item?\n')
            if not confirm:
                return self.add_food()
            Food(food_name) #Inititalize new food
        food_portions = input('Enter portions:\n')
        if not food_portions:
            return self.add_food()
        try:
            food_portions = int(food_portions)
        except InputError:
            print('Invalid portion quantity. Please enter food item again')
            return self.add_food()
        date_string = input('Enter age in days. If new, type ENTER.')
        if not date_string:
            food_date_string = time.today()
        else:
            try:
                food_date_string = time.past_date(int(date_string))
            except ValueError:
                print('Invalid age. Please enter food item again')
                return self.add_food()
        self.contents[food_name] = [food_portions, food_date_string]
        return self.add_food()

    def fill_fridge(self):
        print_food_list()
        print('Filling ' + self.name + '. Press ENTER when full.')        
        while not self.add_food():
            self.add_food()
