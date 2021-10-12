[![Build Status](https://travis-ci.com/collinb9/understatAPI.svg?branch=master)](https://travis-ci.com/collinb9/understatAPI)
![PyPI](https://img.shields.io/pypi/v/understatapi)
![PyPI - License](https://img.shields.io/pypi/l/understatapi)

# understatAPI

This is a python API for scraping data from [understat.com](https://understat.com/). Understat is a website with football data for 6 european leagues for every season since 2014/15 season. The leagues available are the Premier League, La Liga, Ligue 1, Serie A, Bundesliga and the Russian Premier League.

---

**NOTE**

I am not affiliated with understat.com in any way

---

## Installation

To install the package run

```bash
pip install understatapi
```

If you would like to use the package with the latest development changes you can clone this repo and install the package

```bash
git clone git@github.com:collinb9/understatAPI understatAPI
cd understatAPI
python setup.py install
```

This package primarily uses the [requests](https://github.com/psf/requests) library for interacting with understat.com, but the method `UnderstatClient.search()`, which allows you to use the search bar, is implemented using [selenium](https://github.com/SeleniumHQ/selenium/tree/trunk/py).
If you wish to use this method then you will have to install [geckodriver](https://github.com/mozilla/geckodriver).

## Getting started

---

**NOTE**

This package is in early stages of development and the API is likely to change

---

The API contains endpoints which reflect the structure of the understat website. Below is a table showing the different endpoints and the pages on understat.com to which they correspond

| Endpoint               | Webpage                                           |
| ---------------------- | ------------------------------------------------- |
| UnderstatClient.league | `https://understat.com/league/<league_name>`      |
| UnderstatClient.team   | `https://understat.com/team/<team_name>/<season>` |
| UnderstatClient.player | `https://understat.com/player/<player_id>`        |
| UnderstatClient.match  | `https://understat.com/match/<match_id>`          |

Every mwthod in the public API corresponds to one of the tables visible on the understat page for the relevant endpoint.
Each method returns JSON with the relevant data. Below are some examples of how to use the API. Note how the `league()` and `team()` methods can accept the names of leagues and teams respectively, but `player()` and `match()` must receive an id number.

```python
from understatapi import UnderstatClient

understat = UnderstatClient()
# get data for every player playing in the Premier League in 2019/20
league_player_data = understat.league(league="EPL").get_player_data(season="2019")
# Get the name and id of one of the player
player_id, player_name = league_player_data[0]["id"], league_player_data[0]["player_name"]
# Get data for every shot this player has taken in a league match (for all seasons)
player_shot_data = understat.player(player=player_id).get_shot_data()
```

```python
from understatapi import UnderstatClient

understat = UnderstatClient()
# get data for every league match involving Manchester United in 2019/20
team_match_data = understat.team(team="Manchester_United").get_match_data(season="2019")
# get the id for the first match of the season
match_id = match_data[0]["id"]
# get the rosters for the both teams in that match
roster_data = understat.match(match=match_id).get_roster_data()
```

You can also use the `UnderstatClient` class as a context manager which closes the session after it has been used, and also has some improved error handling. This is the recommended way to interact with the API.

```python
from understatapi import UnderstatClient

with UnderstatClient() as understat:
    team_match_data = understat.team(team="Manchester_United").get_match_data()
```

For a full API reference, see [the documentation](https://collinb9.github.io/understatAPI/)

## Contributing

If you find any bugs in the code or have any feature requests, please make an issue and I'll try to address it as soon as possible. If you would like to implement the changes yourself you can make a pull request

- Clone the repo `git clone git@github.com:collinb9/understatAPI`
- Create a branch to work off `git checkout -b descriptive_branch_name`
- Make and commit your changes
- Push your changes `git push`
- Come back to the repo on github, and click on Pull requests -> New pull request

Before a pull request can be merged the code will have to pass a number of checks that are run using TravisCI. These checks are

- Check that the code has been formatted using [black](https://github.com/psf/black)
- Lint the code using [pylint](https://github.com/PyCQA/pylint)
- Check type annotations using [mypy](https://github.com/python/mypy)
- Run the unit tests and check that they have 100% coverage

These checks are in place to ensure a consistent style and quality across the code. To check if the changes you have made will pass these tests run

```bash
pip install -r requirements.txt
pip install -r test_requirments.txt
chmod +x ci/run_tests.sh
ci/run_tests.sh
```

Don't let these tests deter you from making a pull request. Make the changes to introduce the new functionality/bug fix and then I will be happy to help get the code to a stage where it passes the tests.

## Versioning

The versioning for this project follows the [semantic versioning](https://semver.org/) conventions.

## TODO

- Add asynchronous support
