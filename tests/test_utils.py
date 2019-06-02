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


def test_convert_prefixes_to_list():
    prefixes = "PREFIX vCard: <http://www.w3.org/2001/vcard-rdf/3.0#>\
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>"
    expected = [("vCard:", "http://www.w3.org/2001/vcard-rdf/3.0#"),
                ("foaf:", "http://xmlns.com/foaf/0.1/")]
    assert qapedia.utils.convert_prefixes_to_list(prefixes) == expected

def test_encode():
    sparql = "SELECT DISTINCT(?a) ?b WHERE { ?a dbo:location ?b }"
    prefixes = [("dbo:", "http://dbpedia.org/ontology/")]
    expected = "SELECT DISTINCT(var_a) var_b WHERE  bracket_open  var_a "\
               "dbo_location var_b  bracket_close "    
    assert qapedia.utils.encode(sparql, prefixes) == expected

def test_decode():
    sparql_encoded = "SELECT DISTINCT(var_a) var_b WHERE  bracket_open  "\
                     "var_a dbo_location var_b  bracket_close " 
    prefixes = [("dbo:", "http://dbpedia.org/ontology/")]
    expected = "SELECT DISTINCT(?a) ?b WHERE { ?a dbo:location ?b }"
    assert qapedia.utils.decode(sparql_encoded, prefixes) == expected