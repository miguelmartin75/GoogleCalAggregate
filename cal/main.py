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

    print("Removing events...")
    for e in remove:
        service.events().delete(calendarId=output.cal_id, eventId=e['id']).execute()

    print("Adding events...")
    for e in add:
        service.events().insert(calendarId=output.cal_id, body=e).execute()

    print("Updating events...")
    for e in update:
        service.events().update(calendarId=output.cal_id, eventId=events.eid(e), body=e).execute()

    print("Done")

    return remove, add, update

def update_cal(service):
    source = AggregateCal(config.CALANDERS_QUERY)
    output = config.CALENDAR_OUTPUT

    return update_diff(service, source, output)

def main(argv):
    credentials = config.get_creds()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    update_cal(service)

if __name__ == '__main__':
    main(sys.argv)
