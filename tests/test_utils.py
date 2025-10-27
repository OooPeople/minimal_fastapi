import pytest
from app.utils import normalize_name

def test_normalize_name_basic():
    assert normalize_name("  Alice   Bob  ") == "Alice Bob"

def test_normalize_name_empty():
    assert normalize_name("   ") == ""

def test_normalize_name_type_error():
    with pytest.raises(TypeError):
        normalize_name(None)  # type: ignore[arg-type]
