# ''' 
# Script to merge all the respective components of the CV directory.
# '''
# import ast
# # import importlib.util
# # import os
# # import re
# from glob import glob
# import shutil


# # import sys
# # import os

# # core = sys.modules.get('cvtool.core')
# import cvtool.core as core
# # from cvtool.CV.meta import institutions
# from cvtool.CVII.compliance.clean_up import prune

# print = core.stdout.debug_print


# # save eval of the variables files.
# with open(__file__.replace('.py', '-variables.py'), "r") as file:
#     script_code = file.read()
# try:
#     parsed_code = ast.parse(script_code, filename="variables.py", mode="exec")
#     exec(compile(parsed_code, filename="variables.py", mode="exec"))
# except Exception as e:
#     print("Error:", e)



# def create(directory, prefix, tables, institutions, outloc=None):

#     outloc = outloc or 'CVs'
#     cvdict = {'source_type': set()}
#     missing = []

#     # MSM: Comment out for testing purposes
#     if core.io.exists(f'{directory}{outloc}', False):
#         # Delete the directory
#         shutil.rmtree(f'{directory}{outloc}')

#     # WARN! Do not comment this out!
#     core.io.mkdir(f'{directory}{outloc}')

#     # structure comes from imported vars file 
#     for entry in structure:
#         file = f"{directory}{entry}.json"

#         if entry == 'table_id':
#             # print()
#             # MSM rstrip will strip off any occurrence of the characters given to it in the string, not the string itself
#             # cvdict[entry] = sorted([os.path.basename(table.rstrip('.json')) for table in glob(tables+'*') if re.search(frequencypattern, table) and '.json' in table])
#             # following block would get list from directory, but currently pointing at CMIP6 tables
#             # cvdict['table_id'] = []
#             # table_files = glob(tables+'*')
#             # for table_file in sorted(table_files):
#             #     table_name = re.search(r'\w+_(\w+)\.json', os.path.basename(table_file)).group(1)
#             #     cvdict['table_id'].append(table_name)
#             # Hard code to a single table
#             cvdict['table_id'] = [t.split('/')[-1].rstrip('.json') for t in glob(f'{tables}/Tables/*.json')]
#             # ['APmon']

#         elif core.io.exists(file, False):
#             cvdict[entry] = core.io.json_read(file)[entry]

#             if 'experiment_id' in entry:
#                 # this section updates the sources. We expect this to come afterwards, and therefore this should not throw an exception and should work as expected.


#                 cvdict['source_type'] = set(cvdict['source_type']).union(set(component for experiment in cvdict[entry].values() if "required_model_components" in experiment for component in experiment["required_model_components"]+experiment["additional_allowed_model_components"]))
     
                                
#                 if entry == 'experiment_id':

#                     cvdict[entry] = core.stdout.listify(cvdict[entry],['parent_experiment_id','parent)sub_experiment_id','parent_activity_id'])

#                     cvdict[entry] = core.stdout.notnull(cvdict[entry],['parent_experiment_id','parent)sub_experiment_id'], 'no parent')




#                 from cvtool.CV.compliance.experiment_id import test as experiment_test

#                 # experiment_test(cvdict)


#             if entry == 'source_id':
#                 # this section updates the institutions
#                 from cvtool.CV.compliance.source_id import test as source_test
#                 # source_test(cvdict)
#                 print('source test disabled')

#                 cvdict['institution_id'] = {i: f"{institutions[i]['indentifiers']['ror']} - {institutions[i]['indentifiers']['institution_name']}" for i in sorted(
#                     {component for source in cvdict[entry].values() for component in source.get("institution_id", [])})}
                


#                 # cvdict['institution_id'] = {i: institutions[i] for i in sorted({component for source in cvdict[entry].values() for component in source.get("institution_id", [])})}

#                 # [[i,instutitions[i]] for i in sorted(list(set(component for source in cvdict[entry].values() for component in source.get("institution_id",[]))))]

#         elif entry in template:
#             cvdict[entry] = template[entry]

#         else:
#             missing.append(entry)

#     #  final check
#     diff = set(missing) - set(cvdict)

#     if diff:
#         raise core.stdout.MissingValueError(
#             f'The following fields are required:{diff} ')

#     core.stdout.MissingValueError(f'The following fields are required:{diff} ')

#     #  update this to the correct format.
#     cvdict['source_type'] = dict([[s, source_type[s]]
#                                  for s in cvdict['source_type']])
#     print(cvdict['source_type'])
#     cvdict = prune(cvdict)

#     CVfile = f"{directory}{outloc}/{core.io.ensure_suffix(prefix,'_')}CV.json"
#     core.io.json_write(dict(CV=cvdict), CVfile, sort=True)

#     return CVfile
