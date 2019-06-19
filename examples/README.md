# <img alt="QApedia" src="../docs/source/_static/logo.png" height="80">
## Exemplos de uso do QApedia

[![Documentation Status](https://readthedocs.org/projects/qapedia/badge/?version=latest)](https://qapedia.readthedocs.io/pt/latest/?badge=latest)
[![GitHub license](https://img.shields.io/github/license/QApedia/QApedia.svg)](https://github.com/QApedia/QApedia/blob/master/LICENSE)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/QApedia/QApedia/master?filepath=examples)

O módulo ``QApedia`` foi desenvolvido em python e realiza a geração de pares de
questões-sparql com base em um template previamente estabelecido. Para saber
mais sobre o funcionamento do pacote, você pode ler sobre ele na [documentação](https://qapedia.readthedocs.io/pt/latest/). Você pode executar os notebooks do exemplo de forma interativa
através do [binder](https://mybinder.org/v2/gh/QApedia/QApedia/master?filepath=examples).

Para exemplificar o uso da biblioteca, segue os tutoriais a seguir (gerados a partir de ipython notebooks):

* [Realizando consultas sparql com o qapedia](consultas_sparql.ipynb).
<!-- * Realizando consultas em mais de um idioma. -->

### 🚧 Informações importantes

* Os pares gerados podem apresentar problemas de concordância. 
    * Por exemplo, em <Fulana foi autor de que?>, há o problema com o feminino, para resolver isso defina uma pergunta no feminino (autora) e filtre a busca pelo gênero.

* Consultas com problemas na estrutura, por exemplo, falta de "?" antes da variável retornarão a exceção ``"QueryBadFormed"``.

* Consultas que demandam um longo tempo de resposta no servidor serão automaticamente abortadas e uma exceção será capturada.

* A *generator_query* possui o formato SELECT ... WHERE, caso não esteja nesse formato, uma exceção é gerada informando que a consulta não é do tipo SELECT.

    * Não importa o que se encontra dentro do WHERE, contanto que esteja num formato válido.
    * As variáveis do tipo ?a ?b ?c .. ?y ?z são utilizadas no preenchimento das lacunas do par "questão-sparql", sendo elas equivalentes as campos \<A\> \<B\> \<C\> ... \<Y\> \<Z\> presente nesses pares.
