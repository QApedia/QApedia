import pytest
import QApedia.io
import os


def test_load_templates():
    # Testar se os templates estão sendo carregados
    filepath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures/sample.csv"
    )
    obj_type = "pandas.core.frame"
    assert type(QApedia.io.load_templates(filepath)).__module__ == obj_type


def test_load_templates_failure():
    with pytest.raises(
        Exception, match=r"\[Errno 2\] File b.* does not exist:.*"
    ):
        QApedia.io.load_templates("arquivo_inexistente.csv")


def test_load_prefixes():
    # Testar se os prefixos estão sendo carregados
    filepath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures/prefixes.txt"
    )
    assert type(QApedia.io.load_prefixes(filepath)) == tuple


def test_load_prefixes_failure():
    with pytest.raises(Exception, match=r"\[Errno 2\].*"):
        QApedia.io.load_templates("arquivo_inexistente.txt")
