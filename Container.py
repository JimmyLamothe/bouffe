import time_methods as time
from JsonObject import JsonObject
from Food import Food
from food_info import food_list, print_food_list
from food_questions import get_name, get_input, get_best_before_date
from utilities import remove_dupes

class Container(JsonObject):
    def __init__(self, name):
        super().__init__(name)
        if not self.file_exists(): #Generates json file on first creation
            self.contents = {} #Food:{Portions, Bad_Date} - Str:{Str:Int,Str:Str}
            self.staples = [] #List of food to be refilled when empty
            self.save_dict()

    def get_directory(self):
        return 'json/containers/'

    def add_food(self):
        food_name = get_name()
        if not food_name:
            return True #Stop when fridge is full
        if food_name not in food_list:
            confirm = get_input('Create new food item?\n')
            if not confirm:
                return self.add_food()
        food = Food(food_name) #Inititalize new food
        food_portions = input('Enter portions:\n')
        if not food_portions:
            return self.add_food()
        try:
            food_portions = int(food_portions)
        except InputError:
            print('Invalid portion quantity. Please enter food item again')
            return self.add_food()
        date_string = input('Enter age in days. If fresh, type ENTER.')
        if not date_string:
            food_date_string = time.today()
        else:
            try:
                food_date_string = time.past_date(int(date_string))
            except ValueError:
                print('Invalid age. Please enter food item again')
                return self.add_food()
        if food.best_before():
            bad_date = get_best_before_date()
        elif not food.perishable():
            bad_date = '2200-01-01'
        else:
            bad_date = time.get_future_date(food_date_string, food.duration)
            self.contents[food_name] = {'portions' : food_portions,
                                        'bad_date' : bad_date}
        return self.add_food()

    def fill_container(self):
        print_food_list()
        print('Filling ' + self.name + '. Press ENTER when full.')        
        while not self.add_food():
            self.add_food()

    def add_staple(self):
        food_name = get_name()
        if not food_name:
            return True #Stop when fridge is full
        if food_name not in food_list:
            confirm = input('Create new food item?\n')
            if not confirm:
                return self.add_staple()
            Food(food_name) #Inititalize new food
        self.staples.append(food_name)
        self.staples = remove_dupes(self.staples)
        
    def define_staples(self):
        print_food_list()
        print('Enter essential foods for ' + self.name + '. Press ENTER when done.')
        while not self.add_staple():
            self.add_staple()

    def open(self, food):
        if not food.perishable_opened:
            pass
        bad_date = time.get_future_date(time.today(), food.open_duration)
        self.contents[food.name]['bad_date'] = bad_date

    def bad(self, food):
        if time.past(self.contents[food.name]['bad_date']):
            return True
        return False
