# Usage

## Installation

To use Trendlist, first install it with `pip`:

```console
(.venv) $ pip install trendlist
```

## Creating Trendy Lists

To create a list of powers
use the {py:func}`trendlist.pows` function:

```{eval-rst}
.. autofunction:: trendlist.pows
```
The `base` parameter should be of type {py:class}`int`.

To create a list of random floats `U[0, 1)`-distributed random {py:class}`float`s
use the {py:func}`trendlist.rands` function:

```{eval-rst}
.. autofunction:: trendlist.rands
```
the `seed` parameter should be of type {py:class}`float`.

For both functions, the parameters `n` and `start` should be of type {py:class}`int`.

Passing unexpected types to these functions will raise a {py:exc}`TypeError` exception.
