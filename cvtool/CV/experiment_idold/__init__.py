import sys
import os

core = sys.modules.get('cvtool.core')
whoami = __file__.split('/')[-2:-1]

#####################

#### Take this out of each 
def create_meta(whoami, content,institution):
    current_date = core.stdout.yymmdd()
    user = core.stdout.get_user()

    return {
        "Header": {
            "CV_collection_modified": current_date,
            "CV_collection_version": core.stdout.get_github_version('WCRP-CMIP','CMIP6Plus_CVs'),
            "author": f'{user.get("user")} <{user.get("email")}>',
            "checksum": "md5: EDITEDITEDITEDITEDITEDITEDITEDIT",
            "institution_id": institution,
            "previous_commit": core.stdout.get_github_version('WCRP-CMIP','CMIP6Plus_CVs'),
            "specs_doc": "v6.3.0 (link TBC)"
        },
        whoami: content
        }

#####################



def create(optdata):
    this = core.io.get_current_function_name()
    print(whoami,this)
    optdata = optdata.get(this) or {}

    content = optdata.get('mipera')
    institution = optdata.get('institution')

    return create_meta(whoami, content, institution)
     
  



def update(jsn, optdata):
    this = core.io.get_current_function_name()
    optdata = optdata.get(this)
    if not optdata: 
        print ('nothing to update ', whoami)

    # we need something to update
    assert len(jsn) >= 0

    # update some of the metadata
    current_date = core.stdout.yymmdd()

    overwrite={"Header": {
        'updatetest': 'Yay!',
        "CV_collection_modified": current_date,
        "CV_collection_version": core.stdout.get_github_version('WCRP-CMIP', 'CMIP6Plus_CVs'),
        "previous_commit": core.stdout.get_github_version('WCRP-CMIP', 'CMIP6Plus_CVs'),
    }}

    optdata = core.io.combine(optdata,overwrite)

    return core.io.combine(jsn,optdata)