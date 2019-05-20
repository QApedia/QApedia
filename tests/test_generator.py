import pytest
import csv
from qapedia.generator import *
import os
import json


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'fixtures',
)


def adjust_generator_query_test_data():
    test_data_path = os.path.join(FIXTURE_DIR,
                                  'adjust_generator_query_test_data.json')
    return json.load(open(test_data_path))
    

def perform_query_test_data():
    #Selecionar nome dos mangas que tem publicador como dbr:Shueisha
    query1 = ("SELECT ?nome_manga WHERE {"
                "?manga a dbo:Manga . "
                "?manga rdfs:label ?nome_manga . "
                "?manga dbo:publisher dbr:Shueisha. "
                "FILTER(lang(?nome_manga) = 'pt')."
                "}")    
    return [(query1, dict)]

## TESTS

@pytest.mark.parametrize('generator_query, variables, expected',
                         adjust_generator_query_test_data())
def test_adjust_generator_query(generator_query, variables, expected):
    assert adjust_generator_query(generator_query, variables) == expected
    

@pytest.mark.parametrize('query, expected',
                         perform_query_test_data())
def test_perform_query(query, expected):
    assert type(perform_query(query)) == expected


def test_get_results_of_generator_query():
    pass


def test_extract_pairs():
    pass