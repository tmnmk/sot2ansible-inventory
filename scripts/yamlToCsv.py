#!/usr/bin/python3

import yaml
import csv
import os

dir = os.path.dirname(os.getcwd())

rows_to_write = []

with open(dir + '/list_of_network_equipment.yaml') as f:
    content = yaml.safe_load(f)
    for sample in content:
        rows_to_write.append([sample["id"],
        sample["hostname"],
        sample["ip_mgmt_address"],
        sample["site"],
        sample["role_of_work"],
        sample["type_of_login"],
        sample["os"],
        sample["manufacturer"],
        sample["model"],
        sample["serial_number"],
        sample["eos"],
        sample["license_expires"],
        sample["hardware_support"],
        sample["cluster"],
        sample["operational_status"]])


with open(dir + '/list_of_network_equipment.csv', 'w', newline='') as output:
    csvHeaders = ["id","hostname","ip_mgmt_address", "site", "role_of_work", "type_of_login", "os", "manufacturer", "model", "serial_number", "eos", "license_expires", "hardware_support", "cluster", "operational_status"]
    csv_writer = csv.writer(output)
    csv_writer.writerow(csvHeaders)
    csv_writer.writerows(rows_to_write)
