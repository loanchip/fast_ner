from fast_ner.ner import perform_ner, load_csv_data
from fast_ner.utils.entity_handling import insert_entity
from tests.check_output import check_output

def fast_ner_test_big_data(data, queries, return_output=False):
    mega_dict = {}
    outputs = []

    for entity_name in data:
        dict_ = {}
        for entity in data[entity_name]:
            dict_ = insert_entity(dict_, entity)
        mega_dict[entity_name] = dict_
    
    for query in queries:
        output = perform_ner(input_data=query,entity_data=mega_dict)
        if return_output: outputs.append(output)

    if return_output: return outputs

def fast_ner_test(data, return_output=False):
    mega_dict = {}

    for entity_name in data:
        dict_ = {}
        for entity in data[entity_name]:
            dict_ = insert_entity(dict_, entity)
        mega_dict[entity_name] = dict_

    input_string='Have you watched Naruto or Naruto Shippuden : Blood Prison?'
    output = perform_ner(input_data=input_string,entity_data=mega_dict)
    #print(output)
    if return_output:return output

def main():
    csv_data = load_csv_data()
    fast_ner_test(data=csv_data)

if __name__ == "__main__":
    main()