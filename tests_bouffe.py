from Container import Container
from Food import Food
from food_questions import get_input
from utilities import backup_json

def test_fill():
    test_fridge = Container('test')
    print(test_fridge.contents)
    test_fridge.fill_container()
    print(test_fridge.contents)
    test_fridge.reset()

def test_staples():
    test_fridge = Container('test')
    print(test_fridge.staples)
    test_fridge.define_staples()
    print(test_fridge.staples)
    response = get_input('Reset staple foods?')
    if response:
        for food_name in test_fridge.staples:
            food = Food(food_name)
            food.reset()
    test_fridge.reset()

def fill_fridge():
    fridge = Container('JM')
    #fridge.fill_container()
    print(fridge)
    backup_json()
    
def print_fridge():
    fridge = Container('fridge')
    #fridge.fill_container()
    print('Printing Fridge')
    print(fridge)

def update_fridge():
    fridge = Container('JM')
    fridge.update()

def rename_fridge():
    JM_fridge = Container('JM')
    print(JM_fridge.__dict__)
    JM_fridge.rename('fridge')
    print(JM_fridge.__dict__)

def create_spice_rack():
    #spice_rack = 
    pass

def delete_fridge():
    fridge = Container('JM')
    fridge.reset()

def move_foods(source_number):
    fridge = Container('fridge')
    spice_rack = Container('spice_rack')
    freezer = Container('freezer')
    pantry = Container('pantry')
    countertop = Container('countertop')
    choice_dict = {'1' : fridge,
                   '2' : freezer,
                   '3' : pantry,
                   '4' : spice_rack,
                   '5' : countertop}
    source = choice_dict[source_number]
    print('Moving stuff from ' + choice_dict[source_number].name + '.')
    print('Fridge = 1')
    print('Freezer = 2')
    print('Pantry = 3')
    print('Spice Rack = 4')
    print('Countertop = 5')
    def get_choice():
        choice = input()
        if choice == '':
            return source_number
        elif choice in ['1','2','3','4','5']:
            return choice
        else:
            print('Invalid entry, try again.')
            return get_choice()
    source_contents = {}
    for key in source.contents:
        source_contents[key] = source.contents[key]
    for id in source_contents:
        print('Where do you want : ' + source.contents[id]['food_name'] + '?')
        choice = get_choice()
        if choice == source_number:
            continue
        else:
            source.transfer_food(choice_dict[choice], id)
    print('Food is now in following containers:')
    input('Continue')
    print(fridge)
    input('Continue')
    print(freezer)
    input('Continue')
    print(pantry)
    input('Continue')
    print(spice_rack)
    input('Continue')
    print(countertop)

#test_fill()
#test_staples()
#fill_fridge()
#print_fridge()
#backup_json()
#update_fridge()
#rename_fridge()
#delete_fridge()
move_foods('3')
#print_fridge()
