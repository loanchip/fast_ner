import pandas as pd
import pickle
from os import walk

from fast_ner.utils.string_handling import string_cleaning

def insert_entity(dict_, entity):
    clean_entity = string_cleaning(entity)
    length = len(clean_entity)
    count = 0
    current_dict = dict_
    
    for word in clean_entity:
        if word in current_dict:
            current_dict = current_dict[word]
            count += 1
        else: break
    
    if count == length: 
        current_dict[1] = 1
    else:
        loc = length-1 # last word
        
        if count == loc: # only one word left
            current_dict[clean_entity[loc]] = {1:1}
        else:
            old_dict = {}
            old_dict[clean_entity[loc]] = {1:1}
            loc -= 1
            while(count<loc):
                new_dict = {}
                new_dict[clean_entity[loc]] = old_dict
                old_dict = new_dict
                loc -= 1
            current_dict[clean_entity[loc]] = old_dict
    
    return dict_

def create_dict_from_csv(entity_name=None):
    if entity_name:
        data = pd.read_csv('fast_ner/data/'+entity_name+'.csv')
        dict_ = {}
        for entity in data.item:
            dict_ = insert_entity(dict_, entity)
        with open('fast_ner/data/'+entity_name+'.pickle', 'wb') as handle:
            pickle.dump(dict_, handle)
    else:
        files_list = [files_list for _,_,files_list in walk(top='fast_ner/data/')][0]
        for file_name in files_list:
            if file_name[-4:] == '.csv':
                entity_name = file_name[:-4]
                data = pd.read_csv('fast_ner/data/'+entity_name+'.csv')
                dict_ = {}
                for entity in data.item:
                    dict_ = insert_entity(dict_, entity)
                with open('fast_ner/data/'+entity_name+'.pickle', 'wb') as handle:
                    pickle.dump(dict_, handle)

def load_entities(selected_entities=None, from_pickle=False, from_csv=False):
    entity_data = {}

    if from_pickle:
        if selected_entities:
            for entity in selected_entities:
                with open('fast_ner/data/'+entity+'.pickle', 'rb') as handle:
                    entity_data[entity] = pickle.load(handle)
        else: # load all available entities
            files_list = [files_list for _,_,files_list in walk(top='fast_ner/data/')][0]
            for file_name in files_list:
                if file_name[-7:] == '.pickle':
                    entity = file_name[:-7]
                    with open('fast_ner/data/'+entity+'.pickle', 'rb') as handle:
                        entity_data[entity] = pickle.load(handle)
    
    elif from_csv:
        if selected_entities:
            for entity in selected_entities:
                with open('fast_ner/data/'+entity+'.csv', 'rb') as handle:
                    entity_data[entity] = list(pd.read_csv(handle)['item'])
        else: # load all available entities
            files_list = [files_list for _,_,files_list in walk(top='fast_ner/data/')][0]
            for file_name in files_list:
                if file_name[-4:] == '.csv':
                    entity = file_name[:-4]
                    with open('fast_ner/data/'+entity+'.csv', 'rb') as handle:
                        entity_data[entity] = list(pd.read_csv(handle)['item'])

    return entity_data
