import re


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
    
        >>> generator_query = "select distinct ?a where { ?uri <http://dbpedia.org/ontology/author> ?a }"
        >>> variables = extract_variables(generator_query)
        >>> print(variables)
        ['a']
    """
    variables = re.findall('^(.+?)where', generator_query, re.IGNORECASE)
    if variables:
        variables = re.findall('\?(\w)', variables[0])
    if not variables:
        return None
    return variables

