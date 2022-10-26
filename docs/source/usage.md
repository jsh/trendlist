# Usage

## Installation

To use Trendlist, first install it with `pip`:

```console
(.venv) $ pip install trendlist
```

## Creating Trendy Lists

To create a list of powers
use the {py:func}`trendlist.pows` function.

The `base` parameter should be of type {py:class}`int`.

To create a list of random floats `U[0, 1)`-distributed random {py:class}`float`s
use the {py:func}`trendlist.rands` function.

The `seed` parameter should be of type {py:class}`float`.

For both functions, the parameters `n` and `start` should be of type {py:class}`int`.

Passing unexpected types to these functions will raise a {py:exc}`TypeError` exception.

 ```{eval-rst}
.. autosummary::
   :toctree: _autosummary
   :template: custom-module-template.rst
   :recursive:

   trendlist
```
