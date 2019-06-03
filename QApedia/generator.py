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
    * get_results_of_generator_query - similar a função ``perform_query``,
      entretanto, realiza os ajustes em cima da ``generator_query`` e salva o
      resultado da busca na memória.
    * extract_pairs - realiza a construção dos pares de questão-sparql
      com base no resultado e template especificados."""

import re
from random import shuffle
from SPARQLWrapper import SPARQLWrapper2, SPARQLExceptions, SmartWrapper
from urllib.error import HTTPError
from QApedia import utils
from os.path import basename

__all__ = ['adjust_generator_query', 'perform_query',
           'get_results_of_generator_query', 'extract_pairs']


_cache = {}


def _adjust_uri(current_uri, prefixes_list):
    """Método auxiliar utilizado por ``extract_pairs`` que realiza a
    substiuição dos URIs pela sua versão reduzida.

    Parameters
    ----------
    current_uri : str
        URI, por exemplo, ``http://dbpedia.org/resource/Brazil``.
    prefixes_list : [type]
        lista contendo os prefixos, por exemplo,
        [("dbr:", "http://dbpedia.org/resource/")].

    Returns
    -------
    str
        URI no formato reduzido, por exemplo,
        ``http://dbpedia.org/resource/Brazil`` se torna ``dbr:Brazil``.
    """
    for prefix, uri in prefixes_list:
        if uri in current_uri:
            return prefix + basename(current_uri)
    return f"<{current_uri}>"


def _extract_bindings(result):
    """Método auxiliar utilizado em ``perform_query`` que tem como objetivo
    retornar os bindings/boolean retornados pela busca.
    """
    if(type(result) == SmartWrapper.Bindings):
        return result.bindings
    if 'boolean' in result:
        result = result['boolean']
    else:
        result = result['results']['bindings']
    return result


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

    pattern = r"select(.*)where\s*\{([^)]+)\}([^}]+)*$"
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


def perform_query(query, prefixes="", endpoint="http://dbpedia.org/sparql"):
    """Dada uma query sparql retorna uma lista correspondendo ao
    resultado da pesquisa se a cláusula utilizada for SELECT, CONSTRUCT ou
    DESCRIBE. Caso seja ASK, o valor retornado é um `boolean`.

    Parameters
    ----------
    query : str
        Sparql utilizada para realizar uma busca no endpoint
        especificado.
    prefixes: str, optional
        Corresponde ao conjunto de prefixos utilizados na consulta SPARQL.
        Se não estiver usando prefixos, o uso desse parâmetro não é
        necessário, o valor padrão é "".
    endpoint : str, optional
        Indica endpoint utilizado, o valor default é
        ``http://dbpedia.org/sparql``

    Returns
    -------
    list of dict
        Corresponde a um lista contendo ``bindinds`` retornados pela busca
        Sparql. Se a cláusula utiliza SELECT ou CONSTRUCT.
    bool
        Se a cláusula ASK for afirmativa retorna True, caso contrário False.

    Examples
    --------
    .. code-block:: python

        >>> from QApedia.generator import perform_query
        >>> query = "SELECT * WHERE {"\\
        ...         "?manga a dbo:Manga ."\\
        ...         "?manga rdfs:label ?nome ."\\
        ...         "?manga dbo:author dbr:Yoshihiro_Togashi ."\\
        ...         "FILTER(lang(?nome) = 'pt').}"
        >>> results = perform_query(query)
        >>> for result in results:
        ...     print("%s: %s" %(result["nome"].value, result["manga"].value))
        ...
        Level E: http://dbpedia.org/resource/Level_E
        Yu Yu Hakusho: http://dbpedia.org/resource/Yu_Yu_Hakusho
        Hunter × Hunter: http://dbpedia.org/resource/Hunter_×_Hunter

    Raises
    ------
    exc_type
        Caso haja um erro que não seja proveniente do problema de acesso ao
        endpoint, por exemplo, uma query em um formato inválido, uma exceção é
        gerada.
    """
    sparql_query = prefixes + query
    sparql = SPARQLWrapper2(endpoint)
    sparql.setTimeout(600)
    sparql.setQuery(sparql_query)
    try:
        result = sparql.queryAndConvert()
        result = _extract_bindings(result)
    except (HTTPError, SPARQLExceptions.EndPointInternalError):
        result = []
    except Exception as e:
        raise e
    return result


def get_results_of_generator_query(generator_query, variables, prefixes="",
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
    prefixes: str, optional
        Corresponde ao conjunto de prefixos utilizados na consulta SPARQL.
        Se não estiver usando prefixos, o uso desse parâmetro não é
        necessário, o valor padrão é "".
    endpoint : str, optional
        Indica endpoint utilizado., by default "http://dbpedia.org/sparql"
    lang : str, optional
       Idioma do campo ``rdfs:label`` adicionado na
       ``generator_query``. O valor padrão é "pt".

    Returns
    -------
    list of dict
        Corresponde a um lista contendo ``bindinds`` retornados pela busca
        Sparql. Se a cláusula utiliza SELECT ou CONSTRUCT.
    bool
        Se a cláusula ASK for afirmativa retorna True, caso contrário False.
    """
    query = adjust_generator_query(generator_query, variables, lang)
    if query in _cache:
        results = _cache[query]
    else:
        results = perform_query(query, prefixes, endpoint)
        _cache[query] = results
    return results


