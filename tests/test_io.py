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
