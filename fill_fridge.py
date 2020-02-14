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
    fridge = Container('JM')
    #fridge.fill_container()
    print(fridge)


#test_fill()
#test_staples()
#fill_fridge()
update_fridge()
print_fridge()
#backup_json()
