from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fast_ner.utils.entity_handling import create_dict_from_csv, load_entities
from fast_ner.utils.string_handling import string_cleaning

def add_new_entity(entity_name=None, path_to_data_folder=None):
    """Creates a dictionary .pickle file from .csv file of the specified entity.

    Based on the given entity name, loads up the respective .csv file
    from storage and generates a dictionary. Saves this dictionary
    to a corresponding .pickle file.

    Args:
        entity_name: A string specifying the entity name for which.
            the dictionary needs to be generated. Default is generate .pickle
            files for all available entity .csv files.
        path_to_data_folder: A string specifying the absolute path to 
            the data folder that contains the entity dataset files.
            By default, uses the built-in entity datasets.

    Writes:
        A .pickle file containing a dictionary mapping first word of entity values
        to the remaining words of the same entity values. Values are dictionary 
        of dictionaries. 
        
        {
            'comedy': {
                'action': {1:1},
                'drama': {1:1},
                1:1
                },
            'action': {
                'thriller': {1:1}
                1:1
                },
            'suspense': {1:1}
            }
        }

        If a .csv file corresponding to the given entity name is not found
        in storage, throws error.
    """
    create_dict_from_csv(entity_name=entity_name, path_to_data_folder=path_to_data_folder)

def load_dict_data(selected_entities=None, path_to_data_folder=None):
    """Loads up data from .pickle file for the selected entities.

    Based on the selected entities, loads data from storage,
    into memory, if respective files exists.

    Args:
        selected_entities: A list of string entity names to be loaded.
            Default is load all available entitites.
        path_to_data_folder: A string specifying the absolute path to 
            the data folder that contains the entity dataset files.
            By default, uses the built-in entity datasets.

    Returns:
        A dictionary mapping entity type (key) to all entity values of 
        that type. Values are dictionary of dictionaries. 
        
        {
            'genre': {
                'comedy': {
                    'action': {1:1},
                    'drama': {1:1}
                    },
                'action': {
                    'thriller': {1:1}
                    }
                }
        }

        Always returns a dictionary. If .pickle files of selected entitites 
        are not found, or if no .pickle files are found, returns an empty 
        dictionary.
    """
    return load_entities(selected_entities=selected_entities, from_pickle=True,
                            path_to_data_folder=path_to_data_folder)

def load_csv_data(selected_entities=None, path_to_data_folder=None):
    """Loads up data from .csv file for the selected entities.

    Based on the selected entities, loads data from storage,
    into memory, if respective files exists.

    Args:
        selected_entities: A list of string entity names to be loaded.
            Default is load all available entitites.
        path_to_data_folder: A string specifying the absolute path to 
            the data folder that contains the entity dataset files.
            By default, uses the built-in entity datasets.

    Returns:
        A dictionary mapping entity type (key) to all entity values of 
        that type. Values are a list of valid entity values.

        {'genre': ['comedy action', 'comedy drama', 'action thriller']}

        Always returns a dictionary. If .csv files of selected entitites 
        are not found, or if no .csv files are found, returns an empty 
        dictionary.
    """
    return load_entities(selected_entities=selected_entities, from_csv=True, 
                            path_to_data_folder=path_to_data_folder)

