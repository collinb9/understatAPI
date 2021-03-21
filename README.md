# understatAPI
This is a python API for scraping data from [understat.com](https://understat.com/). Understat is a website with football data for 6 european leagues for every season since 2014/15 season. The leagues available are the Premier League, La Liga, Ligue 1, Serie A, Bundesliga and the Russian Premier League. 

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

## Quick Start
---
**NOTE**

This package is in very early stages of development and the API is likely to change

---
The API contains endpoints which reflect the structure of the understat website. Below is a table showing the different endpoints and the pages on understat.com to which they correspond

| Endpoint         | Webpage                                         |
|------------------|-------------------------------------------------|
| UnderstatClient.league | https://understat.com/league/<league_name>      |
| UnderstatClient.team   | https://understat.com/team/<team_name>/<season> |
| UnderstatClient.player | https://understat.com/player/<player_id>        |
| UnderstatClient.match  | https://understat.com/player/<match_id>         |

Every function in the public API corresponds to one of tables visible on the understat webpage corresponding to the endpoint to which it belongs. Each function returns a pandas `DataFrame` with the relevant data. Below are some examples of using the API. Note how some the functions in the `league` and `team` endpoints can accept understandable strings as identifiers, but `player` and `match` must receive an id number.
```python
from understatapi import UnderstatClient

understat = UnderstatClient()
# get data for every player playing in the Premier League in 2019/20
league_player_data = understat.league.get_player_data(league="EPL", season="2019")
# Get the name and id of the player with the highest xG this season
# First we need to change the type of the 'xG' column, by default it is a string
league_player_data["xG"] = league_player_data["xG"].astype(float)
league_player_data = league_player_data.sort_values(by="xG", ascending=False)
player_id, player_name = league_player_data.iloc[0][["id", "player_name"]].values
# Get data for every shot this player has taken in a league match (for all seasons)
player_shot_data = understat.player.get_shot_data(player=player_id)
```

```python
from understatapi import UnderstatClient

understat = UnderstatClient()
# get data for every league match involving Manchester United
team_match_data = understat.team.get_match_data(team="Manchester_United", season="2019")
# get the id for the first match of the season
match_id = match_data.iloc[0]["id"]
# get the rosters for the both teams in that match
roster_data = understat.match.get_roster_data(match=match_id)
```
You can also use the `UnderstatClient` class as a context manager which persists some information about the session between request and closes the session after it has been used. This is the recommended way to interact with the API.
```python
from understatapi import UnderstatClient

with UnderstatClient() as understat:
    team_match_data = understat.team.get_match_data
```

There are some more examples here TODO: Add more examples and link to them
For a full API reference, see the documentation TODO: Add link to docs

## Contributing
If you find any bugs in the code or have any feature requests, please make an issue and I'll try to address it as soon as possible. If you would like to implement the changes yourself you can make a pull request
* Clone this repo `git clone git@github.com:collinb9/understatAPI`
* Create a branch to work off `git checkout -b descriptive_branch_name`
* Make and commit your changes
* Push your changes `git push`
* Come back to this page, and click on Pull requests -> New pull request

Before a pull request can be merged the code will have to pass a number of checks that are run using TravisCI. These checks are
* Check that the code has been formatted using [black](https://github.com/psf/black)
* Lint the code using [pylint](https://github.com/PyCQA/pylint)
* Check type annotations using [mypy](https://github.com/python/mypy)
* Run the unit tests and check that they have 100% coverage

These checks are in place to ensure a consistent style and quality across the code. To check if the changes you have made will pass these tests run
```bash
pip install -r requirements.txt
pip install -r test_requirments.txt
chmod +x ./run_tests.sh
./run_tests.sh
```

Don't let these tests deter you from making a pull request. Make the changes to introduce the new functionality/bug fix and then I will be happy to help get the code to a stage where it passes the tests.

## Versioning
The versioning for this project follows the [semantic versioning](https://semver.org/) conventions.

# TODO
* Add functionality for using the search bar on understat
* Make `APIClient` a context manager that allows you to persist a session
* Creat an async API along with the current synchronous one
