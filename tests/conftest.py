import pytest
import os
import json

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'fixtures',
)


def load_adjust_generator_query_test_data():
    # Carregar json contendo os parâmetros do teste
    test_data_path = os.path.join(FIXTURE_DIR,
                                  'adjust_generator_query_test_data.json')
    return json.load(open(test_data_path))


@pytest.fixture(params=load_adjust_generator_query_test_data())
def adjust_generator_query_example(request):
    # Retorna cada exemplo da função definida no parâmetro
    return request.param
