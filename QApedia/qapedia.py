"""Realiza a geração de pares questão-sparql a partir de um arquivo de
templates previamente estabelecido.

Usage:
------
    $ qapedia [-h] [-tfile TFILE] [-o OUTPUT] [-d DELIMITER] [-n NUMBER]
    [-p PREFIXES] [-e ENDPOINT] [-l LANG] [-v VERBOSE]

As opções disponíveis são:

    -tfile             Qualquer caminho de string válido é aceito. A string
                       pode ser uma URL, por exemplo. Esse caminho corresponde
                       ao arquivo contendo o conjunto de templates. Se nenhum
                       valor for passado, é executado um arquivo de exemplo.
    -o, --output       Corresponde ao caminho do arquivo de saída onde será
                       salvo os pares de questão-sparql gerados. Se nenhum
                       caminho for especificado, o resultado será salvo no
                       arquivo output.txt
    -h, --help         Mostra informações sobre os argumentos.
    -d, --delim        Delimitador usado para separar os campos do template.
                       (default: ';')
    -n, --number       Quantidade de pares gerados por template.
                       (default: 100)
    -p, --prefixe      Caminho do arquivo txt contendo os prefixos utilizados,
                       caso nenhum arquivo seja especificado são utilizados os
                       mesmos prefixos presentes em http://dbpedia.org/snorql/
    -e, --endpoint     URL do SPARQL endpoint.
                       (default http://dbpedia.org/sparql)
    -l, --lang         Idioma das questões do template. (default: 'pt')

Examples:
---------
::

    $ qapedia -tfile templates.csv --lang PT
    $ qapedia -h # exibe ajuda

Contact:
--------
Mais informações estão disponíveis em:
    - https://qapedia.readthedocs.io/
    - https://github.com/QApedia/QApedia
"""
# Standard library imports
import os
import argparse
import csv


__author__ = "Jessica Sousa"
__version__ = "v0.0.0-alpha"
__license__ = "MIT"


__doc__ += f"""
Version:
--------
- QApedia {__version__}
"""


_ROOT = os.path.abspath(os.path.dirname(__file__))


def _get_data(path):
    return os.path.join(_ROOT, "data", path)


def _make_parser():
    p = argparse.ArgumentParser()
    p.add_argument(
        "-tfile",
        help="Qualquer caminho de string válido é aceito. A string pode ser "
        "uma URL, por exemplo. Esse caminho corresponde ao arquivo contendo "
        "o conjunto de templates. Se nenhum valor for passado, é executado "
        "um arquivo de exemplo.",
        default=_get_data("example.csv"),
    )
    p.add_argument(
        "-o",
        "--output",
        help="Corresponde ao caminho do arquivo de saída onde será salvo os "
        "pares de questão-sparql gerados. Se nenhum caminho for especificado,"
        " o resultado será salvo no arquivo output.txt",
        default="output.txt",
    )
    p.add_argument(
        "-d",
        "--delim",
        help="Delimitador usado para separar os campos do template. "
        "(default: ';')",
        default=";",
    )
    p.add_argument(
        "-n",
        "--number",
        help="Quantidade de pares gerados por template. (default: 100)",
        type=int,
        default=100,
    )
    p.add_argument(
        "-p",
        "--prefixes",
        help="Caminho do arquivo txt contendo os prefixos utilizados, caso "
        "nenhum arquivo seja especificado são utilizados os mesmos prefixos"
        " presentes em http://dbpedia.org/snorql/",
        default=_get_data("prefixes.txt"),
    )
    p.add_argument(
        "-e",
        "--endpoint",
        help="URL do SPARQL endpoint. (default: 'http://dbpedia.org/sparql')",
        default="http://dbpedia.org/sparql",
    )
    p.add_argument(
        "-l",
        "--lang",
        help="Idioma das questões do template. (default: 'pt')",
        default="pt",
    )
    p.add_argument(
        "-v",
        "--verbose",
        help="Indica qual template está sendo executado atualmente.",
        type=bool,
        default=False,
    )
    return p


def _run():
    from QApedia import generator
    from QApedia import io

    parser = _make_parser()
    args = parser.parse_args()

    # Carregar lista de prefixos
    prefixes, list_of_prefixes = io.load_prefixes(args.prefixes)

    # Carregar arquivo contendo os templates
    templates = io.load_templates(args.tfile, args.delim)

    with open(args.output, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=args.delim)
        writer.writerow(["question", "sparql", "template_id"])
        for index, template in templates.iterrows():
            if args.verbose:
                print("Executando template da linha %d" % index)
            # Realizar a busca e construção dos pares questão-sparql
            pairs = generator.build_pairs_from_template(
                template,
                prefixes,
                list_of_prefixes,
                args.endpoint,
                args.number,
                args.lang,
            )
            for pair in pairs:
                writer.writerow([pair["question"], pair["sparql"], str(index)])
        csv_file.close()
