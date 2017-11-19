from enum import Enum

import util

def utc_time_str(event, start=True):
    if start:
        return event['start']['dateTime']
    else:
        return event['start']['dateTime']

def utc_time(event, start=True):
    return util.convert_datetime(utc_time_str(event, start=start))

def eid(event):
    # concat the name and start/end time,
    # should be unique enough to uniquely identify the event
    return event['id']

# assumes names are unique
def eids(events):
    return [ eid(event) for event in events ]#, { eid(event): event for event in events }

def diff_events(old_events, new_events, erase_add_ids=True):
    o_eids = eids(old_events)
    n_eids = eids(new_events)

    update = []

    add = []
    # if it's in the new, but not in the old
    # we want to add it
    for e in new_events:
        if eid(e) in o_eids:
            # add the ID
            #e['id'] = events[eid(e)]['id']
            update.append(e)
        else:
            add.append(e)

    # if it's in the old, but not in the new
    # we want to delete it
    remove = []
    for e in old_events:
        if eid(e) not in n_eids:
            remove.append(e)

    return add, remove, update
