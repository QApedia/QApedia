import pytest
import QApedia.generator


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
    # Testando cláusula DESCRIBE.
    test5 = ("DESCRIBE dbr:Panara_language", "http://dbpedia.org/sparql", list)
    return [test1, test2, test3, test4, test5]


def extract_pairs_test_data():
    # Template utilizado exemplo para testar generator.extract_pairs
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

    # Classe auxiliar para ajudar a simular a estrutura retornada pelo
    # perform_query
    class Value:
        def __init__(self, value):
            self.value = value

    # Exemplo com quatro resultados para teste
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

    # Situação 1: resultados não foram retornados, sem prefixos definidos.
    test1 = ([], template, 3, [], list)
    # Situação 2: resultados retornados, sem prefixos definidos
    test2 = (results, template, 3, [], list)
    # Situação 3: resultados retornados, prefixos definidos
    test3 = (results, template, 3,
             [("dbr:", "http://dbpedia.org/resource/")],
             list)
    return[test1, test2, test3]


def perform_query_test_failure_data():
    # Situação 1: link passado é inválido.
    test1 = ("ask where{ ?a dbo:author dbr:Yoshihiro_Togashi}",
             "link-invalido",
             r"unknown url type:*")
    # Situação 2: A query contém algum erro, falta o "?" antes da variável.
    test2 = ("ask where{ a dbo:author dbr:Yoshihiro_Togashi}",
             "http://dbpedia.org/sparql",
             r"QueryBadFormed:.*")

    return [test1, test2]


def test_adjust_generator_query(adjust_generator_query_example):
    generator_query, variables, expected = adjust_generator_query_example
    assert QApedia.generator.adjust_generator_query(generator_query,
                                                    variables) == expected


def test_adjust_generator_query_failure():
    generator_query = "ask where{?a dbo:author dbr:Yoshihiro_Togashi}"
    variables = ["a"]
    expected = r".*SELECT ... WHERE{...}.*"
    with pytest.raises(Exception, match=expected):
        QApedia.generator.adjust_generator_query(generator_query, variables)


@pytest.mark.parametrize('query, endpoint, expected',
                         perform_query_test_data())
def test_perform_query(query, endpoint, expected):
    assert type(
                QApedia.generator.perform_query(query,
                                                endpoint=endpoint)) == expected


@pytest.mark.parametrize('query, endpoint, expected',
                         perform_query_test_failure_data())
def test_perform_query_failure(query, endpoint, expected):
    query = "ask where{ a dbo:author dbr:Yoshihiro_Togashi}"
    with pytest.raises(Exception, match=expected):
        QApedia.generator.perform_query(query, endpoint=endpoint)


@pytest.mark.parametrize('gquery, variables, expected, use_cache',
                         generator_query_test_data())
def test_get_results_of_generator_query(gquery, variables, expected,
                                        use_cache):
    if(use_cache):
        QApedia.generator._cache[gquery] = []
    assert type(QApedia.generator.get_results_of_generator_query(gquery,
                                                                 variables)
                ) == expected


@pytest.mark.parametrize(("results, template, examples,"
                         "list_of_prefixes, expected"),
                         extract_pairs_test_data())
def test_extract_pairs(results, template, examples,
                       list_of_prefixes, expected):
    assert type(QApedia.generator.extract_pairs(results, template,
                                                examples,
                                                list_of_prefixes)) == expected
