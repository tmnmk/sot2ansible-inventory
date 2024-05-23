#!/usr/bin/python3

import yaml
import csv
import os
import sys


def read_yaml(file_path):
    with open(file_path) as f:
        content = yaml.safe_load(f)
    return content


def convert_to_csv(content):
    rows_to_write = []
    for sample in content:
        rows_to_write.append([
            sample["id"],
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
            sample["operational_status"]
        ])
    return rows_to_write


def write_csv(file_path, rows_to_write):
    dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(dir, file_path), 'w', newline='') as output:
        csvHeaders = ["id","hostname",
                      "ip_mgmt_address",
                      "site",
                      "role_of_work",
                      "type_of_login",
                      "os",
                      "manufacturer",
                      "model",
                      "serial_number",
                      "eos",
                      "license_expires",
                      "hardware_support",
                      "cluster",
                      "operational_status"]
        csv_writer = csv.writer(output)
        csv_writer.writerow(csvHeaders)
        csv_writer.writerows(rows_to_write)


def main():
    if len(sys.argv) < 2:
        print("Please provide the path to the YAML file as an argument.")
        sys.exit(1)

    file_path = sys.argv[1]
    content = read_yaml(file_path)
    rows_to_write = convert_to_csv(content)
    write_csv('list_of_network_equipment.csv', rows_to_write)


if __name__ == "__main__":
    main()
