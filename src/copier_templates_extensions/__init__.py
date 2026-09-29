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

"""Deprecated. Import from `copier-template-extensions` instead."""

# YORE: Bump 1: Remove file.

import warnings

from copier_template_extensions import ContextHook, TemplateExtensionLoader

__all__: list[str] = ["ContextHook", "TemplateExtensionLoader"]

warnings.warn(
    "`copier-templates-extensions` is renamed `copier-template-extensions`. "
    "Please use the new name, and replace every occurrence of "
    "`copier-templates-extensions` and `copier_templates_extensions` in your template with "
    "`copier-template-extensions` and `copier_template_extensions` respectively.",
    DeprecationWarning,
    stacklevel=2,
)
