from flask import Flask, request
from fast_ner import ner
server = Flask(__name__)


@server.route("/health/", methods=["GET"])
def health_check():
    return "success"


@server.route("/", methods=["POST"])
def perform_ner():
    data = request.get_json()

    if 'input_data' not in data:
        return 'Error! Provide query data.'
    input_data = data['input_data']

    if 'entity_data' in data:
        entity_data = data['entity_data']
    else:
        entity_data = None

    if 'fuzzy_matching' in data:
        fuzzy_matching = data['fuzzy_matching']
    else:
        fuzzy_matching = None

    if 'csv_data' in data:
        csv_data = data['csv_data']
    else:
        csv_data = None

    return ner.perform_ner(input_data, entity_data, fuzzy_matching, csv_data)


if __name__ == "__main__":
    server.run(host="0.0.0.0")
