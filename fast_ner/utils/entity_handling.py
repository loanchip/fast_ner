import pandas as pd
import pickle
from os import walk

from . string_handling import string_cleaning

def insert_entity(dict_, entity):
    """Inserts a new entity value into a dictionary.

    Finds the appropriate dictionary in the nested dictionary
    structure and inserts the new entity value.

    Args:
        dict_: A nested dictionary containing all previously inserted
            entity values
        entity: A string of the new entity value that needs to be 
            inserted into the exsisting dictionary.

    Returns:
        A dictionary mapping the first word of entity values to the 
        remaining words of the same entity values. Values are dictionary 
        of dictionaries. 
        
        {
            'comedy': {
                'action': {1:1},
                'drama': {1:1},
                1:1
                },
            'action': {
                'thriller': {1:1}
                1:1
                },
            'suspense': {1:1}
            }
        }

        If the entity exists in the dictionary, skips the process.
    """
    clean_entity = string_cleaning(entity)
    length = len(clean_entity)
    count = 0 # keeps track of the cursor
    current_dict = dict_
    
    # checks how much of the new entity already exists in the dictionary
    for word in clean_entity:
        if word in current_dict:
            current_dict = current_dict[word]
            count += 1
        else: break
    
    # based on how much part of the new entity is missing, insert the remaining
    # words in the appropriate dictionary (depth)
    if count == length: 
        current_dict[1] = 1
    else:
        loc = length-1 # last word of new entity
        
        if count == loc: # only one word left
            current_dict[clean_entity[loc]] = {1:1}
        else: # create dictionary of dictionary repeatedly until cursor position is reached
            old_dict = {}
            old_dict[clean_entity[loc]] = {1:1}
            loc -= 1
            while(count<loc):
                new_dict = {}
                new_dict[clean_entity[loc]] = old_dict
                old_dict = new_dict
                loc -= 1
            # merge the created dictionary of dictionary to the main dictionary at appropriate depth
            current_dict[clean_entity[loc]] = old_dict
    
    return dict_

def create_dict_from_csv(entity_name=None, path_to_data_folder=None):
    """Creates a dictionary .pickle file from .csv file of the specified entity.

    Based on the given entity name, loads up the respective .csv file
    from storage and generates a dictionary. Saves this dictionary
    to a corresponding .pickle file.

    Args:
        entity_name: A string specifying the entity name for which.
            the dictionary needs to be generated. Default is generate .pickle
            files for all available entity .csv files.
        path_to_data_folder: A string specifying the absolute path to 
            the data folder that contains the entity dataset files. The created 
            dictionary (.pickle) file will be stored in the same folder.
            By default, uses the built-in entity datasets.

    Writes:
        A .pickle file containing a dictionary mapping first word of entity values
        to the remaining words of the same entity values. Values are dictionary 
        of dictionaries. 
        
        {
            'comedy': {
                'action': {1:1},
                'drama': {1:1},
                1:1
                },
            'action': {
                'thriller': {1:1}
                1:1
                },
            'suspense': {1:1}
            }
        }

        If a .csv file corresponding to the given entity name is not found
        in storage, throws error.
    """
    if path_to_data_folder: path = path_to_data_folder
    else: path = 'fast_ner/data/'

    if entity_name:
        data = pd.read_csv(path+entity_name+'.csv')
        dict_ = {}
        # insert all entity values of the particular entity type into the dictionary
        for entity in data.item:
            dict_ = insert_entity(dict_, entity)
        # save the dictionary to a .pickle file
        with open(path+entity_name+'.pickle', 'wb') as handle:
            pickle.dump(dict_, handle)
    else:
        files_list = [files_list for _,_,files_list in walk(top=path)][0]
        # get all available entity types
        for file_name in files_list:
            if file_name[-4:] == '.csv':
                entity_name = file_name[:-4]
                data = pd.read_csv(path+entity_name+'.csv')
                dict_ = {}
                # insert all entity values of the particular entity type into the dictionary
                for entity in data.item:
                    dict_ = insert_entity(dict_, entity)
                # save the dictionary to a .pickle file
                with open(path+entity_name+'.pickle', 'wb') as handle:
                    pickle.dump(dict_, handle)

def load_entities(selected_entities=None, from_pickle=False, from_csv=False, 
                    path_to_data_folder=None):
    """Loads up data from selected .pickle or .csv files.

    Based on the selected entities, loads data from storage,
    into memory, if respective files exists.

    Args:
        selected_entities: A list of string entity names to be loaded.
            Default is load all available entitites.
        from_pickle: If True, loads data from .pickle files
            of selected entities.
        from_csv: If True, loads data from .csv files
            of selected entities.
        path_to_data_folder: A string specifying the absolute path to 
            the data folder that contains the entity dataset files.
            By default, uses the built-in entity datasets.

    Returns:
        A dictionary mapping entity type (key) to all entity values of 
        that type. Values are dictionary of dictionaries if data was loaded 
        from .pickle files. 
        
        {
            'genre': {
                'comedy': {
                    'action': {1:1},
                    'drama': {1:1}
                    },
                'action': {
                    'thriller': {1:1}
                    }
                }
        }

        If data was loaded from .csv files, values are a list of valid 
        entity values.

        {'genre': ['comedy action', 'comedy drama', 'action thriller']}

        Note: Use (only) one of the following in addition to selected entities,
        in each function call:
            --> from_pickle=True
            --> from_csv=True

        Always returns a dictionary. If no arguments are passed,
        returns an empty dictionary.
    """
    entity_data = {}

    if path_to_data_folder: path = path_to_data_folder
    else: path = 'fast_ner/data/'

    if from_pickle:
        if selected_entities:
            for entity in selected_entities:
                with open(path+entity+'.pickle', 'rb') as handle:
                    entity_data[entity] = pickle.load(handle)
        else: # load all available entities
            files_list = [files_list for _,_,files_list in walk(top=path)][0]
            for file_name in files_list:
                if file_name[-7:] == '.pickle':
                    entity = file_name[:-7]
                    with open(path+entity+'.pickle', 'rb') as handle:
                        entity_data[entity] = pickle.load(handle)
    
    elif from_csv:
        if selected_entities:
            for entity in selected_entities:
                with open(path+entity+'.csv', 'rb') as handle:
                    entity_data[entity] = list(pd.read_csv(handle)['item'])
        else: # load all available entities
            files_list = [files_list for _,_,files_list in walk(top=path)][0]
            for file_name in files_list:
                if file_name[-4:] == '.csv':
                    entity = file_name[:-4]
                    with open(path+entity+'.csv', 'rb') as handle:
                        entity_data[entity] = list(pd.read_csv(handle)['item'])

    return entity_data
