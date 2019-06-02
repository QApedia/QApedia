"""Este módulo trata das operações relacionadas a leitura e escrita do
pacote ``QApedia``.

Neste módulo, pode-se encontrar as seguintes funções:

* load_templates - realiza a leitura do arquivo contendo o conjunto de
  templates utilizados para a geração de perguntas-queries.
"""
from QApedia.utils import extract_variables
import pandas as pd

__all__ = ['load_templates']


def load_templates(filepath, delimiter=';'):
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
    def get_variables(row): return extract_variables(row["generator_query"])
    templates = pd.read_csv(filepath, sep=";")
    templates["variables"] = templates.apply(get_variables, axis=1)
    return templates
