from QApedia import qapedia
import pytest
from argparse import Namespace


def parser_test_data():
    test1 = (
        ["-n 20"],
        Namespace(
            delim=";",
            endpoint="http://dbpedia.org/sparql",
            lang="pt",
            number=20,
            output="output.txt",
            prefixes=qapedia._get_data("prefixes.txt"),
            tfile=qapedia._get_data("example.csv"),
            verbose=False,
        ),
    )

    test2 = (
        ["-n 10", "-opairs.csv"],
        Namespace(
            delim=";",
            endpoint="http://dbpedia.org/sparql",
            lang="pt",
            number=10,
            output="pairs.csv",
            prefixes=qapedia._get_data("prefixes.txt"),
            tfile=qapedia._get_data("example.csv"),
            verbose=False,
        ),
    )

    test3 = (
        [],
        Namespace(
            delim=";",
            endpoint="http://dbpedia.org/sparql",
            lang="pt",
            number=100,
            output="output.txt",
            prefixes=qapedia._get_data("prefixes.txt"),
            tfile=qapedia._get_data("example.csv"),
            verbose=False,
        ),
    )

    return [test1, test2, test3]


def test_parser_argument_error():
    # Testar a passagem inválida de argumentos
    parser = qapedia._make_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["-file", ""])


@pytest.mark.parametrize("params, expected", parser_test_data())
def test_parser(params, expected):
    parser = qapedia._make_parser()
    args = parser.parse_args(params)
    assert args == expected
