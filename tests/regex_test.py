import re
from fast_ner.utils.string_handling import string_cleaning
from fast_ner.ner import load_csv_data
from tests.check_output import check_output

def extract_entities(input_data, entity_list=[]):
    detected_entities = []
    #print(input_data)
    for entity in entity_list: # fix for special characters 
        entity = ' '.join(string_cleaning(entity))
        #print(entity)
        if '*' in entity: continue
        pattern = re.compile(rf"\b{entity}\b")
        detected = pattern.search(input_data)
        #print(detected)
        if detected: detected_entities.append((detected))
    
    return detected_entities

def perform_regex_ner(input_data, csv_data={}):
    input_data_tokens = string_cleaning(input_data)
    input_data = ' '.join(input_data_tokens)
    ner_data = {}
    
    for entity in csv_data:
        detected_entities = extract_entities(input_data=input_data, entity_list=csv_data[entity])
        if detected_entities: ner_data[entity] = detected_entities

    return ner_data

def regex_test_big_data(data, queries):
    ''' Exact matching
    Testing for movie titles with shorter and longer names for movies in the same series
    '''
    for query in queries:
        output = perform_regex_ner(input_data=query,csv_data=data)

def regex_test(data, return_output=False):
    ''' Exact matching
    Testing for movie titles with shorter and longer names for movies in the same series
    '''
    input_string='Have you watched Naruto or Naruto Shippuden : Blood Prison?'
    #expected_output = ("{'movies': [<re.Match object; span=(17, 23), match='naruto'>, "
    #                    "<re.Match object; span=(27, 56), match='naruto shippuden blood prison'>]}")
    output = perform_regex_ner(input_data=input_string,csv_data=data)
    #print(output)
    #print('Test: ',end='')
    #check_output(str(output), expected_output)
    if return_output: return output

def main():
    csv_data = load_csv_data()
    regex_test(data=csv_data)

if __name__ == "__main__":
    main()