import re

from util import time_now_str, convert_datetime
import config

def get_datetime_str(event):
    return event['start'].get('dateTime', event['start'].get('date'))

class Calander:
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

    def events(self, service):
        min_time = time_now_str()
        max_time = time_now_str(config.IGNORE_EVENTS_AFTER_WEEKS)

        events_res = service.events().list(calendarId=self.cal_id, timeMin=min_time, timeMax=max_time, singleEvents=True).execute()

        events = events_res.get('items', [])

        res = []
        for e in events:
            name = e['summary']
            start = convert_datetime(get_datetime_str(e))

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

            if self.time_range and len(self.time_range) >= 2:
                # if the start range is out of range, skip the event
                if start.time() < self.time_range[0] or start.time() > self.time_range[1]:
                    continue

            res.append(e)

        return res

class AggregateCal:
    cals = None
    service = None

    def __init__(self, service, cals, on_update_event, on_new_event, on_delete_event):
        self.cals = cals
        self.service = service
        self.output_cal = output_cal

    
    def events(self):
        # TODO
        return None

