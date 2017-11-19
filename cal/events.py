from enum import Enum

import util

def utc_time_str(event, start=True):
    if start:
        return event.get('start', '').get('dateTime', '')
    else:
        return event.get('end', '').get('dateTime', '')

def utc_time(event, start=True):
    return util.convert_datetime(utc_time_str(event, start=start))

def eid(event):
    return event.get('id', None)

# assumes names are unique
def eids(events):
    return { eid(event): event for event in events if eid(event) is not None }

def diff_events(old_events, new_events):
    print('old', len(old_events))
    print('new', len(new_events))

    o_eids = eids(old_events)
    n_eids = eids(new_events)

    update = []
    add = []

    # if it's in the new, but not in the old
    # we want to add it
    for e in new_events:
        if eid(e) is None:
            continue

        if eid(e) in o_eids:
            if 'sequence' in e:
                e['sequence'] = o_eids[eid(e)]['sequence']

            update.append(e)
        else:
            add.append(e)

    # if it's in the old, but not in the new
    # we want to delete it
    remove = []
    for e in old_events:
        # don't remove already deleted event
        if eid(e) is None or e.get('status', '') == 'cancelled':
            continue

        if not eid(e) in n_eids:
            remove.append(e)

    return add, remove, update
