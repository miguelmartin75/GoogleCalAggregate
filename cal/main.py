import sys
import httplib2

from apiclient import discovery

import config
from util import convert_datetime

from cal import get_datetime_str, AggregateCal, Calander

import events

def print_help(argv):
    sys.stderr.write("Expected command\n")
    sys.stderr.write(argv[0] + " {maintain,update}\n")

def update_diff(service, source, output):
    add, remove, update = events.diff_events(output.events(service), source.events(service))
    for e in remove:
        service.events().delete(calendarId=output.cal_id, eventId=e['id']).execute()

    for e in add:
        service.events().insert(calendarId=output.cal_id, body=e).execute()

    for e in update:
        service.events().update(calendarId=output.cal_id, eventId=events.eid(e), body=e).execute()

def maintain(service, source, output):
    print("Maintain")
    for e in source.events(service):
        print(e)

def main(argv):
    if len(argv) <= 1:
        print_help(argv)
        sys.exit(1)

    credentials = config.get_creds()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    source = AggregateCal(config.CALANDERS_QUERY)
    output = config.CALENDAR_OUTPUT

    if sys.argv[1][0] == 'u':
        update_diff(service, source, output)
    elif sys.argv[1][0] == 'm':
        update_diff(service, source, output)
        maintain(service, source, output)
    else:
        print_help(argv)
        sys.exit(2)

if __name__ == '__main__':
    main(sys.argv)
