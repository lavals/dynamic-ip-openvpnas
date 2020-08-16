# dynamic-ip-openvpnas

A script to add a DNS name with dynamic IP address or addresses to OpenVPN Access Server.

OpenVPN Access Server doesn't allow to add DNS records to the Routing (Configuration -> VPN settings -> Routing -> Specify the private subnets to which all clients should be given access). In case if IP addresses are not static and could be changed, there is no way to do it automatically. 
The idea is to extend `config_local.db` (located at: `/usr/local/openvpn_as/etc/db`) SQLLite3 database and automatically add IPs from a file with DNS names.
Good example is Application Load Balancer at AWS, it doesn't have static IP addresses. 

Deployment steps:

1. Create "domains_list.txt" file and add domain names, each new name starts from a new string.
2. Execute "dnstoip.py" (add it to crontab).