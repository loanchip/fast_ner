from fast_ner.utils.entity_handling import create_dict_from_csv, load_entities
from fast_ner.utils.string_handling import string_cleaning

def add_new_entity(entity_name):
    create_dict_from_csv(entity_name)

def load_data(selected_entities=None):
    return load_entities(selected_entities=selected_entities)

def extract_entities(input_data_tokens, entity_dict):
    detected_entities = []
    length = len(input_data_tokens)
    for i,word in enumerate(input_data_tokens):
        if word in entity_dict:
            start = i
            stop = -1
            loc = i
            current_dict = entity_dict
            
            while(loc<length and current_dict):
                if 1 in current_dict:
                    stop = loc
                    break
                if input_data_tokens[loc] not in current_dict: break
                current_dict = current_dict[input_data_tokens[loc]]
                loc += 1

            if stop != -1: detected_entities.append((input_data_tokens[start:stop], start, stop))

    return detected_entities

def perform_ner(input_data, entity_data={}):
    entities = list(entity_data.keys())
    input_data_tokens = string_cleaning(input_data)

    ner_data = {}
    
    for entity in entities:
        detected_entities = extract_entities(input_data_tokens=input_data_tokens,entity_dict=entity_data[entity])
        if detected_entities: ner_data[entity] = detected_entities

    return ner_data
