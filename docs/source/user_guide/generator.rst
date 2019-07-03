Geração de pares
------------------
A principal funcionalidade do pacote reside na geração de pares de
questão-sparql a partir de um template previamente estabelecido. Inicialmente,
suponha que temos o seguinte template. Neste template desejamos construir uma
lista de perguntas que contenha as obras do autor Yoshihiro Togashi.

Uma das perguntas possíveis seria:
"Yoshihiro Togashi é autor de Hunter × Hunter"?

+---------------------+----------------------+----------------------+
| question            | query                | generator_query      |
+=====================+======================+======================+
| Yoshihiro Togashi é | ask where {          | select distinct ?a   |
+ autor de <A>?       + <A> dbo:author       + where {              +
|                     | dbr:Yoshihiro_Togashi| ?a dbo:author        |
|                     | }                    | dbr:Yoshihiro_Togashi|
|                     |                      | }                    |
+---------------------+----------------------+----------------------+


Realizando a consulta
'''''''''''''''''''''

Esse template é definido como um dicionário, onde cada chave corresponde
ao nome da coluna, a chave *variables* corresponde as variáveis do tipo
``?letra`` localizadas entre *select* e o *where* da ``generator_query``.

.. code-block:: python

    >>> template = {"question": "Yoshihiro Togashi é autor de <A>?",
    ...             "query": "ask where { <A> dbo:author dbr:Yoshihiro_Togashi }",
    ...             "generator_query": "select distinct ?a where { ?a dbo:author dbr:Yoshihiro_Togashi }",
    ...             "variables": ["a"]}
    >>> gquery = template["generator_query"]
    >>> variables = template["variables"]

Dado esse template, inicialmente, iremos realizar o ajuste da
*generator_query* adicionando o *label* do recurso armazenado na variável *a*.
Para isso, realizamos a chamada da função de ajuste da ``generator_query``:

.. code-block:: python

    >>> from QApedia.generator import adjust_generator_query
    >>> gquery = adjust_generator_query(gquery, variables)
    >>> print(gquery)
    select distinct ?a ?la where {?a rdfs:label ?la. FILTER(lang(?la) = 'pt').  ?a dbo:author dbr:Yoshihiro_Togashi }

Em seguida, utilizamos a função de busca ``perform_query`` para
realizar essa consulta. A consulta é realizada sobre a base da DBpedia, então
não precisamos mudar valor padrão da função
``endpoint="http://dbpedia.org/sparql"``.

.. code-block:: python

    >>> from QApedia.generator import perform_query
    >>> results = perform_query(gquery)
    >>> for instance in results:
    ...     print("%s: %s" %(instance["la"].value, instance["a"].value))
    ...
    Level E: http://dbpedia.org/resource/Level_E
    Yu Yu Hakusho: http://dbpedia.org/resource/Yu_Yu_Hakusho
    Hunter × Hunter: http://dbpedia.org/resource/Hunter_×_Hunter

Outra forma de obter os resultados a partir da ``generator_query`` é
utilizando o método ``get_results_of_generator_query``.

.. code-block:: python

    >>> from QApedia.generator import get_results_of_generator_query
    >>> generator_query = "select distinct ?a where { ?a dbo:author dbr:Yoshihiro_Togashi }"
    >>> variables = ["a"]
    >>> results = get_results_of_generator_query(generator_query, variables)
    >>> for instance in results:
    ...     print("%s: %s" %(instance["la"].value, instance["a"].value))
    ...
    Level E: http://dbpedia.org/resource/Level_E
    Yu Yu Hakusho: http://dbpedia.org/resource/Yu_Yu_Hakusho
    Hunter × Hunter: http://dbpedia.org/resource/Hunter_×_Hunter

Construindo os pares
'''''''''''''''''''''
Para a geração dos pares de questão-sparql, utilizamos a função
``extract_pairs``, ela recebe como parâmetro:

* **resultado** da busca no formato retornado pelo exemplo anterior
* **template** da busca
* **quantidade de pares** que você deseja gerar, se a busca retornar mais do
  que esse valor, ela é limitada por essa quantidade.
* **lista de prefixos**, caso deseje que os recursos retornados no formato
  ``<http://dbpedia.org/...>`` sejam substituídos pelo prefixo especificado.

**Exemplo 1**

.. code-block:: python

    >>> from QApedia.generator import extract_pairs
    >>> pairs = extract_pairs(results, template, 2)
    >>> for pair in pairs:
    ...     print(pair["question"])
    ...     print(pair["sparql"])
    ...     print("----")
    ...
    Yoshihiro Togashi é autor de Level E?
    ask where { <http://dbpedia.org/resource/Level_E> dbo:author dbr:Yoshihiro_Togashi }
    ----
    Yoshihiro Togashi é autor de Yu Yu Hakusho?
    ask where { <http://dbpedia.org/resource/Yu_Yu_Hakusho> dbo:author dbr:Yoshihiro_Togashi }
    ----

**Exemplo 2**

.. code-block:: python

    >>> from QApedia.generator import extract_pairs
    >>> from QApedia.utils import convert_prefixes_to_list
    >>> prefixes = "PREFIX dbr:<http://dbpedia.org/resource/>\
    ...             PREFIX dbo:<http://dbpedia.org/ontology/>"
    >>> list_of_prefixes = convert_prefixes_to_list(prefixes)
    >>> list_of_prefixes
    [('dbr:', 'http://dbpedia.org/resource/'), ('dbo:', 'http://dbpedia.org/ontology/')]
    >>> pairs = extract_pairs(results, template, 2, list_of_prefixes)
    >>> for pair in pairs:
    ...     print(pair["question"])
    ...     print(pair["sparql"])
    ...     print("----")
    ...
    Yoshihiro Togashi é autor de Level E?
    ask where { dbr:Level_E dbo:author dbr:Yoshihiro_Togashi }
    ----
    Yoshihiro Togashi é autor de Yu Yu Hakusho?
    ask where { dbr:Yu_Yu_Hakusho dbo:author dbr:Yoshihiro_Togashi }
    ----

Caso deseje substituir alguns símbolos da ``sparql`` por elementos textuais,
você pode fazer isso através da função ``encode``. Para retornar a sparql em
um formato válido, basta utilizar o método ``decode``.

.. code-block:: python

    >>> from QApedia.utils import encode, decode
    >>> for pair in pairs:
    ...     encoded = encode(pair["sparql"], list_of_prefixes)
    ...     decoded = decode(encoded, list_of_prefixes)
    ...     print(pair["question"])
    ...     print("====Encoded sparl====")
    ...     print(encoded)
    ...     print("====Decoded sparl====")
    ...     print(decoded)
    ...     print("----")
    Yoshihiro Togashi é autor de Level E?
    ====Encoded sparl====
    ask where  bracket_open  dbr_Level_E dbo_author dbr_Yoshihiro_Togashi  bracket_close
    ====Decoded sparl====
    ask where { dbr:Level_E dbo:author dbr:Yoshihiro_Togashi }
    ----
    Yoshihiro Togashi é autor de Yu Yu Hakusho?
    ====Encoded sparl====
    ask where  bracket_open  dbr_Yu_Yu_Hakusho dbo_author dbr_Yoshihiro_Togashi  bracket_close
    ====Decoded sparl====
    ask where { dbr:Yu_Yu_Hakusho dbo:author dbr:Yoshihiro_Togashi }
    ----
