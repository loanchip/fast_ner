import time
import pandas as pd
import re
import multiprocessing

from flashtext import KeywordProcessor

from fast_ner.ner import load_csv_data, perform_ner
from fast_ner.utils.entity_handling import insert_entity

def test_fast_ner(query_string, entity_data, show_output=False):
    start_time = time.time()
    entity_dict = {}
    for entity_name in entity_data:
        dict_ = {}
        for value in entity_data[entity_name]:
            dict_ = insert_entity(dict_=dict_,entity=value)
        entity_dict[entity_name] = dict_
    output = perform_ner(input_data=query_string, entity_data=entity_dict)
    stop_time = time.time()
    time_taken = stop_time - start_time
    if show_output: print(output)
    return time_taken

def test_flashtext(query_string, entity_data, show_output=False):
    start_time = time.time()
    detected_entities = {}
    for entity_name in entity_data:
        keyword_processor = KeywordProcessor()
        keyword_processor.add_keywords_from_list(entity_data[entity_name])
        output = keyword_processor.extract_keywords(sentence=query_string)
        if(output): detected_entities[entity_name] = output
    stop_time = time.time()
    time_taken = stop_time - start_time
    if show_output: print(output)
    return time_taken

def test_regex(query_string, entity_data, show_output=False):
    start_time = time.time()
    detected_entities = []
    for entity_name in entity_data:
        for value in entity_data[entity_name]:
            if '*' in value: continue # re.compile can't handle '*' in words pattern
            try:
                pattern = re.compile(rf"\b{value}\b")
            except:
                print('Error with re.compile for entity: ' + value)
            detected = pattern.search(query_string)
            if detected: detected_entities.append(detected)
    stop_time = time.time()
    time_taken = stop_time - start_time
    if show_output: print(detected_entities)
    return time_taken

def multiprocess_fast_ner(query_string, entity_data, runs_count=100, show_output=False):
    start_time = time.time()
    processes = []
    for _ in range(runs_count):
        p = multiprocessing.Process(target=test_fast_ner, args=(query_string, entity_data))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()
    stop_time = time.time()
    time_taken = stop_time - start_time
    return time_taken / runs_count

def multiprocess_flashtext(query_string, entity_data, runs_count=100, show_output=False):
    start_time = time.time()
    processes = []
    for _ in range(runs_count):
        p = multiprocessing.Process(target=test_flashtext, args=(query_string, entity_data))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()
    stop_time = time.time()
    time_taken = stop_time - start_time
    return time_taken / runs_count

def multiprocess_regex(query_string, entity_data, runs_count=10, show_output=False):
    start_time = time.time()
    processes = []
    for _ in range(runs_count):
        p = multiprocessing.Process(target=test_regex, args=(query_string, entity_data))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()
    stop_time = time.time()
    time_taken = stop_time - start_time
    return time_taken / runs_count

def print_query_data_stats(query_data):
    sentence_count = len(query_data)
    avg_word_count = sum([len(x.split()) for x in query_data['item']]) / sentence_count
    print(' '*2+'*'*15+' '*2+'INPUT QUERY STATS'+' '*2+'*'*15+' '*2)
    print('Total Number of Sentences: ' + str(sentence_count))
    print('Average Sentence length (words): '+str(round(avg_word_count,2)))
    print()

def print_entity_data_stats(csv_data):
    entity_count = len(csv_data)
    values_per_entity_count = [len(values) for values in csv_data.values()]
    print(' '*2+'*'*15+' '*2+'ENTITY DATA STATS'+' '*2+'*'*15+' '*2)
    print('Total Number of Entities: ' + str(entity_count))
    print('Count of valid entity values for each entity: ')
    print(values_per_entity_count)
    print()

def compare_test(query_data, csv_data, limited_data, multiprocessing_flag):
    word_count = []
    time_fast_ner = []
    time_flashtext = []
    time_regex = []

    length = len(query_data)
    
    if limited_data:
        start = 1
        stop = length
        inc = 100
    else:
        start = 25000
        stop = 100001
        inc = 5000
        full_query_data = ' '.join(query_data['item'][:])

    for size in range(start, stop, inc):
        if limited_data:
            query_string = ' '.join(query_data['item'][:size])
        else:
            start_c = len(full_query_data.split())      
            query_string = full_query_data
            
            add_c = (size - start_c) % start_c
            mul_c = (size - start_c) // start_c

            while mul_c != 0:
              query_string += ' ' + full_query_data + ' '
              mul_c -= 1
            
            query_string += ' ' + ' '.join(full_query_data.split()[:add_c])

        print(' '*2+'*'*15+' '*2+'TIME STATS'+' '*2+'*'*15+' '*2)
        word_count.append(len(query_string.split()))
        print('Query size (words): '+str(word_count[-1]))

        if multiprocessing_flag:
            time_fast_ner.append(multiprocess_fast_ner(query_string=query_string, entity_data=csv_data))
            print('fast_ner Time (s): '+str(time_fast_ner[-1]))

            time_flashtext.append(multiprocess_flashtext(query_string=query_string, entity_data=csv_data))
            print('flashtext Time (s): '+str(time_flashtext[-1]))

            # regex disabled - takes too long to process
            #time_regex.append(multiprocess_regex(query_string=query_string, entity_data=csv_data)
            #print('regex Time (s): '+str(time_regex[-1]))
            time_regex.append(0)

        else:
            time_fast_ner.append(test_fast_ner(query_string=query_string, entity_data=csv_data))
            print('fast_ner Time (s): '+str(time_fast_ner[-1]))
            
            time_flashtext.append(test_flashtext(query_string=query_string, entity_data=csv_data))
            print('flashtext Time (s): '+str(time_flashtext[-1]))
            
            time_regex.append(test_regex(query_string=query_string, entity_data=csv_data))
            print('regex Time (s): '+str(time_regex[-1]))
            
    data = {'word_count':word_count, 'time_fast_ner':time_fast_ner, 
            'time_flashtext':time_flashtext, 'time_regex':time_regex}
    results = pd.DataFrame(data=data)
    
    return results

def main():
    # Config
    limited_data = True # test for input query data upto 25k tokens
    # set false to test from 25k to 100k tokens
    multiprocessing_flag = True # set to False to disable multiprocessing
    # With multiprocessing enabled, tests each module 100 times for the same 
    # query to get an average time and avoid any fluctuations due to randomness.
    # With multiprocessing disabled, tests each module only once for a query
    # Expect response time fluctuations with multiple tests runs

    # Loading Data
    query_data = pd.read_csv('tests/data/input_sentences.csv')
    csv_data = load_csv_data()

    # Provide data details
    print_query_data_stats(query_data=query_data)
    print_entity_data_stats(csv_data=csv_data)

    # Run compare test
    results = compare_test(query_data, csv_data, limited_data, multiprocessing_flag)
    print(results)

    # Save results to file
    if limited_data: file_name = 'results_upto_25k.csv'
    else: file_name = 'results_over_25k.csv'
    results.to_csv('tests/results/'+file_name, index=False)

if __name__ == "__main__":
    main()