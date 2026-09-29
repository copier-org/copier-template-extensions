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

# Extension allowing to modify the Copier context.

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any

from jinja2.ext import Extension

if TYPE_CHECKING:
    from collections.abc import Callable, MutableMapping

    from jinja2 import Environment


_sentinel = object()


class ContextHook(Extension):
    """Extension allowing to modify the Copier context."""

    update: bool = _sentinel  # ty:ignore[invalid-assignment]
    """Deprecated attribute to indicate whether the context should be updated with the value returned by `hook`."""

    def __init__(extension_self: Extension, environment: Environment) -> None:  # noqa: N805
        """Initialize the object.

        Arguments:
            environment: The Jinja environment.
        """
        super().__init__(environment)  # ty:ignore[invalid-super-argument]

        class ContextClass(environment.context_class):  # ty:ignore[unsupported-base]
            def __init__(
                self,
                env: Environment,
                parent: dict[str, Any],
                name: str | None,
                blocks: dict[str, Callable],
                globals: MutableMapping[str, Any] | None = None,  # noqa: A002
            ):
                if extension_self.update is not _sentinel:  # ty:ignore[unresolved-attribute]
                    warnings.warn(
                        "The `update` attribute of `ContextHook` subclasses is deprecated. "
                        "The `hook` method should now always modify the `context` in place.",
                        DeprecationWarning,
                        stacklevel=1,
                    )
                if "_copier_conf" in parent and (context := extension_self.hook(parent)) is not None:  # ty:ignore[unresolved-attribute]
                    parent.update(context)
                    warnings.warn(
                        "Returning a dict from the `hook` method is deprecated. "
                        "It should now always modify the `context` in place.",
                        DeprecationWarning,
                        stacklevel=1,
                    )

                super().__init__(env, parent, name, blocks, globals)

        environment.context_class = ContextClass

    def hook(self, context: dict[str, Any]) -> dict[str, Any] | None:
        """Abstract hook. Does nothing.

        Override this method to either return
        a new context dictionary that will be used
        to update the original one,
        or modify the context object in-place.

        Arguments:
            context: The context to modify.

        Raises:
            NotImplementedError: This method must be overridden in a subclass,
                and instead return either the same context instance modified,
                or new context instance (dictionary).
        """
        raise NotImplementedError
