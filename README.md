# Lumu_TechnicalTest_MS
Technical Test Python Developer LUMU Technologies By Maryori Sabalza


## How to run:

- Create a Virtual Env
- Activate virtual env: source myenv/bin/activate
- Run the script: 
    - git python dns_collector.py bind_server.log



## Script Explanation

Python Script to collect queries from DNS and send data to LUMU API

- *dns_file_parse*: This method is responsible for opening the file, parsing it by line.

    -Using regular expressions, the specific patterns of each line of the DNS file are searched to capture each
     timestamp, client_ip, and host. Then the client_ip_counter and host_counter counters are incremented according to the IP address of the client and query host.

    - (\S+ \S+): Captures two groups of non-space characters separated by a space. This will correspond to the date and time in the specific DNS record format.

    - queries: \S+: client @\S+: Matches the string "queries:" followed by a space and anything non-spatial up to "client @", then followed by anything non-spatial.

    - (\d+\.\d+\.\d+\.\d+)#\d+: Captures an IP address in numeric format and a port number.

    - \(\S+\): Matches parentheses containing anything non-spatial. This is used to capture additional information in parentheses.

    - query: (\S+) IN: Matches the string "query:" followed by a space and anything non-space after that.


- *send_to_lumu*: This method basically prepares data and makes an HTTP request. The complexity of this is mainly dependent on the length of chunk_data, which refers to the number of records. Despite setting up the connection, no success was achieved since a 403 "The request does not meet the necessary requirements" was always obtained, apparently not all the requirements to send the data are met.


- *print_statistics*: This method loops through the client_ip_counter and host_counter collections to print statistics.


- *main*: The principal function is to call all the methods using argparse library because this helps to analyze the arguments that the program could accept, then count the IP client and host, sum all the records, and show the statistics. Finally, send the data to lumu by calling the send_to_lumu method. 