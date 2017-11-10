import httplib2

from apiclient import discovery

import config
from util import convert_datetime

from cal import get_datetime_str

def main():
    credentials = config.get_creds()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    events = []

    for cal in config.CALANDERS_QUERY:
        for e in cal.events(service):
            events.append(e)

    for event in events:
        start = convert_datetime(get_datetime_str(e))
        print(start, event['summary'])

if __name__ == '__main__':
    main()
