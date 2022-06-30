import contextlib
import io
import pathlib
from typing import NamedTuple

import pytest
from typing_extensions import TypedDict

import dcargs


def test_basic_typeddict():
    class ManyTypesTypedDict(TypedDict):
        i: int
        s: str
        f: float
        p: pathlib.Path

    assert dcargs.cli(
        ManyTypesTypedDict,
        args=[
            "--i",
            "5",
            "--s",
            "5",
            "--f",
            "5",
            "--p",
            "~",
        ],
    ) == dict(i=5, s="5", f=5.0, p=pathlib.Path("~"))


def test_nested_typeddict():
    class ChildTypedDict(TypedDict):
        y: int

    class NestedTypedDict(TypedDict):
        x: int
        b: ChildTypedDict

    assert dcargs.cli(NestedTypedDict, args=["--x", "1", "--b.y", "3"]) == dict(
        x=1, b=dict(y=3)
    )
    with pytest.raises(SystemExit):
        dcargs.cli(NestedTypedDict, args=["--x", "1"])


def test_helptext_and_default_instance_typeddict():
    class HelptextTypedDict(TypedDict):
        """This docstring should be printed as a description."""

        x: int  # Documentation 1

        # Documentation 2
        y: int

        z: int
        """Documentation 3"""

    f = io.StringIO()
    with pytest.raises(SystemExit):
        with contextlib.redirect_stdout(f):
            dcargs.cli(HelptextTypedDict, default_instance={"z": 3}, args=["--help"])
    helptext = f.getvalue()
    assert HelptextTypedDict.__doc__ in helptext
    assert ":\n  --x INT     Documentation 1\n" in helptext
    assert "--y INT     Documentation 2\n" in helptext
    assert "--z INT     Documentation 3 (default: 3)\n" in helptext


def test_basic_namedtuple():
    class ManyTypesNamedTuple(NamedTuple):
        i: int
        s: str
        f: float
        p: pathlib.Path

    assert dcargs.cli(
        ManyTypesNamedTuple,
        args=[
            "--i",
            "5",
            "--s",
            "5",
            "--f",
            "5",
            "--p",
            "~",
        ],
    ) == ManyTypesNamedTuple(i=5, s="5", f=5.0, p=pathlib.Path("~"))


def test_nested_namedtuple():
    class ChildNamedTuple(NamedTuple):
        y: int

    class NestedNamedTuple(NamedTuple):
        x: int
        b: ChildNamedTuple

    assert dcargs.cli(
        NestedNamedTuple, args=["--x", "1", "--b.y", "3"]
    ) == NestedNamedTuple(x=1, b=ChildNamedTuple(y=3))
    with pytest.raises(SystemExit):
        dcargs.cli(NestedNamedTuple, args=["--x", "1"])


def test_helptext_and_default_namedtuple():
    class HelptextNamedTupleDefault(NamedTuple):
        """This docstring should be printed as a description."""

        x: int  # Documentation 1

        # Documentation 2
        y: int

        z: int = 3
        """Documentation 3"""

    f = io.StringIO()
    with pytest.raises(SystemExit):
        with contextlib.redirect_stdout(f):
            dcargs.cli(HelptextNamedTupleDefault, args=["--help"])
    helptext = f.getvalue()
    assert HelptextNamedTupleDefault.__doc__ in helptext
    assert ":\n  --x INT     Documentation 1\n" in helptext
    assert "--y INT     Documentation 2\n" in helptext
    assert "--z INT     Documentation 3 (default: 3)\n" in helptext


def test_helptext_and_default_instance_namedtuple():
    class HelptextNamedTuple(NamedTuple):
        """This docstring should be printed as a description."""

        x: int  # Documentation 1

        # Documentation 2
        y: int

        z: int
        """Documentation 3"""

    f = io.StringIO()
    with pytest.raises(SystemExit):
        with contextlib.redirect_stdout(f):
            dcargs.cli(
                HelptextNamedTuple,
                default_instance=HelptextNamedTuple(
                    # Sketchy, unsupported behavior...
                    x=None,  # type: ignore
                    y=None,  # type: ignore
                    z=3,
                ),
                args=["--help"],
            )
    helptext = f.getvalue()
    assert HelptextNamedTuple.__doc__ in helptext
    assert ":\n  --x INT     Documentation 1\n" in helptext
    assert "--y INT     Documentation 2\n" in helptext
    assert "--z INT     Documentation 3 (default: 3)\n" in helptext
