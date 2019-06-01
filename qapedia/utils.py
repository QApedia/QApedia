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


__all__ = ['extract_variables', 'convert_prefixes_to_list']


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
