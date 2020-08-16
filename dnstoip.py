#!/usr/bin/python3

import sqlite3
import dns.resolver
import os
import time

profile_id = 1
default_name = 'vpn.server.routing.private_network.'

# Read the domain names and save to list
with open('domains_list.txt') as f:
    content = f.readlines()
content = [x.strip() for x in content]

# Resolve DNS names to IP addresses and save to dictionary
domains_dic = {}
for i in content:
    resolved = dns.resolver.query(i, 'A')
    for ipval in resolved:
        domains_dic[ipval.to_text() + '/32'] = i

#Connect to local database
con = sqlite3.connect('/usr/local/openvpn_as/etc/db/config_local.db')

with con:
    cur = con.cursor()
    # Validate if dns column exists, if not -> add it
    columns = [i[1] for i in cur.execute('PRAGMA table_info(config)')]
    if 'dns' not in columns:
        cur.execute('ALTER TABLE config ADD COLUMN dns TEXT')
    #Iterate dictionery with domain names and IPs
    for ip_address in domains_dic:
        #Select and check if pair exists, if it doesn't exist we INSERT it
        cur.execute(""" SELECT value, dns FROM config """)
        #Add x to track the status
        x = 0
        all_rows = cur.fetchall()
        for row in all_rows:
            if row[0] == ip_address and row[1] == domains_dic[ip_address]:
                print ("IP address already added to the database")
                print('{0}, {1}'.format(row[0], row[1]))
                x = 1
            # else:
            #     print ("Else worked")
        print ('Current X value = ' + str(x))
        #If IP and DNS don't match with existing records in the database
        if x == 0:
            #Find the last 'vpn.server.routing.private_network.' in 'name' column
            cur.execute(
                    """ SELECT profile_id, name, value, dns FROM config WHERE name LIKE 'vpn.server.routing.private_network.%' ORDER BY profile_id DESC LIMIT 1 """)
            row = cur.fetchone()
            name = row[1]
            last_position = int(name[35:]) + 1
            new_position = default_name + str(last_position)
            print ("Insert the next values:" + str(profile_id), str(new_position), str(ip_address), str(domains_dic[ip_address]))
            cur.execute("INSERT INTO config (profile_id, name, value, dns) VALUES (?,?,?,?)",
                        (profile_id, new_position, ip_address, domains_dic[ip_address]))
con.commit()
con.close()
time.sleep(2)
if x == 0:
    os.system('/usr/local/openvpn_as/scripts/sacli start')
