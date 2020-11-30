''' Exact matching
Testing for movie titles with shorter and longer names for movies 
in the same series
'''
from fast_ner.ner import add_new_entity, load_dict_data, perform_ner
from tests.check_output import check_output

def main():
    #add_new_entity(entity_name='movies') # refresh data
    data = load_dict_data()
    input_string='Have you watched Naruto or Naruto Shippuden : Blood Prison?'
    expected_output = "{'movies': [(['naruto'], 3, 4), (['naruto'], 5, 6), (['naruto', 'shippuden', 'blood', 'prison'], 5, 9)]}"

    output = perform_ner(input_data=input_string,entity_data=data)

    print('Input: ' + input_string)
    print('Detected Entities:')
    print(output)
    check_output(str(output),expected_output)

if __name__ == "__main__":
    main()