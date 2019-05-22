import pytest
from qapedia.io import load_templates
import os


def test_load_templates():
    filepath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'fixtures/sample.csv',
    )
    assert type(load_templates(filepath)).__module__ == "pandas.core.frame"
    



