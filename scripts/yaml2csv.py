#!/usr/bin/env python3

import yaml
import csv
import os
import sys
import typing


def read_yaml(file_path) -> typing.List[typing.Dict]:
    with open(file_path) as f:
        content = yaml.safe_load(f)
    return content


def write_csv(file_path: str, rows_to_write: typing.List[typing.Dict[str, any]]):
    if not rows_to_write or len(rows_to_write) == 0:
        return

    dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(dir, file_path), 'w', newline='') as output:
        csvHeaders = rows_to_write[0].keys()
        csv_writer = csv.DictWriter(output, fieldnames=csvHeaders)
        csv_writer.writeheader()
        csv_writer.writerows(rows_to_write)


def main():
    if len(sys.argv) < 2:
        print("Please provide the path to the YAML file as an argument.")
        sys.exit(1)

    FILE_PATH = sys.argv[1]
    OUT_FILE = "list_of_network_equipment.csv"
    data = read_yaml(FILE_PATH)
    write_csv(OUT_FILE, data)


if __name__ == "__main__":
    main()