def extract_entities(input_data_tokens, entity_dict):
    """Extracts valid entities present in the input query.

    Parses the tokenized input list to find valid entity values, based 
    on the given entity dataset.

    Args:
        input_data_tokens: A list of string tokens, without any punctuation,
            based on the input string.
        entity_dict: A dictionary of dictionary, of entity values for a 
            particular entity type.

    Returns:
        A list of valid entity values and their start, stop token index 
        locations in the tokenized input query.

        [(['comedy', 'action'], 5, 7), (['suspense'], 9, 10)]

        Always returns a list. If no valid entities are detected, returns 
        an empty list.
    """
    detected_entities = []
    length = len(input_data_tokens)
    for i,word in enumerate(input_data_tokens):
        if word in entity_dict:
            start = i
            stop = -1
            loc = i # keeps track of the current cursor posiiton
            current_dict = entity_dict # keeps track of the current dictionary data
            
            while(loc<=length and current_dict):
                if 1 in current_dict:
                    stop = loc # tags index of a potential entity value if a longer entity is not present
                    if len(current_dict) == 1:
                        detected_entities.append((input_data_tokens[start:stop], start, stop))
                        stop = -1 #reset

                # if end of query reached or mismatch in entity values, discard and move on to the next word
                if loc == length or input_data_tokens[loc] not in current_dict: 
                    # save a shorter entity, if it exists in the already parsed query
                    if stop != -1: detected_entities.append((input_data_tokens[start:stop], start, stop))
                    break
                else:
                    # entity matches up until current word, continue
                    current_dict = current_dict[input_data_tokens[loc]]
                    loc += 1

    return detected_entities

def perform_fuzzy_matching(input_data, entity_list):
    """Performs fuzzing matching of entities in the input_data.

    Parses the given input stirng to find fuzzy matches of valid entity values, 
    based on the entity dataset. Used TFIDF vectorization and cosine 
    similarity index to calculate the fuzzy matches.

    Args:
        input_data: A string of input query to be parsed.
        entity_list: A list containing valid entity values for a particular
            entity type.

    Returns:
        A list of tuples, each tuple containing a valid entity value that 
        matched with the input string (more than the threshold value), and
        the confidence score of the match.

        [('comedy action', 0.5864945177714063), ('suspense', 0.4566449597381272)]

        Always returns a list. If no valid entities are detected, returns 
        an empty list.
    """
    detected_entities = []

    # adding entity and input query data to the corpus
    corpus = entity_list[:]
    corpus.append(input_data)

    # perform TFIDF vectorization on the corpus
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(corpus)

    # calculate the similarity index between the input query and all valie entitiy values
    similarity_index = cosine_similarity(tfidf[-1], tfidf)[0][:-1]

    threshold = 0.75 * max(similarity_index)

    # store each valid entity value that has a confidence score higher than the threshold value
    for i,similarity in enumerate(similarity_index):
        if(similarity > threshold and similarity > 0):
            detected_entities.append((corpus[i], similarity))

    return detected_entities

def perform_ner(input_data, entity_data, fuzzy_matching=False, csv_data=None):
    """Parses input query to search for named entities.

    Parses the given input stirng to find valid entity values, based 
    on the entity dataset.

    Args:
        input_data: A string of input query to be parsed.
        entity_data: A dictionary of dictionary, of entity values for multiple 
            entity types.
        fuzzy_matching: If True, performs fuzzy matching of entities based 
            on TFIDF and cosine_similarity. Default is False.
        csv_data: A dictionary of lists, containing entity values for multiple
            entity types.

    Returns:
        A dictionary mapping entity type (key) to all valid entity values 
        present in the input query of that type. Each value is a tuple of valid 
        entity value and its start, stop token index locations in the input query.

        {
            'genre': [
                (['comedy', 'action'], 5, 7), 
                (['suspense'], 9, 10)
            ],
            'review': [
                (['positive'], 1, 2)
            ]
        }

        Always returns a dictionary. If no valid entities are detected, returns 
        an empty dictionary.
    """
    input_data_tokens = string_cleaning(input_data)
    ner_data = {}
    
    # perform extraction of entities on the input query for each entity type
    for entity in entity_data:
        detected_entities = extract_entities(input_data_tokens=input_data_tokens,entity_dict=entity_data[entity])
        if detected_entities: ner_data[entity] = detected_entities

    if fuzzy_matching:
        if not csv_data: 
            print('csv_data required for fuzzy matching')
        else:
            fuzzy_matches = {}
            # perform extraction of entities on the input query for each entity type
            for entity in csv_data:
                detected_entities = perform_fuzzy_matching(input_data=input_data, entity_list=csv_data[entity])
                if detected_entities: fuzzy_matches[entity] = detected_entities
            ner_data['fuzzy_matches'] = fuzzy_matches

    return ner_data
