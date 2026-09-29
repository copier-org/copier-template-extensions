# SPDX-License-Identifier: ISC
#
# ISC License
#
# Copyright (c) 2021, Timothée Mazzucotelli and contributors
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""Tests for the `extensions` module."""

from pathlib import Path

import copier
import pytest
from copier.errors import UserMessageError

TEMPLATES_DIRECTORY = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize(
    ("template_name", "expected"),
    [
        ("not_using_loader", "not set"),
        ("using_loader", "True"),
        ("updating_context", "True"),
        ("modifying_context", "True"),
        ("not_updating_context_for_prompts", "True"),
        ("loading_normal_extension", "not set"),
        ("dataclass", "True"),
    ],
)
def test_extensions(tmp_path: Path, template_name: str, expected: str) -> None:
    """Test loader and context extensions.

    Arguments:
        tmp_path: A pytest fixture.
        template_name: The parametrized template to use.
        expected: The parametrized value we expect.
    """
    template_path = TEMPLATES_DIRECTORY / template_name
    copier.run_copy(str(template_path), tmp_path, defaults=True, overwrite=True, unsafe=True)
    result_file = tmp_path / "result.txt"
    assert result_file.exists()
    assert result_file.read_text() == f"Success variable: {expected}"


@pytest.mark.parametrize(
    ("template_name", "exception"),
    [
        ("raising_exception_while_loading", RuntimeError),
        ("cant_find_extension_file", UserMessageError),
        ("cant_find_extension_class", UserMessageError),
        ("cant_find_extension_module", UserMessageError),
        ("cant_find_extension_package", UserMessageError),
    ],
)
def test_extensions_raising_exceptions(tmp_path: Path, template_name: str, exception: type) -> None:
    """See what happens when an extension raises an exception.

    Arguments:
        tmp_path: A pytest fixture.
        template_name: The parametrized template to use.
        exception: The exception expected to be raised.
    """
    template_path = TEMPLATES_DIRECTORY / template_name
    with pytest.raises(exception):  # ty:ignore[invalid-argument-type]
        copier.run_copy(str(template_path), tmp_path, defaults=True, overwrite=True, unsafe=True)
    assert not (tmp_path / "result.txt").exists()
    assert not (tmp_path / "extensions.py").exists()


@pytest.mark.parametrize(
    "template_name",
    ["deprecation_warning_hook_return", "deprecation_warning_update_attr"],
)
def test_deprecated_usage(tmp_path: Path, template_name: str) -> None:
    """Test deprecation warnings.

    Arguments:
        tmp_path: A pytest fixture.
        template_name: The parametrized template to use.
    """
    template_path = TEMPLATES_DIRECTORY / template_name
    with pytest.warns(DeprecationWarning):  # noqa: PT030
        copier.run_copy(str(template_path), tmp_path, defaults=True, overwrite=True, unsafe=True)
    result_file = tmp_path / "result.txt"
    assert result_file.exists()
    assert result_file.read_text() == "Success variable: True"


def test_answer_access(tmp_path: Path) -> None:
    """Test accessing an answer.

    Arguments:
        tmp_path: A pytest fixture.
    """
    template_path = TEMPLATES_DIRECTORY / "answer_access"
    copier.run_copy(str(template_path), tmp_path, data={"foo": "bar"}, defaults=True, overwrite=True, unsafe=True)
    result_file = tmp_path / "result.txt"
    assert result_file.exists()
    assert result_file.read_text() == "Success variable: True"
