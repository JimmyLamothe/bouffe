from pathlib import Path
from Food import Food

json_path = Path('./json')

food_list = [x.stem for x in json_path.iterdir() if not x.stem[0] == '.']


def print_food_list():
    print(food_list)

def print_food_info():
    for stem in food_list:
        print('Processing: ' + stem)
        print(Food(stem))
