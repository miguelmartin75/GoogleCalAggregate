from pathlib import Path

import httplib2

from oauth2client.file import Storage
from oauth2client import client
from oauth2client import tools

from cal import Calendar

from pytz import timezone

# general config
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Competitive Programming Event Cal Aggregate'
CRED_STORAGE_DIR = Path('.credentials')
CRED_STORAGE = CRED_STORAGE_DIR / 'cred.json'

# cal config
CALENDAR_OUTPUT = Calendar('2gjuv28dirnbr23vqfc61clloc@group.calendar.google.com')
IGNORE_EVENTS_AFTER_WEEKS = 52

LOCAL_TIMEZONE = timezone('Australia/Adelaide')

# 5am to 12am w.r.t the specified local timezone
GLOBAL_TIME_RANGE = (5, 24)

MIN_HOURS_OUTSIDE_RANGE = 1

CALANDERS_QUERY = [
    # topcoder
    Calendar('appirio.com_bhga3musitat85mhdrng9035jg@group.calendar.google.com', include_events=['SRM', 'TCO'], time_range=GLOBAL_TIME_RANGE),
    # atcoder
    Calendar('atcoder.jp_evjr135c62bddnpd26lotmdicg@group.calendar.google.com', time_range=GLOBAL_TIME_RANGE),
    # codeforces
    Calendar('k23j233gtcvau7a8ulk2p360m4@group.calendar.google.com', time_range=GLOBAL_TIME_RANGE),

    # codejam
    Calendar('google.com_jqv7qt9iifsaj94cuknckrabd8@group.calendar.google.com', time_range=GLOBAL_TIME_RANGE),

    # custom events
    Calendar('19hlpet55u1qlfh9e929lfpvpg@group.calendar.google.com'),
]

def get_creds():
    if not CRED_STORAGE_DIR.exists():
        CRED_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    store = Storage(str(CRED_STORAGE))
    credentials = store.get()
    print("got creds = {}".format(credentials))
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME

        flags = tools.argparser.parse_args(args=[])
        credentials = tools.run_flow(flow, store, flags=flags)

    return credentials
