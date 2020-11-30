''' Exact + Fuzzy matching
Testing for single word movie titles, multi-word movie titles 
and titles with special characters
'''
from fast_ner.ner import add_new_entity, load_dict_data, load_csv_data, perform_ner
from tests.check_output import check_output

def main():
    #add_new_entity(entity_name='movies')
    data = load_dict_data(selected_entities=['movies'])
    csv_data = load_csv_data(selected_entities=['movies'])
    input_string='I would like to watch Travel Mates 2 or Marc Maron: Too Real right now.'
    expected_output = "{'movies': [(['travel', 'mates', '2'], 5, 8), (['marc', 'maron', 'too', 'real'], 9, 13)], 'fuzzy_matches': {'movies': [('Marc Maron: Too Real', 0.569703524874188), ('Travel Mates 2', 0.43260186577568377)]}}"
    
    output = perform_ner(input_data=input_string, entity_data=data, fuzzy_matching=True, csv_data=csv_data)

    print('Input: ' + input_string)
    print('Fuzzy Detected Entities:')
    print(output)
    check_output(str(output),expected_output)

if __name__ == "__main__":
    main()