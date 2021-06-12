from fast_ner.ner import add_new_entity, load_dict_data, load_csv_data
from fast_ner.ner import perform_ner


def test_exact_match():
    ''' Exact matching
    Testing for single word movie titles, multi-word movie titles
    and titles with special characters
    '''
    data = load_dict_data(selected_entities=['movies'])  # for exact matching

    input_string = ('I would like to watch Travel Mates 2, Circle or Marc '
                    'Maron: Too Real right now.')
    expected_output = {
        'movies': [
            (
                ['travel', 'mates', '2'], 5, 8
            ),
            (
                ['circle'], 8, 9
            ),
            (
                ['marc', 'maron', 'too', 'real'], 10, 14
            )
        ]
    }
    output = perform_ner(input_data=input_string, entity_data=data)

    assert(output == expected_output)


def test_fuzzy_match():
    ''' Exact + Fuzzy matching
    Testing for single word movie titles, multi-word movie titles
    and titles with special characters
    '''
    data = load_dict_data(selected_entities=['movies'])  # for exact matching
    csv_data = load_csv_data(
        selected_entities=['movies'])  # for fuzzy matching

    input_string = ('I would like to watch Travel Mates 2, Circle or Marc '
                    'Maron: Too Real right now.')
    expected_output = {
        'movies': [
            (
                ['travel', 'mates', '2'], 5, 8
            ),
            (
                ['circle'], 8, 9
            ),
            (
                ['marc', 'maron', 'too', 'real'], 10, 14
            )
        ],
        'fuzzy_matches':
        {
            'movies':
            [
                ('Marc Maron: Too Real', 0.55),
                ('Travel Mates 2', 0.41)
            ]
        }
    }
    output = perform_ner(input_data=input_string, entity_data=data,
                         fuzzy_matching=True, csv_data=csv_data)

    # rounding fuzzy match % to 2 decimals
    for key in output['fuzzy_matches'].keys():
        for idx, data in enumerate(output['fuzzy_matches'][key]):
            output['fuzzy_matches'][key][idx] = (data[0], round(data[1], 2))

    assert(output == expected_output)


def test_multiple_exact_match():
    ''' Exact matching
    Testing for movie titles with shorter and longer names for movies in the
    same series
    '''
    data = load_dict_data(selected_entities=['movies'])  # for exact matching

    input_string = ('Have you watched Naruto or Naruto Shippuden : Blood'
                    ' Prison?')
    expected_output = {
        'movies': [
            (
                ['naruto'], 3, 4
            ),
            (
                ['naruto', 'shippuden', 'blood', 'prison'], 5, 9
            )
        ]
    }
    output = perform_ner(input_data=input_string, entity_data=data)

    assert(output == expected_output)


def test_multiple_fuzzy_match():
    ''' Exact + Fuzzy matching
    Testing for movie titles with shorter and longer names for movies in the
    same series
    '''
    data = load_dict_data(selected_entities=['movies'])  # for exact matching
    csv_data = load_csv_data(
        selected_entities=['movies'])  # for fuzzy matching

    input_string = ('Have you watched Naruto or Naruto Shippuden : Blood'
                    ' Prison?')
    expected_output = {
        'movies': [
            (
                ['naruto'], 3, 4
            ),
            (
                ['naruto', 'shippuden', 'blood', 'prison'], 5, 9
            )
        ],
        'fuzzy_matches': {
            'movies': [
                ('Naruto', 0.59),
                ('Naruto Shippuden : Blood Prison', 0.76)
            ]
        }
    }
    output = perform_ner(input_data=input_string, entity_data=data,
                         fuzzy_matching=True, csv_data=csv_data)

    # rounding fuzzy match % to 2 decimals
    for key in output['fuzzy_matches'].keys():
        for idx, data in enumerate(output['fuzzy_matches'][key]):
            output['fuzzy_matches'][key][idx] = (data[0], round(data[1], 2))

    assert(output == expected_output)


def reload_data():
    ''' Reconstruct dictionary
    '''
    add_new_entity()


def main():
    reload_data()

    test_exact_match()
    test_fuzzy_match()
    test_multiple_exact_match()
    test_multiple_fuzzy_match()


if __name__ == "__main__":
    main()
