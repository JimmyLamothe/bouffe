import os
from pathlib import Path
import time_methods as time
from JsonObject import JsonObject
from Food import Food
from food_info import food_list, print_food_list
from food_questions import get_name, get_input, get_best_before_date, get_choice
from utilities import remove_dupes, get_uuid

class Container(JsonObject):
    def __init__(self, name):
        super().__init__(name)
        if not self.file_exists(): #Generates json file on first creation
            self.contents = {} #food_name:{portions, in_date, bad_date} - Str:{Str:Int,Str:Str,Str:Str}
            self.staples = [] #List of food to be refilled when empty
            self.save_dict()

    def get_directory(self):
        return 'json/containers/'

    def add_food(self, food_name, food_portions, food_date_string, bad_date):
        id = get_uuid()
        self.contents[id] = {'food_name' : food_name,
                             'portions' : food_portions,
                             'in_date' : food_date_string,
                             'bad_date' : bad_date}
        self.save_dict()
        print('Food added to container. Saved to disk.\n')

    def remove_food(self, id):
        print('Removing ' + self.contents[id]['food_name'] + ' from ' + self.name)
        del self.contents[id]
        self.save_dict()

    def remove_food_by_name(self, name):
        id = self.get_id_by_name(name)
        self.remove_food(id)

    def get_id_by_name(self, name):
        possibilities = {key : index for key, index in self.contents.items()
                         if self.contents[key]['food_name'] == name}
        print('Choose from the following food items:\n')
        print(possibilities)
        ids = []
        in_dates = []
        for key in possibilities:
            ids.append(key)
            in_dates.append(possibilities[key]['in_date'])
        choice = get_choice(in_dates)
        return ids[choice]

    def transfer_food(self, destination, id):
        print('Adding ' + self.contents[id]['food_name'] + ' to ' + destination.name)
        destination.contents[id] = self.contents[id]
        self.remove_food(id)
        self.save_dict()
        destination.save_dict()

    def add_new_food(self, food_name = None):
        if not food_name:
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
            bad_date = time.future_date(food_date_string, food.duration)
        self.add_food(food_name, food_portions, food_date_string, bad_date)

    def fill_container(self):
        print_food_list()
        print(self)
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
        self.save_dict()

    def define_staples(self):
        print_food_list()
        print('Enter essential foods for ' + self.name + '. Press ENTER when done.')
        while not self.add_staple():
            self.add_staple()

    def open(self, food_name):
        food = Food(food_name)
        if not food.perishable_opened:
            pass
        bad_date = time.get_future_date(time.today(), food.open_duration)
        self.contents[food_name]['bad_date'] = bad_date

    def freeze(self, freezer, id): #Reskin of transfer food - Possible to modify later
        self.transfer_food(freezer, id)

    def get_bad(self, id):
        if time.past(self.contents[id]['bad_date']):
            return True
        return False

    def get_age(self, id):
        in_date = self.contents[id]['in_date']
        food_age = time.age(in_date, time.today())
        return food_age

    def get_bad_days(self, id):
        bad_date = self.contents[id]['bad_date']
        bad_days = time.age(time.today(), bad_date)
        return bad_days

    def get_food_name(self, id):
        food_name = self.contents[id]['food_name']
        return food_name

    def get_quantity(self, id):
        quantity = self.contents[id]['quantity']
        return quantity

    def get_in_date(self, id):
        in_date = self.contents[id]['in_date']
        return in_date

    def get_bad_date(self, id):
        bad_date = self.contents[id]['bad_date']
        return bad_date

    def __repr__(self):
        return_string = ''
        for id in self.contents:
            food_name = self.get_food_name(id)
            quantity = self.get_quantity(id)
            in_date = self.get_in_date(id)
            bad_date = self.get_bad_date(id)
            food_age = self.get_age(id)
            name_string = food_name + ':\n'
            if quantity == 'green':
                quantity_string = 'Quantité suffisante.\n'
            elif quantity == 'orange':
                quantity_string = 'Presque terminé.\n'
            else:
                'BOGUE - Vérifier json pour la quantité'
            age_string = 'Âge: ' + food_age + ' jours.\n'
            if self.get_bad(id):
                bad_string = 'Cet aliment est passé date.\n\n'
            else:
                bad_days = self.get_bad_days(id)
                bad_string = 'Encore bon pour ' + bad_days + ' jours.\n\n'
                if int(bad_days) > 60000:
                    bad_string = 'Pas de date d\'expiration\n\n'
            return_string += name_string + quantity_string + age_string + bad_string
        return return_string

    def update(self): #NOTE - Single use function - Change when underlying model changes
        old_dict = self.contents
        new_dict = {}
        for id in old_dict:
            name = old_dict[id]['food_name']
            in_date = old_dict[id]['in_date']
            bad_date = old_dict[id]['bad_date']
            new_dict[id] = {'food_name' : name,
                            'quantity' : 'green',
                            'in_date' : in_date,
                            'bad_date' : bad_date}
        self.contents = new_dict
        self.save_dict() #NOTE - Almost always necessary

    #class variable
    directory = 'json/containers/'

    @staticmethod
    def update_all(): #applies update to all containers in directory
        directory = Container.directory
        for filename in os.listdir(directory):
            path_object = Path(directory + filename)
            container_object = Container(path_object.stem)
            container_object.update()

    @staticmethod
    def print_all():
        directory = Container.directory
        for filename in os.listdir(directory):
            path_object = Path(directory + filename)
            container_object = Container(path_object.stem)
            print(container_object)
