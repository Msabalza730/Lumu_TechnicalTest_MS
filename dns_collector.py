""" 
    **********************************************************
        Python Script to collect queries from DNS
        Develop By Maryori Sabalza Mejia
    **********************************************************
""" 
import argparse
import re
import requests
from collections import Counter

def dns_file_parse(filename):
    """
        Method to open file, read the queries file and parser
    """
    client_ip_counter = Counter()
    host_counter = Counter()

    with open(filename, 'r') as file:
        for line in file:
            match = re.search(r'^(\S+ \S+) queries: \S+: client @\S+ (\d+\.\d+\.\d+\.\d+)#\d+ \(\S+\): query: (\S+) IN', line)
            if match:
                timestamp, client_ip, host = match.groups()
                client_ip_counter[client_ip] += 1
                host_counter[host] += 1

    return client_ip_counter, host_counter


def send_to_lumu(chunk_data):
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
        "CollectorID": collector_id,
        "queriesDNS": chunk_data
    }

    try:
        response = requests.post(api_lumu, json=chunk_data, headers=headers)

        if response.status_code == 200:
            print("Data was sent successfully")
        else:
            print("Error sending data to Lumu Technologies %s" % response.status_code)
            print("----------- CONTENT ------------")
            print(response.content)
    except Exception as e:
        print(f"Error Connection: {e}")


def print_statistics(client_ip_counter, host_counter, total_records):
    """
        Function to print the statistics
    """
    print("Total records {}\n".format(total_records))
    
    print("Client IPs Rank")
    print("--------------   ---  -------")
    for ip, count in client_ip_counter.most_common():
        percentage = (count / total_records) * 100
        print("{}   {}   {:.2f}%".format(ip, count, percentage))
    print("--------------   ---  -------\n")
    
    print("Host Rank")
    print("--------------   ---  -------")
    for host, count in host_counter.most_common():
        percentage = (count / total_records) * 100
        print("{}      {}    {:.2f}%".format(host, count, percentage))
    print("--------------   ---  -------")


def main():
    """
        Principal function to send data parser to LUMU and show the result
    """

    parser = argparse.ArgumentParser(description="Parse BIND Server log and send data to Lumu")
    parser.add_argument("filename", help="Path to the BIND Server log file")
    args = parser.parse_args()

    filename = args.filename

    client_ip_counter, host_counter = dns_file_parse(filename)
    total_records = sum(client_ip_counter.values())

    print_statistics(client_ip_counter, host_counter, total_records)

    # Send data to Lumu
    data = [{"client_ip": ip, "count": count} for ip, count in client_ip_counter.items()]
    send_to_lumu(data)

if __name__ == "__main__":
    main()