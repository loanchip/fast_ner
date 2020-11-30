'''
Compare runtime of fast_ner with regex based approach and flashtext (SpaCy) for ner
'''
import timeit
from fast_ner.ner import load_csv_data
from tests.fast_ner_test import fast_ner_test
from tests.regex_test import regex_test
from tests.flashtext_test import flashtext_test

csv_data = load_csv_data()
total_runs = 100

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

print('Percent boost using fast_ner vs regex: fast_ner is '+str(round(avg_time_regex/avg_time_fast_ner,2)) + ' times faster than regex')
print('Percent boost using fast_ner vs flashtext: fast_ner is '+str(round(avg_time_flashtext/avg_time_fast_ner,2)) + ' times faster than flashtext')
