from pathlib import Path

import httplib2

from oauth2client.file import Storage
from oauth2client import client
from oauth2client import tools

from cal import Calander

# general config
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Competitive Programming Event Cal Aggregate'
CRED_STORAGE_DIR = Path('.credentials')
CRED_STORAGE = CRED_STORAGE_DIR / 'cred.json'

# cal config
IGNORE_EVENTS_AFTER_WEEKS = 52
CALENDAR_INSERT = Calander('') # TODO

GLOBAL_TIME_RANGE = None

CALANDERS_QUERY = [
    # topcoder
    #Calander('appirio.com_bhga3musitat85mhdrng9035jg@group.calendar.google.com', include_events=['SRM', 'TCO'], time_range=GLOBAL_TIME_RANGE),
    # atcoder
    Calander('atcoder.jp_evjr135c62bddnpd26lotmdicg@group.calendar.google.com', time_range=GLOBAL_TIME_RANGE),
    # codeforces
    #Calander('k23j233gtcvau7a8ulk2p360m4@group.calendar.google.com', time_range=GLOBAL_TIME_RANGE),

    # codejam
    #Calander('google.com_jqv7qt9iifsaj94cuknckrabd8@group.calendar.google.com', time_range=GLOBAL_TIME_RANGE)
]

def get_creds():
    if not CRED_STORAGE_DIR.exists():
        CRED_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    store = Storage(str(CRED_STORAGE))
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME

        credentials = tools.run_flow(flow, store, None)

    return credentials
