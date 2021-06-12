''' 
Test pickle data
'''
from fast_ner.utils.entity_handling import load_entities

def test_pickle_keys():
    data = load_entities(from_pickle=True)
    assert(str(data.keys()) == "dict_keys(['trailer', 'director', 'actor', 'ratings_average', 'review', 'rating', 'year', 'movies', 'character', 'genre', 'plot', 'title', 'song'])")

def test_pickle_data():
    data = load_entities(from_pickle=True)
    assert(str(data['movies']['naruto']) == "{1: 1, 'shippuden': {'blood': {'prison': {1: 1}}, 'the': {'movie': {'the': {'lost': {'tower': {1: 1}}}, 1: 1}}}, 'shippûden': {'the': {'movie': {'the': {'will': {'of': {'fire': {1: 1}}}}, 'bonds': {1: 1}}}}, 'the': {'movie': {'2': {'legend': {'of': {'the': {'stone': {'of': {'gelel': {1: 1}}}}}}}, '3': {'guardians': {'of': {'the': {'crescent': {'moon': {'kingdom': {1: 1}}}}}}}, 'ninja': {'clash': {'in': {'the': {'land': {'of': {'snow': {1: 1}}}}}}}}}}")