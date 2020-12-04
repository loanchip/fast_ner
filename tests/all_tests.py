from fast_ner.ner import add_new_entity, load_dict_data, load_csv_data, perform_ner
from tests.check_output import check_output

def test_1(data):
    ''' Exact matching
    Testing for single word movie titles, multi-word movie titles 
    and titles with special characters
    '''
    input_string = 'I would like to watch Travel Mates 2, Circle or Marc Maron: Too Real right now.'
    expected_output = ("{'movies': [(['travel', 'mates', '2'], 5, 8), "
                        "(['circle'], 8, 9), (['marc', 'maron', 'too', 'real'], 10, 14)]}")
    output = perform_ner(input_data=input_string,entity_data=data)
    print('Test 1: ',end='')
    check_output(str(output), expected_output)

def test_2(data, csv_data):
    ''' Exact + Fuzzy matching
    Testing for single word movie titles, multi-word movie titles 
    and titles with special characters
    '''
    input_string="I would like to watch Travel Mates 2, Circle or Marc Maron: Too Real right now."
    expected_output = ("{'movies': [(['travel', 'mates', '2'], 5, 8), "
                        "(['circle'], 8, 9), (['marc', 'maron', 'too', 'real'], 10, 14)], "
                        "'fuzzy_matches': {'movies': [('Marc Maron: Too Real', 0.5456128103461935), "
                        "('Travel Mates 2', 0.41430868766171436)]}}")
    output = perform_ner(input_data=input_string, entity_data=data, fuzzy_matching=True, csv_data=csv_data)
    print('Test 2: ',end='')
    check_output(str(output), expected_output)

def test_3(data):
    ''' Exact matching
    Testing for movie titles with shorter and longer names for movies in the same series
    '''
    input_string='Have you watched Naruto or Naruto Shippuden : Blood Prison?'
    expected_output = ("{'movies': [(['naruto'], 3, 4), "
                        "(['naruto', 'shippuden', 'blood', 'prison'], 5, 9)]}")
    output = perform_ner(input_data=input_string,entity_data=data)
    print('Test 3: ',end='')
    check_output(str(output), expected_output)

def test_4(data, csv_data):
    ''' Exact + Fuzzy matching
    Testing for movie titles with shorter and longer names for movies in the same series
    '''
    input_string='Have you watched Naruto or Naruto Shippuden : Blood Prison?'
    expected_output = ("{'movies': [(['naruto'], 3, 4), "
                        "(['naruto', 'shippuden', 'blood', 'prison'], 5, 9)], "
                        "'fuzzy_matches': {'movies': [('Naruto', 0.5864945177714063), "
                        "('Naruto Shippuden : Blood Prison', 0.7566449597381272)]}}")
    output = perform_ner(input_data=input_string, entity_data=data, fuzzy_matching=True, csv_data=csv_data)
    print('Test 4: ',end='')
    check_output(str(output), expected_output)

def reload_data():
    ''' Reconstruct dictionary
    '''
    add_new_entity()

def run_tests():
    ''' Load data and run all tests
    '''
    data = load_dict_data(selected_entities=['movies']) # for exact matching
    csv_data = load_csv_data(selected_entities=['movies']) # for fuzzy matching
    #data = load_dict_data() # to load all available entity data
    #csv_data = load_csv_data() # to load all available entity data
    
    test_1(data=data)
    test_2(data=data,csv_data=csv_data)
    test_3(data=data)
    test_4(data=data,csv_data=csv_data)

def main():
    reload_data()
    run_tests()

if __name__ == "__main__":
    main()