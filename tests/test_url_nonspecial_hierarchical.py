"""WHATWG hierarchical non-special URLs without an authority."""

import pytest

from yarl import URL


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("/a/./b", "/a/b"),
        ("/a/%2e/b", "/a/b"),
        ("/a/../b", "/b"),
        ("/a/%2e%2E/b", "/b"),
        ("/a/..", "/"),
        ("/a/../../b", "/b"),
        ("/a/..//b", "/.//b"),
        ("/a/..///b", "/.///b"),
    ],
)
def test_hierarchical_non_special_dot_segments(path: str, expected: str) -> None:
    raw = f"web+demo:{path}"
    result = f"web+demo:{expected}"
    parsed = URL(raw)
    assert str(parsed) == result
    # Builder methods quote literal percent signs; only parsing interprets
    # percent-encoded dot segments.
    built_result = f"web+demo:{path.replace('%', '%25')}" if "%" in path else result
    assert str(URL.build(scheme="web+demo", path=path)) == built_result
    assert str(URL("web+demo:/old").with_path(path)) == built_result
    assert str(URL(result)) == result


def test_non_special_double_slash_query_and_fragment() -> None:
    url = URL("web+demo:/a/..//b?q=1#f")
    assert str(url) == "web+demo:/.//b?q=1#f"
    assert url.query_string == "q=1"
    assert url.fragment == "f"
    assert str(url.with_path("/a/..//b", keep_query=True, keep_fragment=True)) == str(
        url
    )


@pytest.mark.parametrize("path", ["a/../b", "a/%2e%2e/b", "a/./b"])
def test_opaque_non_special_path_stays_rootless(path: str) -> None:
    assert str(URL(f"web+demo:{path}")) == f"web+demo:{path.replace('%2e%2e', '..')}"


def test_other_url_modes_not_renormalized() -> None:
    assert str(URL("/a/../b")) == "/a/../b"
    assert str(URL("web+demo:/a/../b", mode="rfc")) == "web+demo:/b"
    assert str(URL("web+demo:/a/../b", encoded=True)) == "web+demo:/a/../b"
    assert (
        str(URL.build(scheme="web+demo", path="/a/../b", encoded=True))
        == "web+demo:/a/../b"
    )
    assert (
        str(URL("web+demo:/a").with_path("/a/../b", encoded=True)) == "web+demo:/a/../b"
    )


def test_with_path_rootless_argument_is_absolute() -> None:
    assert str(URL("web+demo:/old").with_path("a/..//b")) == "web+demo:/.//b"
    assert str(URL("web+demo:/old").with_path("a/../b")) == "web+demo:/b"
