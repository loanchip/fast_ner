'''
Compare runtime of fast_ner with regex based approach and flashtext (SpaCy) for ner
'''
import timeit
import pandas as pd
from fast_ner.ner import load_csv_data
from tests.fast_ner_test import fast_ner_test, fast_ner_test_big_data
from tests.regex_test import regex_test, regex_test_big_data
from tests.flashtext_test import flashtext_test, flashtext_test_big_data

csv_data = load_csv_data(selected_entities=['movies'])
total_runs = 100
big_data_test = False

if not big_data_test:
        print('Regular Test:')
        print('Total runs: '+str(total_runs))

        print('Running fast_ner')
        total_time_fast_ner = timeit.timeit("fast_ner_test(data=csv_data)", globals=globals(), number=total_runs)

        print('Running flashtext')
        total_time_flashtext = timeit.timeit("flashtext_test(data=csv_data)", globals=globals(), number=total_runs)

        print('Running regex')
        total_time_regex = timeit.timeit("regex_test(data=csv_data)", globals=globals(), number=total_runs)

        avg_time_fast_ner = total_time_fast_ner / total_runs
        avg_time_flashtext = total_time_flashtext / total_runs
        avg_time_regex = total_time_regex / total_runs

        print('Total Time for fast_ner (s): '+str(total_time_fast_ner))
        print('Total Time for flashtext (s): '+str(total_time_flashtext))
        print('Total Time for regex (s): '+str(total_time_regex))

        print('Average Time for fast_ner (s): '+str(avg_time_fast_ner))
        print('Average Time for flashtext (s): '+str(avg_time_flashtext))
        print('Average Time for regex (s): '+str(avg_time_regex))

        print('Percent boost using fast_ner vs regex: fast_ner is '
                +str(round(avg_time_regex/avg_time_fast_ner,2)) + ' times faster than regex')
        print('Percent boost using fast_ner vs flashtext: fast_ner is '
                +str(round(avg_time_flashtext/avg_time_fast_ner,2)) + ' times faster than flashtext')

else:
        print('Big Data Test:')

        input_data = pd.read_csv('tests/input_sentences.csv')
        queries = []
        for query in input_data.item:
                queries.append(query)
        
        print('Running fast_ner')
        total_time_fast_ner = timeit.timeit("fast_ner_test_big_data(data=csv_data, queries=queries)", globals=globals(), number=total_runs)

        print('Running flashtext')
        total_time_flashtext = timeit.timeit("flashtext_test_big_data(data=csv_data, queries=queries)", globals=globals(), number=total_runs)

        #print('Running regex')
        #total_time_regex = timeit.timeit("regex_test_big_data(data=csv_data, queries=queries)", globals=globals(), number=total_runs)

        avg_time_fast_ner = total_time_fast_ner / total_runs
        avg_time_flashtext = total_time_flashtext / total_runs
        #avg_time_regex = total_time_regex / total_runs

        print('Total Time for fast_ner (s): '+str(total_time_fast_ner))
        print('Total Time for flashtext (s): '+str(total_time_flashtext))
        #print('Total Time for regex (s): '+str(total_time_regex))

        print('Average Time for fast_ner (s): '+str(avg_time_fast_ner))
        print('Average Time for flashtext (s): '+str(avg_time_flashtext))
        #print('Average Time for regex (s): '+str(avg_time_regex))

        #print('Percent boost using fast_ner vs regex: fast_ner is '
        #        +str(round(avg_time_regex/avg_time_fast_ner,2)) + ' times faster than regex')
        print('Percent boost using fast_ner vs flashtext: fast_ner is '
                +str(round(avg_time_flashtext/avg_time_fast_ner,2)) + ' times faster than flashtext')