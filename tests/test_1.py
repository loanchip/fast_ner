''' Exact matching
Testing for single word movie titles, multi-word movie titles 
and titles with special characters
'''
from fast_ner.ner import add_new_entity, load_dict_data, perform_ner
from tests.check_output import check_output

def main():
    #add_new_entity(entity_name='movies') # refresh data
    data = load_dict_data()
    input_string = 'I would like to watch Travel Mates 2, Circle or Marc Maron: Too Real right now.'
    expected_output = "{'movies': [(['travel', 'mates', '2'], 5, 8), (['circle'], 8, 9), (['marc', 'maron', 'too', 'real'], 10, 14)]}"
    
    output = perform_ner(input_data=input_string,entity_data=data)

    print('Input: ' + input_string)
    print('Detected Entities:')
    print(output)
    check_output(str(output),expected_output)

if __name__ == "__main__":
    main()