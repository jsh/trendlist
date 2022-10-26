# Usage

## Installation

To use Trendlist, first install it with `pip`:

```console
(.venv) $ pip install trendlist
```

## Creating Trend objects

To create a list of powers
use the {py:func}`trendlist.pows` function:

```{eval-rst}
.. autofunction:: trendlist.pows
```
The `n` and `base` parameters should both be of type {py:class}`int`,
otherwise the function will raise a {py:exc}`TypeError` exception.
