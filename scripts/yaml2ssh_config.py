#!/usr/bin/env python3

import yaml
import os
import sys
from operator import itemgetter
from jinja2 import Environment, FileSystemLoader

dir = os.path.dirname(os.getcwd())

#$ python3 yaml2ssh_config.py templates/ssh_config.j2
template_dir, template_file = os.path.split(sys.argv[1])

#Define Environment for Jinja2 template
env = Environment(
    loader=FileSystemLoader(template_dir),
    trim_blocks=True,
    lstrip_blocks=True)
template = env.get_template(template_file)

#Read the file and upload its content to the list of dictionaries
with open(dir + "/list_of_network_equipment.yaml", "r") as f:
    result =  yaml.safe_load(f)

#This string will hold final configurations
config = ""

#Define tuple with certain keys for further work
tuple_keys = ('hostname',
              'ip_mgmt_address',
              'model',
              'role_of_work',
              'type_of_login',
              'operational_status',
              'cluster')

#Write dicts which contain key:value pairs (define on previous step)
#to new list of dictionaries
get_keys = itemgetter(*tuple_keys)
new_result = [ dict(zip(tuple_keys,get_keys(d))) for d in result ]

#delete dicts with unusable values for key "Role of work"
#and write to new variable
filter_list = ['WDM', 'FEX']
filtered_list = [d for d in new_result if d['role_of_work'] not in filter_list]

#Delete dicts with unusable values for key "Operational status"
#and write to new variable
filter_list2 = ['Dismantle', 'Provisioning']
final = [d for d in filtered_list if d['operational_status'] not in filter_list2]

#Normalize name for cluster devices
for i,d in enumerate(final):
    if d['cluster'] == True:
        final[i]['hostname'] = d.get('hostname', '').rsplit('-', 1)[0]


#Render list of dicts by Jinja template
for data in final:
    one_record = template.render(
        hostname_render = data["hostname"],
        ip_mgmt_address_render = data["ip_mgmt_address"],
        model_render = data["model"],
        role_of_work_render = data["role_of_work"],
        type_of_login_render = data["type_of_login"],
        operational_status_render = data["operational_status"],
        cluster_render = data["cluster"]
    )

    config += one_record

#Save final result to config ssh file
with open('config_network', 'w') as f:
        f.write(config)

