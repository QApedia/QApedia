import pytest
from qapedia.generator import adjust_generator_query,\
                              extract_pairs, extract_pairs,\
                              get_results_of_generator_query,\
                              perform_query


def generator_query_test_data():
    #selecionar animes baseado em mangás
    test1 = ("SELECT ?a "\
            "WHERE {"\
            "?a dbo:type dbr:Manga ."\
            "?a dct:subject dbc:Anime_series_based_on_manga . "\
            "}", ["a"], dict)
    #selecionar lista de mangás escritas por Yoshihiro Togashi
    test2 = ("select ?a "\
             "where{ "\
             "?a dbo:author dbr:Yoshihiro_Togashi"\
             "}", ["a"], dict)
    #selecionar animes baseado em mangás de Yoshihiro_Togashi e o estúdio
    test3 = ("select distinct(?a) ?b "\
             "where{ "\
             "?a dbo:author dbr:Yoshihiro_Togashi."\
             "?a dbp:studio ?b"\
             "}", ["a", "b"], dict)
    return [test1, test2, test3]  

def perform_query_test_data():
    #Selecionar quem é o autor de Yu Yu Hakusho
    test1 = ("SELECT * WHERE {dbr:Yu_Yu_Hakusho dbo:author ?autor.}",
             "http://dbpedia.org/sparql",
             dict)
    #Yoshihiro Togashi escreveu Yu Yu Hakusho?
    test2 = ("ask where{dbr:Yu_Yu_Hakusho dbo:author dbr:Yoshihiro_Togashi}",
             "http://dbpedia.org/sparql",
             dict)
    #Testando um endpoint diferente
    #Quais mangás foram escritos por Yoshihiro Togashi?
    test3 = ("SELECT ?manga ?mangaLabel ?authorLabel "\
             "WHERE{"\
             "	?author ?label 'Yoshihiro Togashi'@en . "\
             "    ?manga wdt:P31/wdt:P279? wd:Q8274."\
             "	?manga wdt:P50 ?author ."\
             "	SERVICE wikibase:label {"\
             "		bd:serviceParam wikibase:language 'en' ."\
             "	}"\
             "}", 
             "https://query.wikidata.org/sparql",
             dict)
    #Togashi escreveu Hunter x Hunter?
    test4 = ("ASK WHERE { ?author ?label 'Yoshihiro Togashi'@pt ."\
             "wd:Q696071 wdt:P50 ?author .}", 
             "https://query.wikidata.org/sparql",
             dict)
    return [test1, test2, test3, test4]
  
def extract_pairs_test_data():
    template = {"question": "o manga <A> possui um anime?",
                "query": ("ask where { <A> dbo:type dbr:Manga . "
                         "<A> dct:subject dbc:Anime_series_based_on_manga .}"),
                "generator_query": ("SELECT ?a ?la WHERE {"
                                    "?a dbo:type dbr:Manga ."
                                    "?a dct:subject dbc:Anime_series_based_on_manga . "
                                    "?a rdfs:label ?la . "
                                    "FILTER(lang(?la) = 'pt')}"),
                "variables": ["a"]
                }
    #Exemplo com quatro resultados
    results = [ #Manga 1
                {'a': {'type': 'uri', 'value': 'http://dbpedia.org/resource/Maison_Ikkoku'}, 
                'la': {'type': 'literal', 'xml:lang': 'pt', 'value': 'Maison Ikkoku'}},
                #Manga 2
                {'a': {'type': 'uri', 'value': 'http://dbpedia.org/resource/One_Piece'},
                'la': {'type': 'literal', 'xml:lang': 'pt', 'value': 'One Piece'}},
                #Manga 3
                {'a': {'type': 'uri', 'value': 'http://dbpedia.org/resource/We_Were_There_(manga)'},
                'la': {'type': 'literal', 'xml:lang': 'pt', 'value': 'Bokura ga Ita'}},
                #Manga 4
                {'a': {'type': 'uri', 'value': 'http://dbpedia.org/resource/Noragami'},
                'la': {'type': 'literal', 'xml:lang': 'pt', 'value': 'Noragami'}}]
        
    return[(results, template, list)] 
        
        
def test_adjust_generator_query(adjust_generator_query_example):
    generator_query, variables, expected = adjust_generator_query_example
    assert adjust_generator_query(generator_query, variables) == expected
    
    
@pytest.mark.parametrize('query,endpoint, expected', perform_query_test_data())
def test_perform_query(query, endpoint, expected):
    assert type(perform_query(query, endpoint)) == expected
    

@pytest.mark.parametrize('gquery, variables, expected',
                         generator_query_test_data())
def test_get_results_of_generator_query(gquery, variables, expected):
    assert type(get_results_of_generator_query(gquery, variables)) == expected


@pytest.mark.parametrize('results, template, expected', extract_pairs_test_data())
def test_extract_pairs(results, template, expected):
    assert type(extract_pairs(results, template)) == list