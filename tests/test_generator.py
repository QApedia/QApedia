import pytest
import qapedia.generator


def generator_query_test_data():
    # selecionar animes baseado em mangás
    test1 = ("SELECT ?a "
             "WHERE {"
             "?a dbo:type dbr:Manga ."
             "?a dct:subject dbc:Anime_series_based_on_manga . }", ["a"], dict,
             False)
    # selecionar lista de mangás escritas por Yoshihiro Togashi
    test2 = ("select ?a "
             "where{ "
             "?a dbo:author dbr:Yoshihiro_Togashi"
             "}", [], dict, True)
    # selecionar animes baseado em mangás de Yoshihiro_Togashi e o estúdio
    test3 = ("select distinct(?a) ?b "
             "where{ "
             "?a dbo:author dbr:Yosnumber_of_exampleshihiro_Togashi."
             "?a dbp:studio ?b"
             "}", ["a", "b"], dict, False)
    return [test1, test2, test3]


def perform_query_test_data():
    # Selecionar quem é o autor de Yu Yu Hakusho
    test1 = ("SELECT * WHERE {dbr:Yu_Yu_Hakusho dbo:author ?autor.}",
             "http://dbpedia.org/sparql",
             dict)
    # Yoshihiro Togashi escreveu Yu Yu Hakusho?
    test2 = ("ask where{dbr:Yu_Yu_Hakusho dbo:author dbr:Yoshihiro_Togashi}",
             "http://dbpedia.org/sparql",
             dict)
    # Testando endpoint diferente
    # Quais mangás foram escritos por Yoshihiro Togashi?
    test3 = ("SELECT ?manga ?mangaLabel ?authorLabel "
             "WHERE{"
             "	?author ?label 'Yoshihiro Togashi'@en . "
             "    ?manga wdt:P31/wdt:P279? wd:Q8274."
             "	?manga wdt:P50 ?author ."
             "	SERVICE wikibase:label {"
             "		bd:serviceParam wikibase:language 'en' ."
             "	}"
             "}",
             "https://query.wikidata.org/bigdata/namespace/wdq/sparql",
             dict)
    # Togashi escreveu Hunter x Hunter?
    test4 = ("ASK WHERE { ?author ?label 'Yoshihiro Togashi'@pt ."
             "wd:Q696071 wdt:P50 ?author .}",
             "https://query.wikidata.org/sparql",
             dict)
    return [test1, test2, test3, test4]


def extract_pairs_test_data():
    template = {"question": "o manga <A> possui um anime?",
                "query": ("ask where { <A> dbo:type dbr:Manga . "
                          "<A> dct:subject dbc:Anime_series_based_on_manga.}"
                          ""),
                "generator_query": ("SELECT ?a ?la WHERE {"
                                    "?a dbo:type dbr:Manga ."
                                    "?a dct:subject dbc:Anime_series_based_on"
                                    "_manga . "
                                    "?a rdfs:label ?la . "
                                    "FILTER(lang(?la) = 'pt')}"),
                "variables": ["a"]
                }
    # Exemplo com quatro resultados
    results = [  # Manga 1
                {'a': {'type': 'uri',
                       'value': 'http://dbpedia.org/resource/Maison_Ikkoku'},
                    'la': {'type': 'literal', 'xml:lang': 'pt',
                           'value': 'Maison Ikkoku'}},
                # Manga 2
                {'a': {'type': 'uri',
                       'value': 'http://dbpedia.org/resource/One_Piece'},
                    'la': {'type': 'literal', 'xml:lang': 'pt',
                           'value': 'One Piece'}},
                # Manga 3
                {'a': {'type': 'uri',
                       'value': 'http://dbpedia.org/resource/'\
                                'We_Were_There_(manga)'},
                    'la': {'type': 'literal', 'xml:lang': 'pt',
                           'value': 'Bokura ga Ita'}},
                # Manga 4
                {'a': {'type': 'uri',
                       'value': 'http://dbpedia.org/resource/Noragami'},
                    'la': {
                        'type': 'literal', 'xml:lang': 'pt',
                        'value': 'Noragami'}}]

    test1 = ([], template, 3, list)
    test2 = (results, template, 3, list)
    return[test1, test2]


def test_adjust_generator_query(adjust_generator_query_example):
    generator_query, variables, expected = adjust_generator_query_example
    assert qapedia.generator.adjust_generator_query(generator_query,
                                                    variables) == expected


def test_adjust_generator_query_failure():
    generator_query = "ask where{?a dbo:author dbr:Yoshihiro_Togashi}"
    variables = ["a"]
    expected = r".*SELECT ... WHERE{...}.*"
    with pytest.raises(Exception, match=expected):
        qapedia.generator.adjust_generator_query(generator_query, variables)


@pytest.mark.parametrize('query,endpoint, expected', perform_query_test_data())
def test_perform_query(query, endpoint, expected):
    assert type(qapedia.generator.perform_query(query, endpoint)) == expected


@pytest.mark.parametrize('gquery, variables, expected, use_cache',
                         generator_query_test_data())
def test_get_results_of_generator_query(gquery, variables, expected,
                                        use_cache):
    if(use_cache):
        qapedia.generator._cache[gquery] = {}
    assert type(qapedia.generator.get_results_of_generator_query(gquery,
                                                                 variables)
                ) == expected


@pytest.mark.parametrize('results, template, examples, expected',
                         extract_pairs_test_data())
def test_extract_pairs(results, template, examples, expected):
    assert type(qapedia.generator.extract_pairs(results, template,
                                                examples)) == expected
