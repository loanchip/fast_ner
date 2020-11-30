''' 
Test pickle data
'''
from fast_ner.utils.entity_handling import load_entities

def show_all_keys():
    data = load_entities(from_pickle=True)
    print(data.keys())

def check_entity(key):
    data = load_entities(from_pickle=True)
    if key in data['movies']: print(data['movies'][key])
    else: print('key does not exist in data')

data = load_entities(from_pickle=True)
print(data.keys())
print(data['movies']['naruto'])