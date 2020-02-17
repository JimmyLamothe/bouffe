from Container import Container

fridge = Container('fridge')
freezer = Container('freezer')
pantry = Container('pantry')
spice_rack = Container('spice rack')
countertop = Container('countertop')

JM = {'1' : fridge,
      '2' : freezer,
      '3' : pantry,
      '4' : spice_rack,
      '5' : countertop}

def print_house(container_dict):
    print('Container:')
    for key in container_dict:
        print(key + ' : ' + container_dict[key].name)

def eat():
    print_house(JM)
    def get_next():
        print('Type name of food to eat')
        food_name = input()
        if not food_name:
            return None
        print('Where did you get it from?')
        def get_choice():
            choice = input()
            if choice in ['1','2','3','4','5']:
                return choice
            else:
                print('Invalid entry, try again.')
                return get_choice()
        choice = get_choice()
        if choice:
            JM[choice].remove_food_by_name(food_name)
        return choice
    while get_next():
        get_next()

eat()
