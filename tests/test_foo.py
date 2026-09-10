from pathlib import Path

from markov_chain_haiku.foo import foo


def test_foo():
    assert foo("foo") == "foo"


def test_nltk_declared_as_project_runtime_dependency():
    pyproject_text = Path("pyproject.toml").read_text()
    assert "dependencies = [" in pyproject_text
    assert '"nltk>=3.9"' in pyproject_text
