"""Realiza a geração de pares questão-sparql a partir de um arquivo de
templates previamente estabelecido.

Examples:
---------
    $ QApedia
    $ QApedia -tfile templates.csv --lang PT

Contact:
--------
More information is available at:
- https://qapedia.readthedocs.io/
- https://github.com/QApedia/QApedia

Version:
--------
- QApedia v0.1.1-alpha

Arguments:
---------
"""
# Standard library imports
import os
import argparse
import csv

# QApedia imports
import QApedia
from QApedia import io
from QApedia import utils


_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_data(path):
    return os.path.join(_ROOT, "data", path)


def load_prefixes(filename):
    f = open(filename, "r")
    lines = f.readlines()
    f.close()
    prefixes = "\n".join(line.rstrip() for line in lines)
    return prefixes


def _make_parser():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "-tfile",
        help="Qualquer caminho de string válido é aceito. A string pode ser "
        "uma URL, por exemplo. Esse caminho corresponde ao arquivo contendo "
        "o conjunto de templates. Se nenhum valor for passado, é executado "
        "um arquivo de exemplo.",
        default=None,
    )
    p.add_argument(
        "-o",
        "--output",
        help="Corresponde ao caminho do arquivo de saída onde será salvo os "
        "pares de questão-sparql gerados. Se nenhum caminho for especificado,"
        " o resultado será salvo no arquivo output.txt",
        default=None,
    )
    p.add_argument(
        "-d",
        "--delimiter",
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
        default=None,
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
        help="Indica qual template está sendo " "executado atualmente.",
        type=bool,
        default=False,
    )
    return p


def main():
    parser = _make_parser()
    args = parser.parse_args()

    # Parâmetros defaults
    template_file = get_data("example.csv")
    prefixes_file = get_data("prefixes.txt")
    output_file = "output.txt"

    if args.tfile is not None:
        template_file = args.tfile
    if args.prefixes is not None:
        prefixes_file = args.prefixes
    if args.output is not None:
        output_file = args.output

    # Carregar lista de prefixos
    prefixes = load_prefixes(prefixes_file)
    list_of_prefixes = utils.convert_prefixes_to_list(prefixes)

    # Carregar arquivo contendo os templates
    templates = io.load_templates(template_file, args.delimiter)

    with open(output_file, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=args.delimiter)
        writer.writerow(["question", "sparql", "template_id"])
        for index, template in templates.iterrows():
            if args.verbose:
                print("Executando template da linha %d" % index)
            # Realizar a busca e construção dos pares questão-sparql
            results = QApedia.get_results_of_generator_query(
                template["generator_query"],
                template["variables"],
                prefixes=prefixes,
                endpoint=args.endpoint,
                lang=args.lang.lower(),
            )
            pairs = QApedia.extract_pairs(
                results,
                template,
                number_of_examples=args.number,
                list_of_prefixes=list_of_prefixes,
            )
            for pair in pairs:
                writer.writerow([pair["question"], pair["sparql"], str(index)])


if __name__ == "__main__":
    main()
