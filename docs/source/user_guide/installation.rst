.. _installation:

Instalação
----------

A priori, para se utilizar o pacote do QApedia é necessário realizar a
instalação do mesmo. Ela pode ser executada através de dois modos:

Através das releases
''''''''''''''''''''

Em `Releases`_ o download do código pode ser realizado através do zip ou
tar.gz. No terminal, para realizar a instalação, pode ser executar as
seguintes instruções:

.. code-block:: console

    foo@bar:~$ wget https://github.com/JessicaSousa/QApedia/archive/0.1.0.tar.gz
    foo@bar:~$ tar -xvzf 0.1.0.tar.gz
    foo@bar:~$ cd QApedia-0.1.0/
    foo@bar:~/QApedia-0.1.0$ pip install .

Através do github
'''''''''''''''''

Você pode pode realizar git clone no repositório e instalar usando os
comandos a seguir

.. code-block:: console

    foo@bar:~$ git clone https://github.com/JessicaSousa/qapedia.git
    foo@bar:~$ cd qapedia
    foo@bar:~/qapedia$ pip install .


.. Através do Python packages
.. ''''''''''''''''''''''''''

.. QApedia está disponível no PyPI e pode ser instalado usando o pip.

.. .. code-block:: sh

..    pip install qapedia

.. _Releases: https://github.com/JessicaSousa/QApedia/releases
