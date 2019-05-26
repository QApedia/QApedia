"""
O módulo ``generator`` permite ao usuário realizar buscas sobre o
endpoint da dbpedia. Além disso, permite ao usuário realizar a
construção de queries sparql dado um template previamente especificado.

Este arquivo pode ser importado como um módulo e contém as seguintes
funções:

    * adjust_generator_query - retorna a ``generator_query`` com os
      rótulos correspondente a cada variável.
    * perform_query - realiza a execução da query no endpoint da
      dbpedia.
    * get_results_of_generator_query - idem a função ``perform_query``,
      sendo a diferença, que essa armazena o resultado da última
      busca caso exista.
    * extract_pairs - realiza a construção dos pares de questão-sparql
      com base no resultado e template especificados."""

import re
from random import shuffle
from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
from urllib.error import HTTPError
import sys

_cache = {}


def adjust_generator_query(generator_query, variables, lang="pt"):
    """Dada uma ```generator_query``` é retornada uma versão contendo
    os labels que são utilizados para preencher as lacunas presentes na
    pergunta.

    Parameters
    ----------
    generator_query : str
        Query utilizada para geração dos pares de questão-sparql.
    variables : list
        Lista contendo as variáveis utilizadas nas lacunas da
        questão-sparql.
    lang : str, optional
        Idioma do campo ``rdfs:label`` adicionado na
        ``generator_query``. O valor padrão é "pt".

    Returns
    -------
    str
        Retorna a `generator_query` com os campos `labels` de cada
        variável.

    Examples
    --------
    No exemplo a seguir, temos a ``generator_query`` que será utilizada
    futuramente para retornar recursos que tenham o campo
    ``dbo:abstract``. O resultado dela é usado para preencher as
    lacunas do seguinte par (``"o que é <A>?"``, ``"select ?a where {
    <A> dbo:abstract ?a "``). Para preencher a lacuna da pergunta em
    linguagem natural, é adicionada na ``generator_query`` o campo
    ``rdfs:label`` correspondente as variáveis que se deseja obter
    informações.

    .. code-block:: python

        >>> generator_query = "select distinct(?a) WHERE { ?a dbo:abstract []}"
        >>> variables = ['a']
        >>> result = adjust_generator_query(generator_query, variables)
        >>> result
        "select distinct(?a) ?la where { ?a rdfs:label ?la. FILTER(lang(?la) \
= 'pt').  ?a dbo:abstract [] }"
    """

    def label_query(v):
        return f"?{v} rdfs:label ?l{v}. FILTER(lang(?l{v}) = '{lang}'). "

    pattern = r"select(.+)where\s*{(.+)}([^}]+)*$"
    valid = re.findall(pattern, generator_query, re.IGNORECASE)
    if not valid:
        raise Exception("A query não possui formato SELECT ... WHERE{...}")
    else:
        # Não se deseja adicionar a variável label na query
        if not variables:
            return generator_query
        # first_piece: antes do where, last_piece: depois do where
        first_piece, inside_where, last_piece,  = valid[0]
        first_piece += ''.join(map("?l{:} ".format, variables))
        inside_where = ''.join(map(label_query, variables)) + inside_where
        # nova query construída com os campos de labels
        new_query = f"select{first_piece}where {{{inside_where}}}{last_piece}"
        return new_query


def perform_query(query, endpoint="http://dbpedia.org/sparql"):
    """Dada uma query sparql retorna um dicionário correspondendo ao
    resultado da pesquisa.

    Parameters
    ----------
    query : str
        Sparql utilizada para realizar uma busca no endpoint
        especificado.
    endpoint : str, optional
        Indica endpoint utilizado, o valor default é
        ``http://dbpedia.org/sparql``

    Returns
    -------
    dict
        Corresponde a um dicionário contendo os ``results`` e
        ``bindinds`` retornados pela busca Sparql.

    Examples
    --------
    .. code-block:: python

        >>> query = "SELECT * WHERE {"\\
        ...         "?manga a dbo:Manga ."\\
        ...         "?manga rdfs:label ?nome_manga ."\\
        ...         "?manga dbo:author dbr:Yoshihiro_Togashi ."\\
        ...         "FILTER(lang(?nome_manga) = 'pt').}"
        >>> results = perform_query(query)
        >>> results["head"]
        >>> results = perform_query(query)
        >>> results["head"]["vars"]
        ['manga', 'nome_manga']
        >>> results["results"]["bindings"][0]["manga"]
        {'type': 'uri', 'value': 'http://dbpedia.org/resource/Level_E'}
        >>> results["results"]["bindings"][0]["nome_manga"]
        {'type': 'literal', 'xml:lang': 'pt', 'value': 'Level E'}

    Raises
    ------
    exc_type
        Caso haja um erro que não seja proveniente do problema de acesso ao
        endpoint, por exemplo, uma query em um formato inválido, uma exceção é
        gerada.
    """
    sparql = SPARQLWrapper(endpoint)
    sparql.setTimeout(600)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        result = sparql.query().convert()
    except (HTTPError, SPARQLExceptions.EndPointInternalError):
        result = {"results": {"bindings": []}}
    except Exception as e:
        exc_type, _, _ = sys.exc_info()
        raise exc_type
    return result


