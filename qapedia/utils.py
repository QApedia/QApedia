"""Este módulo contém o conjunto de operações utilizadas pelos módulos
principais como por exemplo, o método
:func:`qapedia.io.load_templates` que utiliza o método
:func:`qapedia.utils.extract_variables` desse módulo para extrair o conjunto
de variáveis presentes na query geradora (``generator_query``).

Neste módulo, pode-se encontrar as seguintes funções:

    * extract_variables - realiza a extração das variáveis presentes no select
      da query geradora.
    * convert_prefixes_to_list - dado o conjunto de prefixos, converte a
      string em uma lista de tuplas.
"""
import re


__all__ = ['extract_variables', 'convert_prefixes_to_list', 'encode', 'decode']

_symbols_and_its_equivalent = [("{", " bracket_open "),
                               ("}", " bracket_close "),
                               ("?", "var_"),
                               ("!=", " not_equal_to "),
                               (">=", " greater_than_or_equal_to "),
                               ("<=", " less_than_or_equal_to "),
                               ("=", " equal_to "),
                               (">", " greater_than "),
                               ("<", " less_than "),
                               ("&&", " and "),
                               ("||", " or "),
                               ("!", " not ")
                               ]


def extract_variables(generator_query):
    """Extrai as variáveis correspondente presentes no 'generator_query'.

    Parameters
    ----------
    generator_query : str
        A 'generator_query' corresponde a query que será utilizada para obter
        as variáveis presente nas lacunas da pergunta(``query``) e do sparql.

    Returns
    -------
    lst
        Lista contendo as variáveis a serem respondidas.

    Examples
    --------
    .. code-block:: python

        >>> generator_query = "select distinct ?a where {"\\
        ...                   "?uri <http://dbpedia.org/ontology/author> ?a }"
        >>> variables = extract_variables(generator_query)
        >>> print(variables)
        ['a']
    """
    variables = re.findall('^(.+?)where', generator_query, re.IGNORECASE)
    if variables:
        variables = re.findall(r"\?(\w)", variables[0])
    if not variables:
        return None
    return variables


def convert_prefixes_to_list(prefixes):
    """Converte uma string dos prefixos em uma lista de tuplas. Onde cada par
    contém um identificador e a uri correspondente.

    Parameters
    ----------
    prefixes : str
        string correspondendo aos prefixos utilizados na consulta SPARQL.

    Returns
    -------
    list
        Lista de tuplas, onde cada tupla contém dois itens, o primeiro
        corresponde ao nome dado a URI que corresponde ao segundo item.
    """
    pattern = r"(\w+:)\s*\<(.*?)\>"
    prefixes_list = re.findall(pattern, prefixes)
    return prefixes_list


def _replace_symbols_with_text(sparql):
    for symbol, text in _symbols_and_its_equivalent:
        sparql = sparql.replace(symbol, text)
    sparql = re.sub(r"\.(\B|filter)", r" sep_dot \1", sparql, flags=re.I)
    sparql = re.sub(r'\;(\B|filter)', r" sep_semicolon \1", sparql, flags=re.I)
    return sparql


def encode(sparql, prefixes):
    """Dada uma query sparql, essa função transforma algum de seus caracteres
    em texto.

    Parameters
    ----------
    sparql : str
        sparql a ser transformada.
    prefixes : list
        lista de prefixos com uris utilizadas na sparql retornadas pela função
        :func:`qapedia.utils.convert_prefixes_to_list`.

    Returns
    -------
    str
        sparql transformada.
    
    Examples
    --------
    .. code-block:: python

        >>> from qapedia.utils import encode
        >>> from qapedia.utils import convert_prefixes_to_list
        >>> prefixes = "PREFIX prop: <http://dbpedia.org/property/>\\
        ...             PREFIX dbr: <http://dbpedia.org/resource/>"
        >>> query = "ASK {\\n\\
        ...         <http://dbpedia.org/resource/Amazon_River> prop:length ?amazon .\\n\\
        ...         <http://dbpedia.org/resource/Nile> prop:length ?nile .\\n\\
        ...         FILTER(?amazon > ?nile) .}"
        >>> list_of_prefixes = convert_prefixes_to_list(prefixes)
        >>> query_encoded = encode(query, list_of_prefixes)
        >>> print(query_encoded)
        ASK  bracket_open 
                dbr_Amazon_River prop_length var_amazon  sep_dot 
                dbr_Nile prop_length var_nile  sep_dot 
                FILTER(var_amazon  greater_than  var_nile)  sep_dot  bracket_close 
    """
    for prefix, uri in prefixes:
        encoding = prefix.replace(":", "_")
        sparql = sparql.replace(prefix, encoding)
        sparql = re.sub(f"<{uri}(.*?)>", fr'{encoding}\1', sparql)
    # Realizar substituição dos caracteres da consulta por texto.
    sparql = _replace_symbols_with_text(sparql)
    return sparql


def _encoded_symbols_to_symbols(sparql):
    for symbol, text in _symbols_and_its_equivalent:
        sparql = sparql.replace(text, symbol)
    sparql = sparql.replace(" sep_dot ", ".")
    sparql = sparql.replace(" sep_semicolon ", ";")
    return sparql


def decode(sparql_encoded, prefixes):
    """Dada uma sparql que foi codificada pela função
    :func:`qapedia.utils.encode`. O método ``decode`` substuir os termos
    codificados por símbolos válidos da consulta sparql.

    Parameters
    ----------
    sparql_encoded : str
        sparql transformada após passar por :func:`qapedia.utils.encode`.
    prefixes : list
        lista de prefixos com uris utilizadas na sparql retornadas pela função
        :func:`qapedia.utils.convert_prefixes_to_list`.

    Returns
    -------
    str
        sparql com os símbolos válidos para uma consulta.

    Examples
    --------
    .. code-block:: python

        >>> from qapedia.utils import decode
        >>> from qapedia.utils import convert_prefixes_to_list
        >>> prefixes = "PREFIX prop: <http://dbpedia.org/property/>\\
        ...             PREFIX dbr: <http://dbpedia.org/resource/>"
        >>> list_of_prefixes = convert_prefixes_to_list(prefixes)
        >>> query_encoded = "ASK  bracket_open \\n\\
        ...         dbr_Amazon_River prop_length var_amazon  sep_dot \\n\\
        ...         dbr_Nile prop_length var_nile  sep_dot \\n\\
        ...         FILTER(var_amazon  greater_than  var_nile)  sep_dot  bracket_close "
        >>> print(decode(query_encoded, list_of_prefixes))
        ASK {
                dbr:Amazon_River prop:length ?amazon .
                dbr:Nile prop:length ?nile .
                FILTER(?amazon > ?nile) .}
    """
    sparql = sparql_encoded
    for prefix, _ in prefixes:
        encoding = prefix.replace(":", "_")
        sparql = sparql.replace(encoding, prefix)
    sparql = _encoded_symbols_to_symbols(sparql)
    return sparql
