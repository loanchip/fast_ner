from flashtext import KeywordProcessor
from fast_ner.utils.string_handling import string_cleaning
from fast_ner.ner import load_csv_data

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

def flashtext_test_big_data(data, queries, return_output=False):
    ''' Exact matching
    Testing for movie titles with shorter and longer names for movies in the same series
    '''
    outputs = []
    keyword_processor = KeywordProcessor()
    for entity_name in data:
        for entity in data[entity_name]:
            entity = ' '.join(string_cleaning(entity))
            keyword_processor.add_keyword(entity)
    
    for query in queries:
        query = ' '.join(string_cleaning(query))
        output = keyword_processor.extract_keywords(sentence=query, span_info=True)
        if return_output: outputs.append(output)

    if return_output: return outputs

def flashtext_test(data, return_output=False):
    ''' Exact matching
    Testing for movie titles with shorter and longer names for movies in the same series
    '''
    input_string='Have you watched Naruto or Naruto Shippuden : Blood Prison?'
    #expected_output = "{'movies': [[('naruto', 17, 23), ('naruto shippuden blood prison', 27, 56)]]}"
    output = perform_flashtext_ner(input_data=input_string,csv_data=data)
    #print(output)
    #assert(str(output) == expected_output)
    if return_output: return output

def main():
    csv_data = load_csv_data()
    flashtext_test(data=csv_data)

if __name__ == "__main__":
    main()