def get_results_of_generator_query(generator_query, variables,
                                   endpoint="http://dbpedia.org/sparql",
                                   lang="pt"):

    """Dada uma ```generator_query``` é retornado um conjunto de
    resultados obtidos ao executar a query no endpoint especificado.

    Parameters
    ----------
    generator_query : str
        String representando a ```generator_query```.
    variables : list
        Lista de caracteres correspondendo as variáveis.
    endpoint : str, optional
        Indica endpoint utilizado., by default "http://dbpedia.org/sparql"
    lang : str, optional
       Idioma do campo ``rdfs:label`` adicionado na
       ``generator_query``. O valor padrão é "pt".

    Returns
    -------
    dict
        Corresponde a um dicionário contendo os ``head`` e ``results``
        retornados pela busca Sparql.
    """
    query = adjust_generator_query(generator_query, variables, lang)
    if query in _cache:
        results = _cache[query]
    else:
        results = perform_query(query, endpoint)
        _cache[query] = results
    return results


def extract_pairs(results, template, number_of_examples=600):
    """Realiza a extração do conjunto de pares  de questão-sparql
    correspondentes obtidos pelo método
    :func:`qapedia.generator.get_results_of_generator_query`.

    Parameters
    ----------
    results : list
        Resultado obtido após a execução da query, ["results"]
        ["bindings"]
    template : dict
        Corresponde ao template utilizado para geração dos resultados.
    number_of_examples : int, optional
        Número de resultados a serem considerados para o template,
        padrão 600.

    Returns
    -------
    list
        Lista contendo os pares ``sparql``-``question`` do template.

    Examples
    --------
    .. code-block:: python

        >>> from qapedia.generator import extract_pairs
        >>> from qapedia.generator import get_results_of_generator_query
        >>> template = {"question": "Yoshihiro Togashi escreveu <A>?",
        ...             "query": "ask where {"\\
        ...                      "dbr:Yoshihiro_Togashi ^ dbo:author <A>}",
        ...             "generator_query": "select ?a where{"\\
        ...                          "dbr:Yoshihiro_Togashi ^ dbo:author ?a}",
        ...             "variables": ["a"]}
        >>> results = get_results_of_generator_query(
        ...                                       template["generator_query"],
        ...                                       template["variables"])
        >>> pairs = extract_pairs(results["results"]["bindings"], template)
        >>> pairs[1]["question"]
        'Yoshihiro Togashi escreveu Hunter × Hunter?'
        >>> pairs[1]["sparql"]
        'ask where {dbr:Yoshihiro_Togashi ^ dbo:author http://dbpedia.org/\
resource/Hunter_×_Hunter}'
    """
    data = results.copy()

    if not data:
        return []

    if len(data) > number_of_examples:
        # data = sort_matches(data, template)[0:number_of_examples]
        data = data[0:number_of_examples]

    # Embaralha os dados
    shuffle(data)

    pairs = []
    for result in data:
        bindings = {key: value['value'] for key, value in result.items()}
        query = template['query']
        question = template['question']

        for variable in template['variables']:
            query = query.replace(
                '<%s>' % variable.upper(), "<%s>" % bindings[variable])
            question = question.replace(
                '<%s>' % variable.upper(), bindings['l'+variable])
        pairs.append({'sparql': query, 'question': question})
    return pairs
