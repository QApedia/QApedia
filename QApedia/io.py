"""Este módulo trata das operações relacionadas a leitura e escrita do
pacote ``QApedia``.

Neste módulo, pode-se encontrar as seguintes funções:

* load_templates - realiza a leitura do arquivo contendo o conjunto de
  templates utilizados para a geração de perguntas-queries.
* load_prefixes - realiza a leitura do arquivo contendo os prefixos utilizados
  pelas SPARQLs durante a consulta.
"""
from QApedia.utils import extract_variables
from QApedia.utils import convert_prefixes_to_list
from QApedia.generator import build_pairs_from_template
import pandas as pd
import csv

__all__ = ["load_templates", "load_prefixes"]


def load_templates(filepath, delimiter=";"):
    """A função load_templates, carrega o conjunto de templates a partir de um
    arquivo csv. O dado deve possuir um campo ``generator_query`` que servirá
    para realizar buscas que preencherão as lacunas presentes nos campos
    ``question`` e ``query``.

    Parameters
    ----------
    filepath : str
        Caminho do arquivo csv que contém os templates.
    delimiter : str, optional
        Indicar qual separador utilizado no arquivo, by default ';'

    Returns
    -------
    pd.DataFrame
        Retorna um dataframe contendo o conjunto de templates.

    Examples
    --------
    Exemplo contendo 14 templates sendo carregado através da função
    load_templates.

    .. code-block:: python

        >>> from QApedia.io import load_templates
        >>> filename = "sample.csv"
        >>> templates = load_templates(filename)
        >>> len(templates)
        14
        >>> templates.head()
                                                    query  ... variables
        0  <A> e <B> são os municípios vizinhos de que lu...  ...    [a, b]
        1                <A> e <B> pertencem a qual espécie?  ...    [a, b]
        2      <A> e <B> podem ser encontrados em qual país?  ...    [a, b]
        3            <A> e <B> é produzido por qual empresa?  ...    [a, b]
        4      <A> e <B> é o trabalho notável de qual autor?  ...    [a, b]

        [5 rows x 4 columns]

    """

    def get_variables(row):
        return extract_variables(row["generator_query"])

    templates = pd.read_csv(filepath, sep=delimiter)
    templates["variables"] = templates.apply(get_variables, axis=1)
    return templates


def load_prefixes(filepath):
    """Dado um arquivo txt contendo os prefixos utilizados na SPARQL, é
    devolvida uma string contendo os prefixos e uma lista de tuplas contendo
    os prefixos.

    Parameters
    ----------
    filepath : str
        Caminho do arquivo txt contendo o conjunto de prefixos.

    Returns
    -------
    tuple of str
        Uma tupla contendo os prefixos carregados na forma de string e uma
        lista de tuplas, onde a primeira posição é o nome dado ao URI e a
        segunda contém a URI correspondente.

    Examples
    --------

    .. code-block:: python

        >>> from QApedia.io import load_prefixes
        >>> filename = "prefixes.txt"
        >>> prefixes = load_prefixes(filename)
        >>> for uri_name, uri in prefixes[1]:
        ...     print(uri_name, uri)
        ...
        owl: http://www.w3.org/2002/07/owl#
        xsd: http://www.w3.org/2001/XMLSchema#
        rdfs: http://www.w3.org/2000/01/rdf-schema#
        rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#
        foaf: http://xmlns.com/foaf/0.1/
        dc: http://purl.org/dc/elements/1.1/
        dbpedia2: http://dbpedia.org/property/
        dbpedia: http://dbpedia.org/
        skos: http://www.w3.org/2004/02/skos/core#
    """
    f = open(filepath, "r")
    lines = f.readlines()
    f.close()
    prefixes = "\n".join(line.rstrip() for line in lines)
    list_of_prefixes = convert_prefixes_to_list(prefixes)
    return prefixes, list_of_prefixes
