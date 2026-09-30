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

<div id="premium-sponsors" style="text-align: center;">

<div id="silver-sponsors"><b>Silver sponsors</b><p>
<a href="https://fastapi.tiangolo.com/"><img alt="FastAPI" src="https://raw.githubusercontent.com/tiangolo/fastapi/master/docs/en/docs/img/logo-margin/logo-teal.png" style="height: 200px; "></a><br>
</p></div>

<div id="bronze-sponsors"><b>Bronze sponsors</b><p>
<a href="https://www.nixtla.io/"><picture><source media="(prefers-color-scheme: light)" srcset="https://www.nixtla.io/img/logo/full-black.svg"><source media="(prefers-color-scheme: dark)" srcset="https://www.nixtla.io/img/logo/full-white.svg"><img alt="Nixtla" src="https://www.nixtla.io/img/logo/full-black.svg" style="height: 60px; "></picture></a><br>
</p></div>
</div>

---

<div id="sponsors"><p>
<a href="https://github.com/ofek"><img alt="ofek" src="https://avatars.githubusercontent.com/u/9677399?u=386c330f212ce467ce7119d9615c75d0e9b9f1ce&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/samuelcolvin"><img alt="samuelcolvin" src="https://avatars.githubusercontent.com/u/4039449?u=42eb3b833047c8c4b4f647a031eaef148c16d93f&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/tlambert03"><img alt="tlambert03" src="https://avatars.githubusercontent.com/u/1609449?u=922abf0524b47739b37095e553c99488814b05db&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/ssbarnea"><img alt="ssbarnea" src="https://avatars.githubusercontent.com/u/102495?u=c7bd9ddf127785286fc939dd18cb02db0a453bce&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/femtomc"><img alt="femtomc" src="https://avatars.githubusercontent.com/u/34410036?u=f13a71daf2a9f0d2da189beaa94250daa629e2d8&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/cmarqu"><img alt="cmarqu" src="https://avatars.githubusercontent.com/u/360986?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/kolenaIO"><img alt="kolenaIO" src="https://avatars.githubusercontent.com/u/77010818?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/ramnes"><img alt="ramnes" src="https://avatars.githubusercontent.com/u/835072?u=3fca03c3ba0051e2eb652b1def2188a94d1e1dc2&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/machow"><img alt="machow" src="https://avatars.githubusercontent.com/u/2574498?u=c41e3d2f758a05102d8075e38d67b9c17d4189d7&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/BenHammersley"><img alt="BenHammersley" src="https://avatars.githubusercontent.com/u/99436?u=4499a7b507541045222ee28ae122dbe3c8d08ab5&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/trevorWieland"><img alt="trevorWieland" src="https://avatars.githubusercontent.com/u/28811461?u=74cc0e3756c1d4e3d66b5c396e1d131ea8a10472&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/MarcoGorelli"><img alt="MarcoGorelli" src="https://avatars.githubusercontent.com/u/33491632?u=7de3a749cac76a60baca9777baf71d043a4f884d&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/analog-cbarber"><img alt="analog-cbarber" src="https://avatars.githubusercontent.com/u/7408243?u=fe0e7bf2882d1c9c901a341c2502e1518466527a&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/OdinManiac"><img alt="OdinManiac" src="https://avatars.githubusercontent.com/u/22727172?u=36ab20970f7f52ae8e7eb67b7fcf491fee01ac22&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/rstudio-sponsorship"><img alt="rstudio-sponsorship" src="https://avatars.githubusercontent.com/u/58949051?u=0c471515dd18111be30dfb7669ed5e778970959b&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/schlich"><img alt="schlich" src="https://avatars.githubusercontent.com/u/21191435?u=6f1240adb68f21614d809ae52d66509f46b1e877&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/butterlyn"><img alt="butterlyn" src="https://avatars.githubusercontent.com/u/53323535?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/livingbio"><img alt="livingbio" src="https://avatars.githubusercontent.com/u/10329983?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/NemetschekAllplan"><img alt="NemetschekAllplan" src="https://avatars.githubusercontent.com/u/912034?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/EricJayHartman"><img alt="EricJayHartman" src="https://avatars.githubusercontent.com/u/9259499?u=7e58cc7ec0cd3e85b27aec33656aa0f6612706dd&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/15r10nk"><img alt="15r10nk" src="https://avatars.githubusercontent.com/u/44680962?u=f04826446ff165742efa81e314bd03bf1724d50e&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/activeloopai"><img alt="activeloopai" src="https://avatars.githubusercontent.com/u/34816118?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/roboflow"><img alt="roboflow" src="https://avatars.githubusercontent.com/u/53104118?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/cmclaughlin"><img alt="cmclaughlin" src="https://avatars.githubusercontent.com/u/1061109?u=ddf6eec0edd2d11c980f8c3aa96e3d044d4e0468&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/RapidataAI"><img alt="RapidataAI" src="https://avatars.githubusercontent.com/u/104209891?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/rodolphebarbanneau"><img alt="rodolphebarbanneau" src="https://avatars.githubusercontent.com/u/46493454?u=6c405452a40c231cdf0b68e97544e07ee956a733&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/theSymbolSyndicate"><img alt="theSymbolSyndicate" src="https://avatars.githubusercontent.com/u/111542255?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/blakeNaccarato"><img alt="blakeNaccarato" src="https://avatars.githubusercontent.com/u/20692450?u=bb919218be30cfa994514f4cf39bb2f7cf952df4&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/ChargeStorm"><img alt="ChargeStorm" src="https://avatars.githubusercontent.com/u/26000165?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/Cusp-AI"><img alt="Cusp-AI" src="https://avatars.githubusercontent.com/u/178170649?v=4" style="height: 32px; border-radius: 100%;"></a>
</p></div>


*And 4 more private sponsor(s).*

<!-- sponsors-end -->
