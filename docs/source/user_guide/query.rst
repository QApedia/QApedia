Realizando uma consulta
-----------------------
Uma busca pode ser feita utilizando dois métodos presentes no QApedia, sendo
eles o :func:`QApedia.generator.perform_query` e o
:func:`QApedia.generator.get_results_of_generator_query`. O primeiro pode ser
utilizado com qualquer consulta SPARQL, o segundo utiliza o primeiro método,
mas antes ele ajusta a *generator_query* com a função explicada na seção
:doc:`adjust`. Como o resultado é grande, vamos apenas imprimir o tamanho da
lista gerada e um exemplo.

.. code-block:: python

    >>> from QApedia import generator
    >>> query = "select distinct ?a ?b where {\
    ...         ?uri <http://dbpedia.org/property/notableworks> ?a .\
    ...         ?uri <http://dbpedia.org/property/notableworks> ?b .\
    ...         ?uri a <http://dbpedia.org/ontology/Writer>}"
    >>> results = generator.perform_query(query)
    >>> len(results)
    10000
    >>> results[15]
    {'a': Value(typed-literal:'Petty Crimes'), 'b': Value(typed-literal:'New and Selected Poems')}