def extract_pairs(bindings, template, number_of_examples=500,
                  list_of_prefixes=[]):
    """Realiza a extração do conjunto de pares  de questão-sparql
    correspondentes obtidos pelo método
    :func:`QApedia.generator.get_bindings_of_generator_query`.

    Parameters
    ----------
    bindings : list
        Resultado obtido após a execução da query correspondendo aos
        "bindings"
    template : dict
        Corresponde ao template utilizado para geração dos resultados.
    number_of_examples : int, optional
        Número de resultados a serem considerados para o template, o valor
        padrão é 500.
    list_of_prefixes: list, optional
        Corresponde a lista de prefixos obtida através do método
        :func:`QApedia.utils.convert_prefixes_to_list`, onde os prefixos devem
        ser os mesmos que foram utilizados na função que gerou os bindings.
        Se não estiver usando prefixos, o uso desse parâmetro não é
        necessário, o valor padrão é [].

    Returns
    -------
    list
        Lista contendo os pares ``sparql``-``question`` do template.

    Examples
    --------
    .. code-block:: python

        >>> from QApedia.generator import extract_pairs
        >>> from QApedia.generator import get_results_of_generator_query
        >>> template = {"question": "Yoshihiro Togashi escreveu <A>?",
        ...             "query": "ask where {"\\
        ...                      "dbr:Yoshihiro_Togashi ^ dbo:author <A>}",
        ...             "generator_query": "select ?a where{"\\
        ...                          "dbr:Yoshihiro_Togashi ^ dbo:author ?a}",
        ...             "variables": ["a"]}
        >>> bindings = get_results_of_generator_query(
        ...                                       template["generator_query"],
        ...                                       template["variables"])
        >>> pairs = extract_pairs(bindings, template)
        >>> pairs[2]["question"]
        'Yoshihiro Togashi escreveu Hunter × Hunter?'
        >>> pairs[2]["sparql"]
        'ask where {dbr:Yoshihiro_Togashi ^ dbo:author http://dbpedia.org/\
resource/Hunter_×_Hunter}'
    """
    my_bindings = bindings.copy()

    if not my_bindings:
        return []

    if len(my_bindings) > number_of_examples:
        my_bindings = my_bindings[0:number_of_examples]

    pairs = list()

    for result in my_bindings:
        query = template['query']
        question = template['question']
        # Para cada variável preencher as lacunas com os resultados da busca
        for variable in template['variables']:
            question = question.replace('<%s>' % variable.upper(),
                                                result[f"l{variable}"].value)
            query = query.replace('<%s>' % variable.upper(),
                                          _adjust_uri(
                                          result[variable].value,
                                          list_of_prefixes))
        pairs.append({'sparql': query, 'question': question})
    return pairs
