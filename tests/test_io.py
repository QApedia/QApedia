import pytest
import qapedia.io
import os


def test_load_templates():
    filepath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'fixtures/sample.csv',
    )
    type = "pandas.core.frame"
    assert type(qapedia.io.load_templates(filepath)).__module__ == type
