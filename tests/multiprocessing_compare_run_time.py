import time
import multiprocessing
import pandas as pd
import random
import json
from fast_ner.ner import load_csv_data
from tests.fast_ner_test import fast_ner_test, fast_ner_test_big_data
from tests.regex_test import regex_test, regex_test_big_data
from tests.flashtext_test import flashtext_test, flashtext_test_big_data
    
def fast_ner(csv_data, queries, total_runs):
    start_time = time.time()
    processes = []
    for _ in range(total_runs):
        p = multiprocessing.Process(target=fast_ner_test_big_data, args=(csv_data, queries))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()
    stop_time = time.time()
    time_taken = stop_time - start_time
    return time_taken

def flashtext(csv_data, queries, total_runs):
    start_time = time.time()
    processes = []
    for _ in range(total_runs):
        p = multiprocessing.Process(target=flashtext_test_big_data, args=(csv_data, queries))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()
    stop_time = time.time()
    time_taken = stop_time - start_time
    return time_taken

def regex(csv_data, queries, total_runs):
    start_time = time.time()
    processes = []
    for _ in range(total_runs):
        p = multiprocessing.Process(target=regex_test_big_data, args=(csv_data, queries))
        processes.append(p)
        p.start()
    for process in processes:
        process.join()
    stop_time = time.time()
    time_taken = stop_time - start_time
    return time_taken

def perform_test(total_runs, show_output):
    print('Single Query Test: ')
    print('Single input query parsed for a single type of entity (movies)')
    csv_data = load_csv_data(selected_entities=['movies'])

    print()

    # fast_ner
    print('Running fast_ner')
    start_time = time.time()
    for _ in range(total_runs):
        fast_ner_test(csv_data)
    stop_time = time.time()
    time_fast_ner = stop_time - start_time
    avg_time_fast_ner = time_fast_ner / total_runs
    
    # flashtext
    print('Running flashtext')
    start_time = time.time()
    for _ in range(total_runs):
        flashtext_test(csv_data)
    stop_time = time.time()
    time_flashtext = stop_time - start_time
    avg_time_flashtext = time_flashtext / total_runs

    # regex - disabled - takes too long to run
    print('Running regex')
    # reducing the total number of runs for regex because it takes a long time to run
    total_runs = total_runs // 10
    start_time = time.time()
    for _ in range(total_runs):
        regex_test(csv_data)
    stop_time = time.time()
    time_regex = stop_time - start_time
    avg_time_regex = time_regex / total_runs
    total_runs = total_runs * 10

    print()
    print('Total Time for '+str(total_runs)+' runs of fast_ner (s): '+str(time_fast_ner))
    print('Total Time for '+str(total_runs)+' runs of flashtext (s): '+str(time_flashtext))
    print('Total Time for regex (s): '+str(time_regex))
    print()
    print('Average Time for fast_ner (s): '+str(avg_time_fast_ner))
    print('Average Time for flashtext (s): '+str(avg_time_flashtext))
    print('Average Time for regex (s): '+str(avg_time_regex))
    print()
    print('Percent boost using fast_ner vs regex: fast_ner is '
        +str(round(avg_time_regex/avg_time_fast_ner,2)) + ' times faster than regex')
    print('Percent boost using fast_ner vs flashtext: fast_ner is '
        +str(round(avg_time_flashtext/avg_time_fast_ner,2)) + ' times faster than flashtext')
    print()

    if show_output:
        print(' ******   Sample Outputs   ****** ')
    
        print(' -----   INPUT   ----- ')
        print('Have you watched Naruto or Naruto Shippuden : Blood Prison?')
        print(' -----   OUTPUT   ----- ')
        print('fast_ner:')
        print(json.dumps(fast_ner_test(csv_data, return_output=True), indent=2))
        print('flashtext:')
        print(flashtext_test(csv_data, return_output=True))
        print('regex:')
        print(regex_test(csv_data, return_output=True))

def perform_big_data_test(total_runs, sample_count):
    print('Big Data Test: (multiprocessing)')
    print('Parsing multiple queries for multiple types of entities.')
    print()
    
    csv_data = load_csv_data()
    input_data = pd.read_csv('tests/input_sentences.csv')
    queries = []
    for query in input_data.item:
            queries.append(query)
    number_of_queries = len(queries)

    print('Total Number of queries to process: '+str(number_of_queries))
    print('Total Number of entity types: '+str(len(csv_data)))
    print('Entity Types: ')
    print(list(csv_data.keys()))
    print()

    # fast_ner
    print('Running fast_ner')
    time_fast_ner = fast_ner(csv_data=csv_data, queries=queries, total_runs=total_runs)
    avg_time_fast_ner = time_fast_ner / total_runs
    
    # flashtext
    print('Running flashtext')
    time_flashtext = flashtext(csv_data=csv_data, queries=queries, total_runs=total_runs)
    avg_time_flashtext = time_flashtext / total_runs

    # regex - disabled - takes too long to run
    #print('Running regex')
    # reducing the total number of runs for regex because it takes a long time to run
    #time_regex = regex(csv_data=csv_data, queries=queries, total_runs=1)
    #avg_time_regex = time_regex
    
    print()
    print('Total Time for '+str(total_runs)+' runs of fast_ner (s): '+str(time_fast_ner))
    print('Total Time for '+str(total_runs)+' runs of flashtext (s): '+str(time_flashtext))
    #print('Total Time for regex (s): '+str(time_regex))
    print()
    print('Average Time for fast_ner (s): '+str(avg_time_fast_ner))
    print('Average Time for flashtext (s): '+str(avg_time_flashtext))
    #print('Average Time for regex (s): '+str(avg_time_regex))
    print()
    #print('Percent boost using fast_ner vs regex: fast_ner is '
    #    +str(round(avg_time_regex/avg_time_fast_ner,2)) + ' times faster than regex')
    print('Percent boost using fast_ner vs flashtext: fast_ner is '
        +str(round(avg_time_flashtext/avg_time_fast_ner,2)) + ' times faster than flashtext')
    print()

    # sample outputs
    sample_queries = random.sample(range(number_of_queries), k=sample_count)
    sample_queries = [queries[i] for i in sample_queries]
    fast_ner_outputs = fast_ner_test_big_data(data=csv_data,queries=sample_queries,return_output=True)
    flashtext_outputs = flashtext_test_big_data(data=csv_data,queries=sample_queries,return_output=True)
    print(' ******   Sample Outputs   ****** ')
    for i in range(sample_count):
        print(' -----   INPUT '+str(i+1)+'   ----- ')
        print(sample_queries[i])
        print(' -----   OUTPUT '+str(i+1)+'   ----- ')
        print('fast_ner:')
        print(json.dumps(fast_ner_outputs[i], indent=2))
        print('flashtext:')
        print(flashtext_outputs[i])

if __name__ == '__main__':
    total_runs = 100
    big_data_test = False
    show_sample_outputs = 1

    if big_data_test: perform_big_data_test(total_runs=total_runs, sample_count=show_sample_outputs)
    else: perform_test(total_runs=total_runs, show_output=show_sample_outputs)

    