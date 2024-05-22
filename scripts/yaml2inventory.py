#!/usr/bin/env python3

import yaml
import os
import sys
from operator import itemgetter
from jinja2 import Environment, FileSystemLoader

dir = os.path.dirname(os.getcwd())

#$ python3 yaml2inventory.py templates/hosts.yaml.j2
template_dir, template_file = os.path.split(sys.argv[1])

#define Environment for Jinja2 template
env = Environment(
    loader=FileSystemLoader(template_dir),
    trim_blocks=True,
    lstrip_blocks=True)
template = env.get_template(template_file)

#read the file and upload its content to the list of dictionaries
with open(dir + "/list_of_network_equipment.yaml", "r") as f:
    result =  yaml.safe_load(f)

#define tuple with certain keys for further work
tuple_keys = ('hostname', 
              'ip_mgmt_address',
              'site',
              'role_of_work',
              'os',
              'cluster',
              'operational_status')

#write dicts which contain key:value pairs (define on previous step)
#to new list of dictionaries 
get_keys = itemgetter(*tuple_keys)
new_result = [ dict(zip(tuple_keys,get_keys(d))) for d in result ]

#delete dicts with unusable values for key "Role of work" 
#and write to new variable
filter_list = ['FEX',
               'FI switch',
               'WDM',
               'Console switch',
               'Bladecenter switch',]
filtered_list = [d for d in new_result if d['role_of_work'] not in filter_list]

#delete dicts with unusable values for key "Operational status"
#and write to new variable
filter_list2 = ['Dismantle', 'Provisioning']
final = [d for d in filtered_list if d['operational_status'] not in filter_list2]

for i,d in enumerate(final):
    if d['cluster'] == True:
        final[i]['hostname'] = d.get('hostname', '').rsplit('-', 1)[0]

#create dict with list of dicts for jinja2 template working
dict = {"top": final}

#write result of render variable via jinja2 template to file
with open('hosts.yaml', 'w') as f:
        f.write(template.render(dict))
