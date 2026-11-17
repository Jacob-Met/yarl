"""WHATWG opaque paths preserve spaces except before query/fragment delimiters."""

import pytest

from yarl import URL


@pytest.mark.parametrize(
    ("input_url", "expected"),
    [
        ("non-special:opaque  ?hi", "non-special:opaque %20?hi"),
        ("non-special:opaque  #hi", "non-special:opaque %20#hi"),
        ("non-special:opaque  x?hi", "non-special:opaque  x?hi"),
        ("non-special:opaque  x#hi", "non-special:opaque  x#hi"),
        ("sc:foo bar", "sc:foo bar"),
        ("sc:foo%20bar", "sc:foo%20bar"),
        ("sc:foo  ", "sc:foo"),
        ("sc:foo  ?", "sc:foo %20?"),
        ("sc:foo #bar", "sc:foo%20#bar"),
        ("sc:foo%20?bar", "sc:foo%20?bar"),
        ("sc:foo  ?bar#baz", "sc:foo %20?bar#baz"),
        ("lolscheme:x x#x x", "lolscheme:x x#x%20x"),
        ("sc:a%20 b", "sc:a%20 b"),
    ],
)
def test_whatwg_opaque_path_spaces(input_url: str, expected: str) -> None:
    url = URL(input_url)
    assert str(url) == expected
    assert str(URL(str(url))) == expected


@pytest.mark.parametrize(
    ("input_url", "expected"),
    [
        ("sc://h/a b", "sc://h/a%20b"),
        ("sc:/a b", "sc:/a%20b"),
        ("https://h/a b", "https://h/a%20b"),
    ],
)
def test_opaque_path_spaces_do_not_change_other_grammars(
    input_url: str, expected: str
) -> None:
    assert str(URL(input_url)) == expected


def test_rfc_mode_rejects_literal_spaces() -> None:
    with pytest.raises(ValueError, match="RFC 3986"):
        URL("sc:opaque  x?hi", mode="rfc")


def test_preserve_explicit_encoded_opaque_path() -> None:
    source = "sc:foo  ?bar"
    assert str(URL(source, encoded=True)) == source
    assert str(URL.build(scheme="sc", path="foo bar")) == "sc:foo%20bar"
