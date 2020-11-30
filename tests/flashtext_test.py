from flashtext import KeywordProcessor
from fast_ner.utils.string_handling import string_cleaning
from fast_ner.ner import load_csv_data
from tests.check_output import check_output

def extract_entities(input_data, entity_list=[]):
    detected_entities = []
    keyword_processor = KeywordProcessor()
    for entity in entity_list:
        entity = ' '.join(string_cleaning(entity))
        keyword_processor.add_keyword(entity)
    
    detected = keyword_processor.extract_keywords(sentence=input_data, span_info=True)
    if detected: detected_entities.append((detected))
    return detected_entities

def perform_flashtext_ner(input_data, csv_data={}):
    input_data_tokens = string_cleaning(input_data)
    input_data = ' '.join(input_data_tokens)
    ner_data = {}

    for entity in csv_data:
        detected_entities = extract_entities(input_data=input_data, entity_list=csv_data[entity])
        if detected_entities: ner_data[entity] = detected_entities

    return ner_data

def flashtext_test(data):
    ''' Exact matching
    Testing for movie titles with shorter and longer names for movies in the same series
    '''
    input_string='Have you watched Naruto or Naruto Shippuden : Blood Prison?'
    expected_output = "{'movies': [[('naruto', 17, 23), ('naruto shippuden blood prison', 27, 56)]]}"
    output = perform_flashtext_ner(input_data=input_string,csv_data=data)
    #print(output)
    #print('Test: ',end='')
    #check_output(str(output), expected_output)

def main():
    csv_data = load_csv_data()
    flashtext_test(data=csv_data)

if __name__ == "__main__":
    main()