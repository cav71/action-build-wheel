from unittest import mock

import pytest

from action_build_wheel_support import builder

REFS = [
    (
        "cav71/lektor-ng/.github/workflows/beta.yml@refs/heads/beta/0.0.0",
        ("beta", "0.0.0"),
    ),
    (
        "cav71/lektor-ng/.github/workflows/release.yml@refs/heads/release/0.0.0",
        ("release", "0.0.0"),
    ),
    ("cav71/lektor-ng/.github/workflows/main.yml@refs/heads/main", ("main", None)),
    ("cav71/lektor-ng/.github/workflows/main.yml@refs/heads/some-branch", ("some-branch", None)),
    ("cav71/lektor-ng/.github/workflows/tags.yml@refs/tags/v0.0.0", (None, None)),
]


def test_rget():
    data = {}
    assert None == builder.rget(data, "")
    assert None == builder.rget(data, "x.y")
    assert {"b": 1} == builder.rget({"a": {"b": 1}}, "a")
    assert 1 == builder.rget({"a": {"b": 1}}, "a.b")
    assert None == builder.rget({"a": {"b": 1}}, "x.y")


def test_parse_ref():
    for branch, expected in REFS:
        found = builder.parse_ref(branch.rpartition("@")[2])
        assert expected == found


@pytest.mark.parametrize("modetxt", ["release", "post", "beta"])
def test_get_gdata_pyproject(loader, modetxt):
    pyproject = loader("sample-project/pyproject", "toml")

    mode = builder.ReleaseMode[modetxt.upper()]
    gdata = builder.get_gdata(mode, pyproject)
    assert {
        "name": "lektor-ng",
        "sha": None,
        "version": "0.0.0",
        "mode": mode,
        "number": None,
        "branch": None,
        "ref": None,
    } == gdata.__dict__

    expected = {
        "release": "0.0.0",
        "post": "0.0.0.post0",
        "beta": "0.0.0b0",
    }[mode]
    assert expected == gdata.version_string()


@pytest.mark.parametrize("modetxt", ["release", "post", "beta"])
def test_get_gdata_git(loader, modetxt):
    pyproject = loader("sample-project/pyproject", "toml")

    git = mock.MagicMock()
    git.sha.return_value = f"ABCDFE-{modetxt}"
    git.branch.return_value = f"my-branch-{modetxt}"
    git.default.return_value = "master-branch"

    mode = builder.ReleaseMode[modetxt.upper()]
    gdata = builder.get_gdata(mode, pyproject, git=git)
    assert {
        "name": "lektor-ng",
        "sha": f"ABCDFE-{modetxt}",
        "version": "0.0.0",
        "mode": mode,
        "number": None,
        "branch": f"my-branch-{modetxt}",
        "ref": f"refs/heads/my-branch-{modetxt}",
    } == gdata.__dict__

    expected = {
        "release": "0.0.0",
        "post": "0.0.0.post0",
        "beta": "0.0.0b0",
    }[mode]
    assert expected == gdata.version_string()


@pytest.mark.parametrize("modetxt", ["release", "beta"])
def test_get_gdata_gitdump(loader, modetxt):
    pyproject = loader("sample-project/pyproject", "toml")
    gitdump = loader(f"sample-project/{modetxt}.gitdump", "json")

    mode = builder.ReleaseMode[modetxt.upper()]
    gdata = builder.get_gdata(mode, pyproject, gitdump=gitdump)

    branch = {
        "release": "release/0.0.0",
        "beta": "beta/0.1.0",
    }[modetxt]
    sha = {
        "release": "e6606ae1e22b680fcc2d1e37f0a9ac30a0e5ab6e",
        "beta": "5effa07c2baaf03d71b23afaf823d1c7bf08fbc5",
    }[modetxt]
    assert {
        "name": "lektor-ng",
        "sha": sha,
        "version": "0.0.0",
        "mode": mode,
        "number": None,
        "branch": branch,
        "ref": f"refs/heads/{branch}",
    } == gdata.__dict__

    expected = {
        "release": "0.0.0",
        "post": "0.0.0.post0",
        "beta": "0.0.0b0",
    }[mode]
    assert expected == gdata.version_string()


def test_pypi(loader):
    data = loader("sample-project/pypi", "json")
    pypi = builder.pypi_parse_releases("lektor-ng", data)

    checks = {
        "versions": list,
        "releases": list,
        "betas": dict,
        "posts": dict,
        "category": dict,
    }
    assert list(checks) == list(pypi)
    for name, check in checks.items():
        assert isinstance(pypi[name], check)

    assert 0 == min(pypi["betas"]["0.0.2"])
    assert 16 == max(pypi["betas"]["0.0.2"])
    assert 17 == len(pypi["betas"]["0.0.2"])

    assert "betas" == pypi["category"]["0.0.0b13"]
    assert "releases" == pypi["category"]["0.0.0"]
    assert "posts" == pypi["category"]["0.0.0.post0"]

    assert ["0.0.0", "0.0.1"] == pypi["releases"]
    assert ["0.0.0", "0.0.1", "0.0.2"] == list(pypi["betas"])


@pytest.mark.parametrize("modetxt", ["release", "post", "beta"])
def test_pypi_numbered(loader, modetxt):
    mode = builder.ReleaseMode[modetxt.upper()]

    pypi = builder.pypi_parse_releases("lektor-ng", loader("sample-project/pypi", "json"))

    gdata = builder.GData("abcd", "xxxx", "0.0.0", mode=mode)

    expected = {
        "release": "0.0.0",
        "post": "0.0.0.post0",
        "beta": "0.0.0b0",
    }[mode]
    assert expected == gdata.version_string()

    assert 13 in pypi["betas"]["0.0.0"]
    assert 0 in pypi["posts"]["0.0.0"]
    gdata.update_number(pypi)
    expected = {
        "release": "0.0.0",
        "post": "0.0.0.post1",
        "beta": "0.0.0b14",
    }[mode]
    assert expected == gdata.version_string()


def test_variables(loader):
    pyproject = loader("sample-project/pyproject", "toml")
    gitdump = loader("sample-project/beta.gitdump", "json")

    gdata = builder.get_gdata(builder.ReleaseMode.RELEASE, pyproject, gitdump)

    assert {
        "branch": "beta/0.1.0",
        "mode": "release",
        "name": "lektor-ng",
        "ref": "refs/heads/beta/0.1.0",
        "sha": "5effa07c2baaf03d71b23afaf823d1c7bf08fbc5",
        "version": "0.0.0",
        "number": None,
    } == gdata.__dict__
