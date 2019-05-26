Realizando uma consulta
-----------------------
Uma busca pode ser feita utilizando dois métodos presentes no qapedia, sendo
eles o :func:`qapedia.generator.perform_query` e o
:func:`qapedia.generator.get_results_of_generator_query`. O primeiro pode ser
utilizado com qualquer consulta SPARQL, o segundo utiliza o primeiro método,
mas antes ele ajusta a *generator_query* com a função explicada na seção
:doc:`adjust`. Como o resultado é grande, vamos apenas imprimir o tamanho da
lista gerada e um exemplo.

.. code-block:: python

    >>> from qapedia import generator
    >>> query = "select distinct ?a ?b where {\
    ...         ?uri <http://dbpedia.org/property/notableworks> ?a .\
    ...         ?uri <http://dbpedia.org/property/notableworks> ?b .\
    ...         ?uri a <http://dbpedia.org/ontology/Writer>}"
    >>> results = generator.perform_query(query)
    >>> len(results["results"]["bindings"])
    10000
    >>> results["results"]["bindings"][5000]
    {'a': {'type': 'typed-literal', 'datatype': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#langString', 'value': 'Principles of the Criminal Law of Scotland'}, 'b': {'type': 'typed-literal', 'datatype': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#langString', 'value': 'History of Europe, 19 volumes'}}
