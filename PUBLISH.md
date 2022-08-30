# Howto publish

Ensure that all required dependencies are installed:

```bash
pip3 install pip-tools build twine
```

Regenerate `requirements.txt` based on `pyproject.toml`, include development dependencies:

```bash
pip-compile --extra dev pyproject.toml
```

**(Optional)** Align virtualenv with update `requirements.txt` (will uninstall extra dependencies):

```bash
pip-sync
```

Build distribution:

```bash
python3 -m build
```

Check dist packages:

```bash
twine check dist/*

```

Upload distribution to PyPi (first on test environment, after that on production):

```bash
twine upload --verbose -r testpypi dist/*
twine upload --verbose -r pypi dist/*
```
