import pytest
import QApedia.io
import os


def test_load_templates():
    filepath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'fixtures/sample.csv',
    )
    obj_type = "pandas.core.frame"
    assert type(QApedia.io.load_templates(filepath)).__module__ == obj_type


def test_load_prefixes():
    filepath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'fixtures/prefixes.txt',
    )
    assert type(QApedia.io.load_prefixes(filepath)) == tuple

