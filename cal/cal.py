import re

from util import time_now_str, convert_datetime
import config

import datetime
import pytz

def get_datetime_str(event, start=True):
    name = 'start'
    if not start:
        name = 'end'
    return event[name].get('dateTime', event[name].get('date'))

class Calendar:
    cal_id = None
    include_events = None
    exclude_events = None
    time_range = None

    def __init__(self, cal_id = None, include_events = [], exclude_events = [], time_range = None):
        self.cal_id = cal_id
        self.time_range = time_range

        self.include_events = []
        self.exclude_events = []
        for arr in [(include_events, self.include_events), (exclude_events, self.exclude_events)]:
            loop = arr[0]
            insert = arr[1]
            for pattern in loop:
                insert.append(re.compile(pattern))

    def events(self, service, deleted=False):
        max_time = time_now_str(config.IGNORE_EVENTS_AFTER_WEEKS)

        events_res = service.events().list(calendarId=self.cal_id, timeMax=max_time, singleEvents=False, maxResults=10000, showDeleted=deleted).execute()

        events = events_res.get('items', [])

        res = []
        for e in events:
            name = e.get('summary', None)

            if not deleted:
                if name is None:
                    continue

            start = convert_datetime(get_datetime_str(e))
            end = convert_datetime(get_datetime_str(e, start=False))

            # not sure what this is about, but wont work otherwise :/
            if e['id'][0] == '_':
                continue

            include = len(self.include_events) == 0
            for pattern in self.include_events:
                if pattern.search(name):
                    include = True
                    break

            for pattern in self.exclude_events:
                if pattern.search(name):
                    include = False
                    break

            if not include:
                continue

            try:
                start_local = config.LOCAL_TIMEZONE.localize(start)
                end_local = config.LOCAL_TIMEZONE.localize(end)
            except:
                start_local = start.astimezone(config.LOCAL_TIMEZONE)
                end_local = end.astimezone(config.LOCAL_TIMEZONE)

            if self.time_range is not None:
                if start_local == end_local:
                    if not (start_local.hour >= self.time_range[0] and start_local.hour <= self.time_range[1]):
                        continue
                else:
                    # 1D range intersection

                    # max begin
                    if self.time_range[0] > start_local.hour:
                        start_local = start_local.replace(hour=self.time_range[0], minute=0, second=0)

                    # min end
                    if self.time_range[1] < end_local.hour:
                        end_local = end_local.replace(hour=self.time_range[1], minute=0, second=0)

                    if end_local - start_local < datetime.timedelta(hours=config.MIN_HOURS_OUTSIDE_RANGE):
                        continue

            #print(name)
            res.append(e)

        return res

class AggregateCal:
    cals = []
    events = []

    def __init__(self, cals):
        self.cals = cals

    def events(self, service, deleted=False):
        res = []
        for c in self.cals:
            res.extend(c.events(service, deleted=deleted))
        return res
