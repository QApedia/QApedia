# <img alt="QApedia" src="docs/source/_static/logo.png" height="80">

[![Travis](https://img.shields.io/travis/QApedia/QApedia/master.svg?label=Travis%20CI)](
    https://travis-ci.org/QApedia/QApedia)
[![AppVeyor](https://ci.appveyor.com/api/projects/status/22bvm999anmdlyxv?svg=true)](https://ci.appveyor.com/project/JessicaSousa/qapedia)
[![Azure Pipelines](https://dev.azure.com/qapedia/QApedia/_apis/build/status/QApedia.QApedia?branchName=master)](https://dev.azure.com/qapedia/QApedia/_build/latest?definitionId=2&branchName=master)
[![codecov]( https://codecov.io/gh/QApedia/QApedia/branch/master/graph/badge.svg)](https://codecov.io/gh/QApedia/QApedia)
[![Documentation Status](https://readthedocs.org/projects/qapedia/badge/?version=latest)](https://qapedia.readthedocs.io/pt/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/QApedia/QApedia/master?filepath=examples)

O módulo ``QApedia`` foi desenvolvido em python e realiza a geração de pares de
questões-sparql com base em um template previamente estabelecido. Para saber
mais sobre o funcionamento do pacote, você pode ler sobre ele na [documentação](https://qapedia.readthedocs.io/pt/latest/).


## ⚙️ Instalando


Caso deseje, você pode realizar a instalação do módulo do ``QApedia``,
primeiramente, dentro da pasta do projeto, você pode executar o
``pip install .``. 

```console
foo@bar:~/QApedia$ pip install .
```

O Download do projeto se encontra disponível na aba [release](https://github.com/QApedia/QApedia/releases) do repositório atual nos formatos *tar.gz* e *zip*.

## 📚 Documentação

A documentação do ``QApedia`` se encontra disponível em [qapedia.rtfd.io](https://qapedia.readthedocs.io/pt/latest/).

Esse pacote contempla as seguintes operações:

* Permite a busca de uma consulta *SPARQL* em um endpoint especificado.
* Realiza a geração de pares de questões-sparql sobre a dbpedia a partir de um template previamente estabelecido.

## 📝 Exemplo inicial

Após ter instalado o QApedia, é possível executar um exemplo disponível no pacote para a geração de pares questão-sparql. No console abaixo, é definido uma quantidade máxima de dez pares por template e esse conjunto gerado é salvo no arquivo chamado "pares.csv".

```console
foo@bar:~$ qapedia -n 10 -v True -o pares.csv
Executando template da linha 0
Executando template da linha 1
Executando template da linha 2
Executando template da linha 3
Executando template da linha 4
foo@bar:~$ 
```

Para verificar as opções disponíveis no comando ``qapedia``, apenas coloque ``-h`` ou ``--help`` como argumento. Caso deseje criar um conjunto de pares para um arquivo específico, informe o caminho do arquivo contendo o conjunto de templates.

```console
foo@bar:~$ qapedia -tfile templates.csv -n 10 -v True -o pares.csv
```

 Você pode encontrar alguns exemplos de uso do QApedia nesse [link](examples).

## 🚧 Informações importantes

* Os pares gerados podem apresentar problemas de concordância. 
    * Por exemplo, em <Fulana foi autor de que?>, há o problema com o feminino, para resolver isso defina uma pergunta no feminino (autora) e filtre a busca pelo gênero.

* Consultas com problemas na estrutura, por exemplo, falta de "?" antes da variável retornarão a exceção ``"QueryBadFormed"``.

* Consultas que demandam um longo tempo de resposta no servidor serão automaticamente abortadas e uma exceção será capturada.

* A *generator_query* possui o formato SELECT ... WHERE, caso não esteja nesse formato, uma exceção é gerada informando que a consulta não é do tipo SELECT.

    * Não importa o que se encontra dentro do WHERE, contanto que esteja num formato válido.
    * As variáveis do tipo ?a ?b ?c .. ?y ?z são utilizadas no preenchimento das lacunas do par "questão-sparql", sendo elas equivalentes as campos \<A\> \<B\> \<C\> ... \<Y\> \<Z\> presente nesses pares.

## 📏 Testes

Os testes do pacote foram construídos utilizando o pytest e é possível verificá-los executando os seguintes comandos dentro da pasta do QApedia. 

```console
foo@bar:~/QApedia$ pip install pytest
foo@bar:~/QApedia$ pytest
```

