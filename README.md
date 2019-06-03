# <img alt="QApedia" src="docs/source/_static/logo.png" height="80">

[![Travis](https://img.shields.io/travis/QApedia/QApedia/master.svg?label=Travis%20CI)](
    https://travis-ci.org/QApedia/QApedia)
[![Build Status](https://dev.azure.com/qapedia/QApedia/_apis/build/status/QApedia.QApedia?branchName=master)](https://dev.azure.com/qapedia/QApedia/_build/latest?definitionId=2&branchName=master)
[![codecov]( https://codecov.io/gh/QApedia/QApedia/branch/master/graph/badge.svg)](https://codecov.io/gh/QApedia/QApedia)
[![Documentation Status](https://readthedocs.org/projects/qapedia/badge/?version=latest)](https://qapedia.readthedocs.io/pt/latest/?badge=latest)
[![GitHub license](https://img.shields.io/github/license/QApedia/QApedia.svg)](https://github.com/QApedia/QApedia/blob/master/LICENSE)
![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/QApedia/QApedia.svg)


O módulo ``QApedia`` foi desenvolvido em python e realiza a geração de pares de
questões-sparql com base em um template previamente estabelecido. Para saber
mais sobre o funcionamento do pacote, você pode ler sobre ele na [documentação](https://qapedia.readthedocs.io/pt/latest/).


## ⚙️ Instalando


Caso deseje, você pode realizar a instalação do módulo do ``QApedia``,
primeiramente, dentro da pasta do projeto, você deverá instalar os
``requirements.txt`` caso não possua as bibliotecas necessárias para executar o
``QApedia``. Em seguida no diretório do QApedia você pode executar o
``pip install .``.

```console
    foo@bar:~/QApedia$ pip install -r requirements.txt
    foo@bar:~/QApedia$ pip install .
```

## 📚 Documentação

A documentação do ``QApedia`` se encontra disponível em qapedia.rtfd.io.

Esse pacote contempla as seguintes operações:

* Permite a busca de uma consulta *SPARQL* em um endpoint especificado.
* Realiza a geração de pares de questões-sparql sobre a dbpedia a partir de um template previamente estabelecido.

## 📝 Exemplo de uso


Ao acessar o link http://dbpedia.org/sparql, você é levado a seguinte tela do
Endpoint SPARQL Virtuoso. Alguns dos formatos dos resultados gerados através da
busca SPARQL estão mostrados na figura abaixo.

![Virtuoso SPARQL Endpoint](docs/source/_static/SPARQL_Query_Editor.png)


No ``QApedia``, o resultado de uma consulta pode ser obtido no formato json
nesse endpoint através da função
``QApedia.generator.get_results_of_generator_query``, no python ele é exibido
no formato dicionário, conforme mostrado no bloco de código a seguir.

```python
>>> from QApedia import generator
>>> template = {"question": "latitude de <A>",
...             "query": "select ?a where { <A> geo:lat ?a }",
...             "generator_query": "select distinct(?a) where"\
...             "{ ?a geo:lat [] }",
...             "variables": ["a"]}
>>> results = generator. get_results_of_generator_query(
...                         template["generator_query"],
...                         template["variables"],
...                         endpoint = "http://dbpedia.org/sparql")
>>> print(type(results))
<class 'dict'>
```
Com o resultado obtido em cima da ``generator_query``, a construção dos pares
questões-sparql podem ser realizados ao chamar a função
``QApedia.generator.extract_pairs``, o resultado será exibido como uma lista de
dicionários, onde cada um deles conterá as chaves ``question`` e ``sparql``.

```python
>>> from QApedia import generator
>>> template = {"question": "latitude de <A>",
...             "query": "select ?a where { <A> geo:lat ?a }",
...             "generator_query": "select distinct(?a) where"\
...             "{ ?a geo:lat [] }",
...             "variables": ["a"]}
>>> results = generator.get_results_of_generator_query(
...                     template["generator_query"],
...                     template["variables"],
...                     endpoint = "http://dbpedia.org/sparql")
>>> pairs = generator.extract_pairs(results["results"]["bindings"], template)
>>> len(pairs)
600
>>> "sparql" in pairs[0]
True
>>> "question" in pairs[0]
True
```