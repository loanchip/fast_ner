from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fast_ner.utils.entity_handling import create_dict_from_csv, load_entities
from fast_ner.utils.string_handling import string_cleaning

def add_new_entity(entity_name):
    create_dict_from_csv(entity_name)

def load_dict_data(selected_entities=None):
    return load_entities(selected_entities=selected_entities, from_pickle=True)

def load_csv_data(selected_entities=None):
    return load_entities(selected_entities=selected_entities, from_csv=True)

def extract_entities(input_data_tokens, entity_dict):
    detected_entities = []
    length = len(input_data_tokens)
    for i,word in enumerate(input_data_tokens):
        if word in entity_dict:
            start = i
            stop = -1
            loc = i
            current_dict = entity_dict
            
            while(loc<=length and current_dict):
                if 1 in current_dict:
                    stop = loc
                    detected_entities.append((input_data_tokens[start:stop], start, stop))

                if loc == length or input_data_tokens[loc] not in current_dict: break
                else:
                    current_dict = current_dict[input_data_tokens[loc]]
                    loc += 1

    return detected_entities

def perform_fuzzy_matching(input_data, entity_list):
    detected_entities = []

    corpus = entity_list[:]
    corpus.append(input_data)
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(corpus)

    similarity_index = cosine_similarity(tfidf[-1], tfidf)[0][:-1]

    max_similarity = max(similarity_index)

    for i,similarity in enumerate(similarity_index):
        if(similarity > (0.75*max_similarity) and similarity > 0):
            detected_entities.append((corpus[i], similarity))

    return detected_entities

def perform_ner(input_data, entity_data={}, fuzzy_matching=False, csv_data={}):
    input_data_tokens = string_cleaning(input_data)
    ner_data = {}
    
    for entity in entity_data:
        detected_entities = extract_entities(input_data_tokens=input_data_tokens,entity_dict=entity_data[entity])
        if detected_entities: ner_data[entity] = detected_entities

    if fuzzy_matching:
        fuzzy_matches = {}
        for entity in entity_data:
            detected_entities = perform_fuzzy_matching(input_data=input_data, entity_list=csv_data[entity])
            if detected_entities: fuzzy_matches[entity] = detected_entities
        ner_data['fuzzy_matches'] = fuzzy_matches

    return ner_data
