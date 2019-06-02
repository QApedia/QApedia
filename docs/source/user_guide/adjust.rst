Ajustando a *query geradora*
----------------------------

Uma *generator_query* possui o seguinte formato::

    #<A> e <B> são os trabalhos notáveis de qual escritor?
    select distinct ?a ?b where {
        ?uri <http://dbpedia.org/property/notableworks> ?a .
        ?uri <http://dbpedia.org/property/notableworks> ?b .
        ?uri a <http://dbpedia.org/ontology/Writer>
    }

Onde *a* e *b* correspondem as lacunas *<A>* e *<B>* definidas na *questão* e
*query* do respectivo template. Nesse exemplo, a consulta irá retornar uma
lista contendo os URIS dos trabalhos notáveis *a* e *b* de cada escritor.
Entretanto, para preencher a lacuna da pergunta em linguagem natural,
necessitamos do nome desses recursos em linguagem natural, para isso, são
extraídas a propriedade **rdfs:label** de cada uma dessas URIs. As
*generator_query* definida em nosso template não possui esses campos, então
para isso pode ser utilizada a função
:func:`QApedia.generator.adjust_generator_query` que irá inserir as variáveis
``la`` e ``lb`` que correspondem as *labels* extraídas sobre cada recurso.

.. code-block:: python

    >>> from QApedia import generator
    >>> generator_query = "select distinct ?a ?b where {"\
    ...                   "?uri <http://dbpedia.org/property/notableworks> ?a . "\
    ...                   "?uri <http://dbpedia.org/property/notableworks> ?b . "\
    ...                   "?uri a <http://dbpedia.org/ontology/Writer> }"
    >>> variables = ["a", "b"]
    "select distinct ?a ?b ?la ?lb where {?a rdfs:label ?la. FILTER(lang(?la) = 'pt'). ?b rdfs:label ?lb. FILTER(lang(?lb) = 'pt'). ?uri <http://dbpedia.org/property/notableworks> ?a . ?uri <http://dbpedia.org/property/notableworks> ?b . ?uri a <http://dbpedia.org/ontology/Writer> }"
