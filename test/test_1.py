from fast_ner.ner import add_new_entity, load_data, perform_ner

#ner.add_new_entity(entity_name='movies')
data = load_data()
input_string='I would love to watch Travel Mates 2 or Marc Maron: Too Real right now.'
output = perform_ner(input_data=input_string,entity_data=data)
print('Detected Entities:')
print(output)
