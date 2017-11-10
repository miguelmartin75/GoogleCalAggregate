# Google Calendar Aggregate

A simple script to aggregate (and maintain) multiple Google Calendars using the Google Calendar API.

# Features

- Place Events from multiple calendars into an output calendar
- Filter events from the source based off their name and time

# Usage

## Requirements

- python >= 3.6
- Google Calendar API installed

There's probably some others, but just use pip to install the rest pls.

## Configuration

Configuration is in the file `cal/config.py`, as I'm too lazy to make this JSON which would be easy to do but meh.

## Generate or Update

You can generate or update an aggregate calander by running:

```
python cal/main.py generate
```

## Generate/Update and Maintain

Instead of manually forcing an update, you can simply run let the script maintain the calendar for
you, which will run the script continuously until you have chosen to kill it. To do so, simply run:

```
python cal/main.py maintain
```
