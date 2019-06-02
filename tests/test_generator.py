import pytest
import qapedia.generator


def generator_query_test_data():
    # selecionar animes baseado em mangás
    test1 = ("SELECT ?a "
             "WHERE {"
             "?a dbo:type dbr:Manga ."
             "?a dct:subject dbc:Anime_series_based_on_manga . }", ["a"], list,
             False)
    # selecionar lista de mangás escritas por Yoshihiro Togashi
    test2 = ("select ?a "
             "where{ "
             "?a dbo:author dbr:Yoshihiro_Togashi"
             "}", [], list, True)
    # selecionar animes baseado em mangás de Yoshihiro_Togashi e o estúdio
    test3 = ("select distinct(?a) ?b "
             "where{ "
             "?a dbo:author dbr:Yosnumber_of_exampleshihiro_Togashi."
             "?a dbp:studio ?b"
             "}", ["a", "b"], list, False)
    return [test1, test2, test3]


def perform_query_test_data():
    # Selecionar quem é o autor de Yu Yu Hakusho
    test1 = ("SELECT * WHERE {dbr:Yu_Yu_Hakusho dbo:author ?autor.}",
             "http://dbpedia.org/sparql",
             list)
    # Yoshihiro Togashi escreveu Yu Yu Hakusho?
    test2 = ("ask where{dbr:Yu_Yu_Hakusho dbo:author dbr:Yoshihiro_Togashi}",
             "http://dbpedia.org/sparql",
             bool)
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
             list)
    # Togashi escreveu Hunter x Hunter?
    test4 = ("ASK WHERE { ?author ?label 'Yoshihiro Togashi'@pt ."
             "wd:Q696071 wdt:P50 ?author .}",
             "https://query.wikidata.org/sparql",
             bool)

    test5 = ("DESCRIBE dbr:Panara_language", "http://dbpedia.org/sparql", list)
    return [test1, test2, test3, test4, test5]


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

    class Value:
        def __init__(self, value):
            self.value = value
    # Exemplo com quatro resultados
    results = [  # Manga 1
                {'a': Value('dbr:Maison_Ikkoku'),
                 'la': Value('Maison Ikkoku')},
                # Manga 2
                {'a': Value('http://dbpedia.org/resource/One_Piece'),
                 'la': Value('One Piece')},
                # Manga 3
                {'a': Value('http://dbpedia.org/resource/'\
                            'We_Were_There_(manga)'),
                 'la': Value('Bokura ga Ita')},
                # Manga 4
                {'a': Value('http://dbpedia.org/resource/Noragami'),
                 'la': Value('Noragami')}]

    test1 = ([], template, 3, [], list)
    test2 = (results, template, 3, [], list)
    test3 = (results, template, 3,
             [("dbr:", "http://dbpedia.org/resource/")],
             list)
    return[test1, test2, test3]


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


@pytest.mark.parametrize('query, endpoint, expected',
                         perform_query_test_data())
def test_perform_query(query, endpoint, expected):
    assert type(
                qapedia.generator.perform_query(query,
                                                endpoint=endpoint)) == expected


def perform_query_test_failure_data():
    test1 = ("ask where{ ?a dbo:author dbr:Yoshihiro_Togashi}",
             "link-invalido",
             r"unknown url type:*")

    test2 = ("ask where{ a dbo:author dbr:Yoshihiro_Togashi}",
             "http://dbpedia.org/sparql",
             r"QueryBadFormed:.*")

    return [test1, test2]


@pytest.mark.parametrize('query, endpoint, expected',
                         perform_query_test_failure_data())
def test_perform_query_failure(query, endpoint, expected):
    query = "ask where{ a dbo:author dbr:Yoshihiro_Togashi}"
    with pytest.raises(Exception, match=expected):
        qapedia.generator.perform_query(query, endpoint=endpoint)


@pytest.mark.parametrize('gquery, variables, expected, use_cache',
                         generator_query_test_data())
def test_get_results_of_generator_query(gquery, variables, expected,
                                        use_cache):
    if(use_cache):
        qapedia.generator._cache[gquery] = []
    assert type(qapedia.generator.get_results_of_generator_query(gquery,
                                                                 variables)
                ) == expected


@pytest.mark.parametrize(("results, template, examples,"
                         "list_of_prefixes, expected"),
                         extract_pairs_test_data())
def test_extract_pairs(results, template, examples,
                       list_of_prefixes, expected):
    assert type(qapedia.generator.extract_pairs(results, template,
                                                examples,
                                                list_of_prefixes)) == expected
