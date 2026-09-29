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

# Extension allowing to load other extensions using relative file paths.

from __future__ import annotations

import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import TYPE_CHECKING, Any

from copier.errors import UserMessageError
from jinja2 import Environment
from jinja2 import environment as jinja_env_module
from jinja2.ext import Extension

if TYPE_CHECKING:
    from types import ModuleType


class TemplateExtensionLoader(Extension):
    """Extension allowing to load other extensions using relative file paths."""

    def __init__(self, environment: Environment):
        """Initialize the object.

        Arguments:
            environment: The Jinja environment.
        """
        super().__init__(environment)
        # patch jinja's extension loading mechanism
        jinja_env_module.import_string = self._patched_import_string  # ty:ignore[invalid-assignment]

    def _patched_import_string(self, import_name: str, *, silent: bool = False) -> Any:
        try:
            return self._import_string(import_name)
        except Exception:
            if not silent:
                raise

    def _import_string(self, import_name: str) -> Any:
        if ":" in import_name:
            module_name, obj_name = import_name.split(":", 1)
            module = self._import_module(module_name, obj_name, try_filepath=True)
            return self._get_module_attribute(module, obj_name)

        if "." in import_name:
            module_name, _, obj_name = import_name.rpartition(".")
            module = self._import_module(module_name, obj_name)
            return self._get_module_attribute(module, obj_name)

        try:
            return __import__(import_name)
        except ImportError as error:
            raise UserMessageError(f"Could not import extension '{import_name}'") from error

    def _get_module_attribute(self, module: ModuleType, obj_name: str) -> Any:
        try:
            return getattr(module, obj_name)
        except AttributeError as error:
            raise UserMessageError(
                f"Module '{module.__name__}' does not have the '{obj_name}' attribute.\n"
                "Please report this issue to the template maintainers.",
            ) from error

    def _import_module(self, module_name: str, obj_name: str, *, try_filepath: bool = False) -> ModuleType:
        try:
            return __import__(module_name, None, None, [obj_name])
        except ImportError as error:
            if try_filepath:
                return self._import_template_module(module_name)
            raise UserMessageError(f"Could not import extension '{obj_name}' from '{module_name}'") from error

    def _import_template_module(self, relative_path: str | Path) -> ModuleType:
        module_name = Path(relative_path).stem
        for search_path in self.environment.loader.searchpath:  # ty:ignore[unresolved-attribute]
            template_relative_path = Path(search_path) / relative_path
            if template_relative_path.exists():
                break
        else:
            raise UserMessageError(
                f"Could not resolve path to local extension module '{relative_path}'\n"
                "Please report this issue to the template maintainers.",
            )
        spec = spec_from_file_location(
            module_full_name := f"copier_template_extensions.{module_name}",
            template_relative_path,
        )
        module = module_from_spec(spec)  # ty:ignore[invalid-argument-type]
        sys.modules[module_full_name] = module
        spec.loader.exec_module(module)  # ty:ignore[unresolved-attribute]
        return module
