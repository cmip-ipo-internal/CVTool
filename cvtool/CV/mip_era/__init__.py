
# import os

# def get_parent_file(module):
#     module_path = os.path.abspath(module.__file__)
#     parent_path = os.path.dirname(module_path)
#     return parent_path
# parent_file = get_parent_file(sys.modules[__name__])
# print(parent_file)

import sys
import os

core = sys.modules.get('cvtool.core')
meta = sys.modules.get('cvtool.CV.meta')
whoami = __file__.split('/')[-2]
info = core.stdout.log(whoami, level='info')


#####################
#  Main code
#####################



def create(optdata):
    this = core.io.get_current_function_name()
    print(whoami,this)
    optdata = optdata.get(this) or {}

    content = optdata.get('mipera')
    institution = optdata.get('institution')

    header = meta.create(institution)
    header[whoami] = content

    return  header



def update(jsn, optdata):
    this = core.io.get_current_function_name()
    optdata = optdata.get(this)
    if not optdata:
        info('nothing to update')
    # we need something to update
    assert len(jsn) >= 0
    # update some of the metadata
    current_date = core.stdout.yymmdd()

    overwrite = meta.update()

    optdata = core.io.combine(optdata, overwrite)

    return core.io.combine(jsn, optdata)
