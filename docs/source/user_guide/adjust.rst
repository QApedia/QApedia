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
*query* do respectivo template. Essa consulta irá retornar uma lista contendo
os URIS dos trabalhos notáveis *a* e *b* de cada escritor. Entretanto, para
preencher a lacuna da pergunta em linguagem natural, necessitamos do nome
desses recursos em linguagem natural, para isso, são extraídas a propriedade
**rdfs:label** de cada uma dessas URIs. A inserção do campo ``rdfs:label``
pode ser realizada usando :func:`qapedia.generator.adjust_generator_query`.

.. code-block:: python

    >>> from qapedia import generator
    >>> template = templates.iloc[1]
    >>> template
    question           <A> e <B> são os trabalhos notáveis de qual es...
    query              SELECT DISTINCT ?uri where { ?uri <http://dbpe...
    generator_query    select distinct ?a, ?b where { ?uri <http://db...
    variables                                                     [a, b]
    Name: 1, dtype: object
    >>> generator.adjust_generator_query(template["generator_query"],template["variables"] )
    "select distinct ?a, ?b ?la ?lb where {?a rdfs:label ?la. FILTER(lang(?la) = 'pt'). ?b rdfs:label ?lb. FILTER(lang(?lb) = 'pt').  ?uri <http://dbpedia.org/property/notableworks> ?a . ?uri <http://dbpedia.org/property/notableworks> ?b . ?uri a <http://dbpedia.org/ontology/Writer> }"
