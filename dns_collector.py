"""
        Python Script to collect queries from DNS
        Develop By Maryori Sabalza Mejia
"""

import requests


def dns_file_parse(filename):
    """
        Method to open and read the queries file 
    """
    data = []

    with open(filename, 'r') as filename:
        for line in filename:
            p = line.strip().split()
            if len(p) == 2:
                ip_client, host, port = p
                data.append((ip_client,host))
    return data

if __name__ == "__main__":
    filename = "queries"
    parsed_data = dns_file_parse(filename)

    for record in parsed_data:
        print(record)