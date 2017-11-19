import sys
import httplib2

from apiclient import discovery

import config
from util import convert_datetime

from cal import get_datetime_str, AggregateCal, Calendar

import events

def update_diff(service, source, output):
    output_events = output.events(service, deleted=True)
    source_events = source.events(service)

    add, remove, update = events.diff_events(output_events, source_events)

    for e in remove:
        print(e['summary'])
        service.events().delete(calendarId=output.cal_id, eventId=e['id']).execute()

    print("Adding events...")
    for e in add:
        print(e['summary'])
        service.events().insert(calendarId=output.cal_id, body=e).execute()

    print("Updating events...")
    for e in update:
        print(e['summary'])
        service.events().update(calendarId=output.cal_id, eventId=events.eid(e), body=e).execute()

def main(argv):
    credentials = config.get_creds()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    source = AggregateCal(config.CALANDERS_QUERY)
    output = config.CALENDAR_OUTPUT

    update_diff(service, source, output)

if __name__ == '__main__':
    main(sys.argv)
