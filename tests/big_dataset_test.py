''' Exact matching
NER for all available entities on multiple input queries
'''
import pandas as pd
from fast_ner.ner import add_new_entity, load_dict_data, perform_ner
from tests.check_output import check_output

def main():
    #add_new_entity() # refresh data
    data = load_dict_data()
    input_data = pd.read_csv('tests/input_sentences.csv')
    queries = []
    for query in input_data.item:
        queries.append(query)
    
    for query in queries:    
        output = perform_ner(input_data=query,entity_data=data)
        print('Input: ' + query)
        print('Detected Entities:')
        print(output)

    #check_output(str(output),expected_output)

if __name__ == "__main__":
    main()