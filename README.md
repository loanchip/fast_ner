# fast_ner

A fast Named-Entity Recognition module

## Description
fast_ner is built from ground-up for quick response time when extracting entity data from input query.  
Utilizes a dictionary based approach to match and extract entity data from any text.  
 
### Performance:  
Entity Dataset Size: 10k entity value  
Input Query Size: 100k words  
Response Time: under 0.5s  
 
## Installation
``` bash
git clone https://github.com/loanchip/fast_ner.git
```  
Navigate to the directory  
``` bash
python setup.py install
```   
OR To use it as a Docker Container  
``` bash
docker-compose up
```  
   

## Usage 
```python
from fast_ner import ner

# to create new entities, provide folder path containing entity datasets
ner.add_new_entity(path_to_data_folder='abs_path_to_folder')

# to load already created entities, provide folder path to created entities,
# or use already provided entities by leaving that as None
data = ner.load_dict_data(path_to_data_folder='abs_path_to_folder')

# to perform NER extraction
query = 'Back to the Future is a great movie series'
output = ner.perform_ner(query, data)
# {'title': [(['back', 'to', 'the', 'future'], 0, 4)], 'review': [(['great'], 6, 7)]}
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)