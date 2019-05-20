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
    >>> generator_query = "select distinct ?a where { ?uri <http://dbpedia.org/ontology/author> ?a }"
    >>> variables = extract_variables(generator_query)
    >>> print(variables)
    ['a']
    """
    var = re.findall('^(.+?)where', generator_query, re.IGNORECASE)
    if var:
        var = re.findall('\?(\w)', var[0])
    if not var:
        return None
    return var


def extract_elements(line, fields):
    """Extrai um conjunto formado de pares e valores presentes em cada linha.

    Parameters
    ----------
    line : list
        Lista contendo os elementos que representando cada valor de ``fields``.     
    fields : list
        Termos que identificam cada elemento presente na linha.

    Returns
    -------
    dict 
        Dicionário representando o par identificador: elemento.

    Examples
    --------
    >>> fields = ['question','query','generator_query']
    >>> line = ['<A> escreveu qual livro?',
    ... 'SELECT DISTINCT ?uri where { ?uri <http://dbpedia.org/ontology/author> <A> }',
    ... 'select distinct ?a where { ?uri <http://dbpedia.org/ontology/author> ?a }']
    >>> extract_elements(line, fields)
    {'question': '<A> escreveu qual livro?', 'query': 'SELECT DISTINCT ?uri where { ?uri 
    <http://dbpedia.org/ontology/author> <A> }', 'generator_query': 'select distinct ?a 
    where { ?uri <http://dbpedia.org/ontology/author> ?a }', 'variables': ['a']}
    """
    if "generator_query" not in fields:
        return None
    if len(line) != len(fields):
        return None
    line = {fields[idx]: elm for idx, elm in enumerate(line)}
    line['variables'] = extract_variables(line["generator_query"])
    return line
