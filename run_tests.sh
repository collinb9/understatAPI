black --check --line-length=79 understatapi/ test/ setup.py
pylint understatapi/ test/
mypy -p understatapi
coverage run -m unittest discover
coverage report --fail-under=100
