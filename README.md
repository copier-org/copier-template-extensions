# Copier Template-Extensions

[![ci](https://github.com/copier-org/copier-template-extensions/workflows/ci/badge.svg)](https://github.com/copier-org/copier-template-extensions/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-zensical-FF9100.svg?style=flat)](https://copier-org.github.io/copier-template-extensions/)
[![pypi version](https://img.shields.io/pypi/v/copier-template-extensions.svg)](https://pypi.org/project/copier-template-extensions/)

Special Jinja2 extension for Copier that allows to load extensions using file paths relative to the template root instead of Python dotted paths.

## Installation

With pip:

```bash
pip install copier-template-extensions
```

With uv:

```bash
uv tool install copier --with copier-template-extensions
```

With pipx:

```bash
pipx install copier
pipx inject copier copier-template-extensions
```

## Usage

In your template configuration,
first add our loader extension,
then add your templates extensions
using relative file paths,
and the class name after a colon:

```yaml
_jinja_extensions:
- copier_template_extensions.TemplateExtensionLoader
- extensions/context.py:ContextUpdater
- extensions/slugify.py:SlugifyExtension
```

With this example, you are supposed to have an `extensions`
directory at the root of your template containing two modules:
`context.py` and `slugify.py`.

```
📁 template_root
├── 📄 abc.txt.jinja
├── 📄 copier.yml
└── 📁 extensions
    ├── 📄 context.py
    └── 📄 slugify.py
```

See [Context hook extension](#context-hook-extension)
to see how the `ContextUpdater` class can be written.

The `SlugifyExtension` class could be written like this:

```python
import re
import unicodedata

from jinja2.ext import Extension


# taken from Django
# https://github.com/django/django/blob/main/django/utils/text.py
def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


class SlugifyExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["slugify"] = slugify
```

### Context hook extension

This package also provides a convenient extension class
allowing template writers to update the context used
to render templates, in order to add, modify or remove
items of the context.

In one of your relative path extensions modules,
create a class that inherits from `ContextHook`,
and override its `hook` method:

```python
from copier_template_extensions import ContextHook


class ContextUpdater(ContextHook):
    def hook(self, context):
        context["say"] = "hello " + context["name"]
```

In your Jinja templates, you will now have access
to the `{{ say }}` variable directly.

This can be extremely useful in template projects
where you don't want to ask too many questions to the users
and instead infer some values from their answers.

Consider the following example:
you ask your users if they want to generate
a CLI app or a web API.
Depending on their answer,
the main Python module should be named
`cli.py` or `app.py`.

Without the context hook,
you would need to write a Jinja macro somewhere,
or update the context directly in Jinja,
and import this file (still using Jinja)
*in the filename of the module*:

```jinja
{# using macros #}
{%- macro module_name() %}
  {%- if project_type == "webapi" %}app{% else %}cli{% endif %}
{%- endmacro %}
```

```jinja
{# or enhancing the context #}
{#- Initiate context with a copy of Copier answers -#}
{%- set ctx = _copier_answers.copy() -%}

{#- Populate our new variables -#}
{%- set _ = ctx.update({"module_name": ("app" if project_type == "webapi" else "cli") -%}
```

```
📁 template_root
├── 📄 copier.yml
├── 📄 macros      # the macros file
├── 📄 context     # the context file
├── 📁 extensions
│   └── 📄 slugify.py
└── 📁 {{project_name|slugify}}
    │
    │   # using the macros
    ├── 📄 {% import 'macros' as macros with context %}{{macros.module_name()}}.py.jinja
    │
    │   # or using the enhanced context
    └── 📄 {% from 'context' import ctx with context %}{{ctx.module_name}}.py.jinja
```

As you can see, both forms are really ugly to write:

- the `macros` or `context` can only be placed in the root,
  as slashes `/` are not allowed in filenames
- you must use spaces and single-quotes
  (double-quotes are not valid filename characters on Windows)
  in your templated filenames, which is not clean
- filenames are very long

**Using our context hook instead makes it so easy and clean!**

```python
from copier_template_extensions import ContextHook


class ContextUpdater(ContextHook):
    def hook(self, context):
        context["module_name"] = "app" if context["project_type"] == "webapi" else "cli"
```

```
📁 template_root
├── 📄 copier.yml
├── 📁 extensions
│   ├── 📄 slugify.py
│   └── 📄 context.py
└── 📁 {{project_name|slugify}}
    └── 📄 {{module_name}}.py.jinja
```

You can do many more things with a context hook,
like downloading data from external resources
to include it in the context, etc.

> [!TIP]
> **Context hooks run during every Copier rendering phase.**
> During project generation or project updates, Copier passes
> through several rendering phases: when prompting (questions / answers),
> when rendering files, when running tasks, and when running migrations.
>
> By default, a context hook runs during all these phases,
> possibly multiple times, for example once per prompted question,
> or once per rendered file. The task of running the hook only once,
> or during a specific phase only, is left to you.
>
> To run only once, you can use caching within your class
> (for example by storing computed values in class variables).
>
> To run during a specific phase only, you can check the value
> of `context["_copier_phase"]` (Copier 9.6+), which is one of:
> `"prompt"`, `"render"`, `"tasks"`, `"migrate"`.
>
> Other key-value pairs can be found in the context
> that you might find useful (Copier configuration, etc.).

## Sponsors

<!-- sponsors-start -->
<!-- sponsors-end -->
