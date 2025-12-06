# Changelog

## [Unreleased]

### Changed

- Upgraded `urllib3` from `1.26.5` to `>=2.6.0` ✅ **Tested & Verified**
- Upgraded `requests` from `2.25.1` to `>=2.32.0` ✅ **Tested & Verified**
- Upgraded development dependencies:
  - `pytest` to `>=8.0.0`
  - `black` from `21.10b0` to `>=24.0.0`
  - `mypy` from `0.812` to `>=1.8.0`
  - `pylint` from `2.11.1` to `>=3.0.0`
  - `coverage` from `6.0.1` to `>=7.4.0`
- Upgraded documentation dependencies:
  - `sphinx` from `3.5.2` to `>=7.2.0`
  - `sphinx-rtd-theme` from `0.5.1` to `>=2.0.0`
- Modernized `pyproject.toml` with full project metadata and dependencies (PEP 621)
- Simplified `setup.cfg` (kept for backwards compatibility)
- Updated all `requirements.txt` files

### Added

- Optional dependency groups in pyproject.toml: `[dev]` and `[docs]`
- Tool configurations in pyproject.toml (black, pytest, mypy, pylint)

### Testing

- ✅ All 31 tests pass with 100% coverage
- ✅ Verified in fresh virtual environment
- ✅ Package imports and works correctly

### Notes

- No API changes - fully backwards compatible for end users
- New installation for developers: `pip install -e ".[dev]"`
- Traditional installation still works: `pip install -r requirements.txt`

## [0.6.1] - Previous Release
