Carregando os templates
-----------------------

Carregue o pacote para poder utilizar suas funcionalidades

.. code-block:: python

    >>> import qapedia

Você pode carregar o dataset utilizando a função
:func:`qapedia.io.load_templates` presente no pacote. O arquivo do dataset
deve estar no formato csv, a primeira linha deve conter o nome das colunas.
Esses nomes devem ser os mesmos que são mostrados no :doc:`../tutorial`. São
eles:

* **query** - consulta SPARQL contendo uma lacuna no formato ``<LETTER>``.
* **question** - pergunta em linguagem natural contendo a mesma lacuna
  presente na *query*.
* **generator_query** - query utilizada para preencher as lacunas e assim
  permitir a geração do conjunto de ``question-query``.

+---------------------+---------------------+--------------------+
| question            | query               | generator_query    |
+=====================+=====================+====================+
|                     | select distinct ?uri| select distinct ?a |
+ <A> é autor de que? + where {             + where {            +
|                     | ?uri dbo:author <A>}| ?uri dbo:author ?a}|
+---------------------+---------------------+--------------------+

O template é carregado como um ``pandas.Dataframe``, então as operações de
Dataframe podem ser realizadas em cima do conjunto de dados. As variáveis
presentes no select da **generator_query** são extraídas no processo de
leitura do conjunto de dados e são disponibilizadas na coluna **variables**.

.. code-block:: python

    >>> from qapedia import io
    >>> templates = io.load_templates("templates.csv")
    >>> templates.head()
                                            question  ... variables
    0        <A> e <B> é produzido por qual empresa?  ...    [a, b]
    1  <A> e <B> é o trabalho notável de qual autor?  ...    [a, b]
    2         <A> e <B> são escritos por qual autor?  ...    [a, b]
    3                       <A> escreveu qual livro?  ...       [a]
    4          <A> pertence a qual partido político?  ...       [a]

    [5 rows x 4 columns]



