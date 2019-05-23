import pytest
import qapedia.utils


def extract_variables_test_data():
    test1 = ("select distinct(?a) where { ?a dbo:abstract [] }",
             ["a"])
    test2 = ("SELECT DISTINCT(?a) ?b WHERE { ?a dbo:location ?b }",
             ["a", "b"])
    test3 = ("select distinct ?a ?b ?c where { "
             "?uri <http://dbpedia.org/property/relatives> ?b ."
             "?uri <http://dbpedia.org/ontology/child> ?a . "
             "?uri a ?c }", ["a", "b", "c"])
    test4 = ("select * where { ?a dbo:abstract [] }",
             None)
    return [test1, test2, test3, test4]


@pytest.mark.parametrize('generator_query, expected',
                         extract_variables_test_data())
def test_extract_variables(generator_query, expected):
    assert qapedia.utils.extract_variables(generator_query) == expected
