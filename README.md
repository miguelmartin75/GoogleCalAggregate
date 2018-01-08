# Google Calendar Aggregate

A simple script to aggregate (and maintain) multiple Google Calendars using the Google Calendar API.

# Features

- Place Events from multiple calendars into an output calendar
- Filter events from the source based off their name and time

# Usage

## Requirements

- python >= 3.6
    - `pip install python-dateutil`
    - `pip install pytz`
- Google Calendar API installed
    - `pip install --upgrade google-api-python-client`
- Appropriate `client_secret.json` file with rights to write and read to a Google Cal in root
  directory

## Configuration

Configuration is in the file `cal/config.py`, as I'm too lazy to make this JSON which would be easy to do but meh.

## Update and Maintain

To run, simply run 

```
python cal/main.py
```

which will update your output calendar from the list of source calendars in `cal/config.py`.

# TODO

- Google App Engine
    - For autonomous updating and OAuth2

# Example

The default configuration aggregates calendars relating to _competitive programming_ from sources
such as topcoder, atcoder and codeforces. The events are filtered to range between 5AM to 12AM
Adelaide time (for the use of myself), and only SRMs and TCOs events from topcoder are considered.
