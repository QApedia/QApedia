"""Este script trata das operações relacionadas a leitura e escrita do
pacote ``qapedia``.

Este arquivo tem as seguintes funções:

* load_templates - realiza a leitura do arquivo contendo o conjunto de
    templates utilizados para a geração de perguntas-queries.
"""
from qapedia.utils import extract_elements
from csv import reader as csv_reader


def load_templates(filepath, delimiter=';'):
    """A função load_templates, carrega o conjunto de templates a partir de um
    arquivo csv.

    Parameters
    ----------
    filepath : str
        Caminho do arquivo csv que contém os templates.
    delimiter : str, optional
        Indicar qual separador utilizado no arquivo, by default ';'

    Returns
    -------
    list
        Retorna uma lista contendo os campos extraídos do arquivo:
        * question: pergunta em linguagem natural.
        * query: query correspondente a pergunta.
        * generator_query: query utilizada para preencher as lacunas presentes
        em 'question' e 'query'.
        * variables: corresponde as variáveis das lacunas.

    Examples
    --------
    >>> templates = load_templates('/home/jeca/Downloads/NSpMQueryTemplatesPT.csv')
    >>> len(templates)
    200
    >>> templates[7]
    {'question': '<A> e <B> podem ser encontrados em qual país?', 'query': 'SELECT DISTINCT ?uri where { <A> <http://
    dbpedia.org/ontology/locationCountry> ?uri . <B> <http://dbpedia.org/ontology/locationCountry> ?uri }', 'generato
    r_query': 'select distinct ?a, ?b where { ?a <http://dbpedia.org/ontology/locationCountry> ?uri . ?b <http://dbpe
    dia.org/ontology/locationCountry> ?uri }', 'variables': ['a', 'b']}
    """
    fields = ["question", "query", "generator_query"]
    def extract_values(line): return extract_elements(line, fields)

    with open(filepath, mode='r') as infile:
        reader = csv_reader(infile, delimiter=";")
        templates = [extract_values(line) for line in reader]
        return templates
