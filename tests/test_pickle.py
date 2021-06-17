'''
Test pickle data
'''
from os import walk
from fast_ner.utils.entity_handling import load_entities, create_dict_from_csv


def test_add_all_entities():
    # create .pickle files for all available entity data (.csv) files
    create_dict_from_csv()

    files_list = [
        files_list for _, _, files_list in walk(top='fast_ner/data/')
        ][0]
    csv_count, pickle_count = 0, 0
    for file_name in files_list:
        if file_name[-7:] == '.pickle':
            pickle_count += 1
        elif file_name[-4:] == '.csv':
            csv_count += 1

    assert(pickle_count == csv_count)


def test_add_new_entities():
    # create .pickle files for all available entity data (.csv) files
    create_dict_from_csv(
        entity_name='movies',
        path_to_data_folder='fast_ner/data/'
    )

    files_list = [
        files_list for _, _, files_list in walk(top='fast_ner/data/')
        ][0]
    csv_count, pickle_count = 0, 0
    for file_name in files_list:
        if file_name[-7:] == '.pickle':
            pickle_count += 1
        elif file_name[-4:] == '.csv':
            csv_count += 1

    assert(pickle_count == csv_count)


def test_csv_data():
    data = load_entities(
        from_csv=True,
        path_to_data_folder='fast_ner/data/'
    )

    assert(len(list(data.keys())) == 13)
    assert(len(data['movies']) == 4265)


def test_pickle_keys():
    data = load_entities(from_pickle=True)
    expected_keys = [
        'actor', 'character', 'director', 'genre', 'movies', 'plot', 'rating',
        'ratings_average', 'review', 'song', 'title', 'trailer', 'year'
    ]
    assert(sorted(list(data.keys())) == expected_keys)


def test_pickle_data():
    data = load_entities(from_pickle=True)
    expected_entity_data = {
        1: 1,
        'shippuden': {
            'blood': {
                'prison': {
                    1: 1
                }
            },
            'the': {
                'movie': {
                    'the': {
                        'lost': {
                            'tower': {
                                1: 1
                            }
                        }
                    },
                    1: 1
                }
            }
        },
        'shippûden': {
            'the': {
                'movie': {
                    'the': {
                        'will': {
                            'of': {
                                'fire': {
                                    1: 1
                                }
                            }
                        }
                    },
                    'bonds': {
                        1: 1
                    }
                }
            }
        },
        'the': {
            'movie': {
                '2': {
                    'legend': {
                        'of': {
                            'the': {
                                'stone': {
                                    'of': {
                                        'gelel': {
                                            1: 1
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                '3': {
                    'guardians': {
                        'of': {
                            'the': {
                                'crescent': {
                                    'moon': {
                                        'kingdom': {
                                            1: 1
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                'ninja': {
                    'clash': {
                        'in': {
                            'the': {
                                'land': {
                                    'of': {
                                        'snow': {
                                            1: 1
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    assert(data['movies']['naruto'] == expected_entity_data)


def main():
    test_add_all_entities()
    test_add_new_entities()
    test_csv_data()
    test_pickle_keys()
    test_pickle_data()


if __name__ == "__main__":
    main()
