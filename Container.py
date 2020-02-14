import time_methods as time
from JsonObject import JsonObject
from Food import Food
from food_info import food_list, print_food_list
from food_questions import get_name, get_input, get_best_before_date
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

    def transfer_food(self, destination, id):
        print('Adding ' + self.contents[id]['food_name'] + ' to ' + destination.name)
        destination.contents[id] = self.contents[id]
        self.remove_food(id)
        self.save_dict()
        destination.save_dict()

    def add_new_food(self):
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

    def get_portions(self, id):
        portions = self.contents[id]['portions']
        return portions

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
            portions = self.get_portions(id)
            in_date = self.get_in_date(id)
            bad_date = self.get_bad_date(id)
            food_age = self.get_age(id)
            portion_string = '\n' + food_name + ': ' +  str(portions) + ' portions.\n'
            age_string = 'Âge: ' + food_age + ' jours.\n'
            if self.get_bad(id):
                bad_string = 'Cet aliment est passé date.'
            else:
                bad_days = self.get_bad_days(id)
                bad_string = 'Encore bon pour ' + bad_days + ' jours.\n\n'
                if int(bad_days) > 60000:
                    bad_string = 'Pas de date d\'expiration\n\n'
            return_string += portion_string + age_string + bad_string
        return return_string

    def update(self): #NOTE - Single use function - Change when underlying model changes
        old_dict = self.contents
        new_dict = {}
        for name in old_dict:
            id = get_uuid()
            portions = old_dict[name]['portions']
            in_date = old_dict[name]['in_date']
            bad_date = old_dict[name]['bad_date']
            new_dict[id] = {'food_name' : name,
                            'portions' : portions,
                            'in_date' : in_date,
                            'bad_date' : bad_date}
        self.contents = new_dict
        self.save_dict() #NOTE - Almost always necessary

