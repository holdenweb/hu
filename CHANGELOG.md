# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Work since 1.0.0. The `ObjectDict` redesign below is a backwards-incompatible
change, so the next stable release should be **2.0.0** rather than 1.0.1.

### ⚠ Breaking changes

- **`ObjectDict` no longer subclasses `dict`.** It is now a composition wrapper
  that wraps nested values lazily and shares the underlying data. Practical
  consequences for callers:
  - `ObjectDict` instances are no longer `dict` instances
    (`isinstance(od, dict)` is `False`), and `json.dumps(od)` no longer works
    directly — use `od.to_dict()`.
  - The polymorphic constructor is gone: `ObjectDict` now takes a mapping (or an
    iterable of pairs). `ObjectDict(42)`, `ObjectDict("x")` and
    `ObjectDict([...])` are no longer special-cased; lists are wrapped on access
    as `ObjectList` instead.
  - Inherited dict methods (`.keys()`, `.values()`, `.items()`, `.get()`, …) are
    no longer present as methods. Iterate the object for its keys, use
    membership/`len()`, or call `to_dict()`. (This is deliberate: it is what
    lets keys named like dict methods be reached as attributes.)
- **Minimum supported Python is now 3.10** (3.9 reached end of life).

### Added

- `ObjectDict.to_dict()` returns a plain, detached `dict` (e.g. for
  `json.dumps`).
- `ObjectList`, a lazy list view that wraps elements on access and writes
  through to the underlying list; exported from the package.
- `DottedDict.get(key, default=None)` and `in` membership tests, both path-aware:
  a path that does not resolve yields the default / `False` instead of raising.
- Regression test suites covering the bugs fixed below.
- The Sphinx documentation source is now tracked in version control.

### Changed

- `ObjectDict` reimplemented as a lazy composition wrapper (see Breaking
  changes). Keys that clash with dict method names (`items`, `keys`, `get`, …)
  are now reachable as attributes, and mutations made through item assignment,
  `update`-style edits or list mutation stay consistent with attribute access.
- `DottedDict` error messages now quote the offending path, and the path parser
  no longer relies on shared mutable state between the generator and its
  consumer.
- Build tooling migrated from Poetry to **uv**, and `make` to **just**.
- Linting consolidated on **Ruff**, replacing flake8, black and
  reorder-python-imports.
- CI rewritten to use uv; the test matrix runs pypy3.10 and CPython 3.10–3.13.
- The package version is single-sourced from `pyproject.toml` and exposed at
  runtime via `importlib.metadata`.
- Dependabot switched from the `pip` ecosystem to `uv`.

### Fixed

- **Packaging:** installed wheels now expose the package as `hu`. Previously the
  build did not remap `src/hu`, so `import hu` failed after a normal install and
  only worked via a `PYTHONPATH` hack.
- `DottedDict.__delitem__` of a single-fragment key (e.g. `del dd["a"]`) raised
  `UnboundLocalError`.
- `ObjectDict.__delattr__` of a missing attribute silently returned an
  `AttributeError` instead of raising it.
- `DottedDict` lookups with an out-of-range list index, or a path fragment
  applied to the wrong type, now raise a clean `KeyError` instead of leaking a
  `TypeError`.

### Removed

- `semver` is no longer a runtime dependency (it is only used by the release
  script); `hu` now installs with no runtime dependencies.
- Dead and stray files: an empty `config.toml`, a duplicate Sphinx scaffold,
  committed build artifacts under `dist/`, and the redundant `version.py` /
  generated `_version.py`.

## [1.0.0] - 2024-12-30

- Baseline release: `ObjectDict` (attribute access over nested dicts) and
  `DottedDict` (path-string access over nested structures).
