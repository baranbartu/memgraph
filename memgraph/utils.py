__author__ = 'baranbartu'

import os
import string
import random
import csv


def generate_file_name(chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(6))


def make_csv(logs, headers):
    csv_file = '%s.csv' % generate_file_name()
    with open(csv_file, 'w') as csvfile:
        fieldnames = headers
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for log in sorted(logs, key=lambda l: l['x']):
            writer.writerow(
                {headers[0]: str(log['x']), headers[1]: str(log['y'])})
    return csv_file


def remove_file(file_name):
    return os.remove(file_name)
