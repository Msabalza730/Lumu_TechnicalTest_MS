"""
        Python Script to collect queries from DNS
        Develop By Maryori Sabalza Mejia
"""

import requests


def dns_file_parse(filename):
    """
        Method to open file, read the queries file and parser
    """
    data = []

    with open(filename, 'r') as filename:
        for line in filename:
            p = line.strip().split()
            if len(p) == 2:
                ip_client, host, port = p
                data.append((ip_client,host))
    return data

def send2_Lumu(chunk):
    api_lumu = "https://api.lumu.io/collectors/custom-collectors/collector-id/send-dns-queries"
    lumu_client_key = "d39a0f19-7278-4a64-a255-b7646d1ace80"
    collector_id = "5ab55d08-ae72-4017-a41c-d9d735360288 "

    headers = {
        "Content-Type": "application/json",
        "Lumu-Client-Key": lumu_client_key
    }

    payload = {
        "Collector-ID": collector_id,
        "queries_dns": chunk
    }

    try:
        response = requests.post(api_lumu, json=payload, headers=headers)

        if response.status_code == 200:
            print("Data was sent successfully")
        else:
            print("Error sending data to Lumu Technologies %s" % response.status_code)
    except Exception as e:
        print(f"Error Connection: {e}")



if __name__ == "__main__":
    filename = "queries"
    parsed_data = dns_file_parse(filename)

    for record in parsed_data:
        print(record)