[![CI](https://github.com/jeke-deportivas/jeke-understat-scrapper/actions/workflows/ci.yml/badge.svg)](https://github.com/jeke-deportivas/jeke-understat-scrapper/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/jeke-understat-scrapper)](https://pypi.org/project/jeke-understat-scrapper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

# jeke-understat-scrapper

A Python API for scraping football data from [understat.com](https://understat.com/). Understat is a website with football data for 6 european leagues for every season since 2014/15 season. The leagues available are the Premier League, La Liga, Ligue 1, Serie A, Bundesliga and the Russian Premier League.

> This is a maintained fork of [understatapi](https://github.com/collinb9/understatAPI) with fixes for Understat's new AJAX-based data loading.

---

**NOTE**

This project is not affiliated with understat.com in any way

---

## Installation

```bash
pip install jeke-understat-scrapper
```

## Getting started

The API contains endpoints which reflect the structure of the understat website. Below is a table showing the different endpoints and the pages on understat.com to which they correspond

| Endpoint               | Webpage                                           |
| ---------------------- | ------------------------------------------------- |
| UnderstatClient.league | `https://understat.com/league/<league_name>`      |
| UnderstatClient.team   | `https://understat.com/team/<team_name>/<season>` |
| UnderstatClient.player | `https://understat.com/player/<player_id>`        |
| UnderstatClient.match  | `https://understat.com/match/<match_id>`          |

Every method in the public API corresponds to one of the tables visible on the understat page for the relevant endpoint.
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
match_id = team_match_data[0]["id"]
# get the rosters for the both teams in that match
roster_data = understat.match(match=match_id).get_roster_data()
```

You can also use the `UnderstatClient` class as a context manager which closes the session after it has been used, and also has some improved error handling. This is the recommended way to interact with the API.

```python
from understatapi import UnderstatClient

with UnderstatClient() as understat:
    team_match_data = understat.team(team="Manchester_United").get_match_data(season="2019")
```

## Contributing

If you find any bugs in the code or have any feature requests, please make an issue and I'll try to address it as soon as possible.

## Versioning

The versioning for this project follows the [semantic versioning](https://semver.org/) conventions.

## Credits

This package is based on the original [understatapi](https://github.com/collinb9/understatAPI) by collinb9.
