.. _installation:

Instalação
----------

A priori, para se utilizar o pacote do QApedia é necessário realizar a
instalação do mesmo. A instalação pode ser executada de dois modos:

Através das releases disponíveis no Github
'''''''''''''''''''''''''''''''''''''''''''

Em `Releases`_ há a versão compactada .zip e .tar.gz do código. No terminal,
caso escolha o formato .tar.gz, no ubuntu, podem ser realizadas as seguintes
operações:

.. code-block:: console

    foo@bar:~$ wget https://github.com/QApedia/QApedia/archive/0.2.2.tar.gz
    foo@bar:~$ tar -xvzf 0.2.2.tar.gz
    foo@bar:~$ cd QApedia-0.2.2/
    foo@bar:~/QApedia-0.2.2$ pip install .

Através do github
'''''''''''''''''

É possível instalar a versão mais atual disponível no Github através do
seguinte comando em seu terminal. É necessário possuir o _git_ instalado.

.. code-block:: console

    foo@bar:~$ pip install git+https://github.com/QApedia/QApedia.git


.. _Releases: https://github.com/QApedia/QApedia/releases
