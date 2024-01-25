"""
        Python Script to collect queries from DNS
        Develop By Maryori Sabalza Mejia
"""

import requests
from collections import Counter

def dns_file_parse(file_path):
    dns_data = []

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 7:
                timestamp = " ".join(parts[:3])
                client_ip = parts[9]
                host = parts[-2][:-1]
                dns_data.append((timestamp, client_ip, host))

    return dns_data


def send2_Lumu(chunk):
    """
        Method to sent data to Lumu
    """
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


def statics(records, client_ip_rank, host_rank):
    """
        Function to print a static of the parsed data
    """
    print(f"Total records {len(records)}")

    print("Client IPs Rank")
    print("--------------- --- -----")
    for ip, count in client_ip_rank:
        percentage = (count / len(records)) * 100
        print(f"{ip} {count} {percentage:.2f}%")
    print("--------------- --- -----")

    print("Host Rank")
    print("------------------------------------------------------------ --- -----")
    for host, count in host_rank:
        percentage = (count / len(records)) * 100
        print(f"{host} {count} {percentage:.2f}%")
    print("------------------------------------------------------------ --- -----")


