import cvtool.core as core
from copy import deepcopy


def generic_load_existing(cvloc, prefix,test,whoami,parse = None):
    fname = f"{cvloc}{prefix}{whoami}.json"
    core.io.exists(fname)
    load = core.io.json_read(fname)[whoami]
    
    if parse:
      load = parse(load)

    test(load)
    return load

def generic_add_new(cvloc, prefix, existing ,new,test):
    duplicates = [new_item for new_item in new if new_item in existing]

    assert not duplicates, f'Please remove duplicates from your activity "add" section. \nYou can put them in the "update" to instead.\n Duplicates: {duplicates}'

    test(new)
    existing.update(new)
    return existing

def generic_ammend(cvloc,prefix,existing,overwrite,test):
    
    # test the updated values
    ecopy = deepcopy(existing)
    ecopy.update(overwrite)
    existing = core.io.merge_entries(existing,overwrite,append = False)
    return existing
