''' Exact + Fuzzy matching
Testing for movie titles with shorter and longer names for movies 
in the same series
'''
from fast_ner.ner import add_new_entity, load_dict_data, load_csv_data, perform_ner
from tests.check_output import check_output

def main():
    #add_new_entity(entity_name='movies')
    data = load_dict_data(selected_entities=['movies'])
    csv_data = load_csv_data(selected_entities=['movies'])
    input_string='Have you watched Naruto or Naruto Shippuden : Blood Prison?'
    expected_output = "{'movies': [(['naruto'], 3, 4), (['naruto'], 5, 6), (['naruto', 'shippuden', 'blood', 'prison'], 5, 9)], 'fuzzy_matches': {'movies': [('Naruto', 0.5864945177714063), ('Naruto Shippuden : Blood Prison', 0.7566449597381272)]}}"
    output = perform_ner(input_data=input_string, entity_data=data, fuzzy_matching=True, csv_data=csv_data)

    print('Input: ' + input_string)
    print('Fuzzy Detected Entities:')
    print(output)
    check_output(str(output),expected_output)

if __name__ == "__main__":
    main()