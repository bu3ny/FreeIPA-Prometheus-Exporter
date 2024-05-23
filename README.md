# FreeIPA and LDAP Prometheus Exporter

  - This script collects metrics from FreeIPA and LDAP and exposes them for Prometheus monitoring.

# Prerequisites
- Ensure you have the following installed on your system:
    - Python 3.9 or higher
    - FreeIPA client
    - Prometheus client library for Python
    - LDAP3 library for Python

# Required Python Packages

  - You can install the required Python packages using pip:

    ~~~
    # pip install prometheus_client ldap3 requests
    ~~~

# Script Overview

  - The script freeipa_exporter.py collects various metrics from FreeIPA and LDAP servers and exposes them on port 8000 for Prometheus to scrape.

# Metrics Collected

  - FreeIPA Metrics:
    - Total number of FreeIPA users
    - Total number of FreeIPA groups
    - Total number of FreeIPA hosts
    - Total number of FreeIPA replicas
    - Total number of FreeIPA sudo rules
    - Total number of FreeIPA HBAC rules
    - Total number of DNS zones
    - Total number of certificates
    - Number of certificates expiring soon
    - Replication latency between FreeIPA servers
    - Uptime of FreeIPA services
    - Number of active user accounts
    - Number of inactive user accounts
    - Number of locked user accounts
    - Number of users with expiring passwords
    - Number of users in each group

  - LDAP Metrics:
    - Total number of LDAP entries
    - Total number of LDAP user entries
    - Total number of LDAP group entries
    - Number of LDAP threads
    - Number of current LDAP connections
    - Total number of LDAP connections
    - Number of LDAP operations initiated
    - Number of LDAP operations completed
    - Number of LDAP entries sent
    - Number of LDAP bytes sent
    - Number of anonymous LDAP binds
    - Number of unauthenticated LDAP binds
    - Number of simple authenticated LDAP binds
    - Number of LDAP search operations

  - Logconv.pl Metrics:

    - Peak Concurrent Connections
    - Total Operations
    - Total Results
    - Overall Performance
    - Total Connections
      - Number of LDAP Connections
      - Number of LDAPI Connections
      - Number of LDAPS Connections
      - Number of StartTLS Extended Ops
      - Number of Searches
      - Number of Modifications
      - Number of Adds
      - Number of Deletes
      - Number of Mod RDNs
      - Number of Compares
      - Number of Binds
    - Average wait time
    - Average operation time
    - Average elapsed time

# Script Usage

1. Configure FreeIPA and LDAP Connection Parameters:
Modify the following variables in the script with your FreeIPA and LDAP server details:

    ~~~
    FREEIPA_SERVER = 'idm-1.linux.example.com'
    FREEIPA_USERNAME = 'admin'
    FREEIPA_PASSWORD = 'P@ssw0rd'

    LDAP_SERVER = 'ldaps://idm-1.linux.example.com'
    LDAP_USER = 'cn=Directory Manager'
    LDAP_PASSWORD = 'P@ssw0rd'
    LDAP_BASE_DN = 'dc=linux,dc=example,dc=com'
    LDAP_MONITOR_DN = 'cn=monitor'
    ~~~

2. Run the Script:

    ~~~
    python3 freeipa_exporter.py
    ~~~


      1. This will start the Prometheus exporter on port 8000.
      2. Verify Metrics Exposure: You can verify the metrics exposure by accessing http://localhost:8000 in your web browser or using curl.

          ~~~
          curl http://localhost:8000
          ~~~

3. Configure Prometheus to Scrape Metrics:

  - Add the following job configuration to your Prometheus configuration file (prometheus.yml):

    ~~~
    scrape_configs:
      - job_name: 'freeipa_exporter'
        static_configs:
          - targets: ['localhost:8000']              # change it to the IP on hostname on which the script is running on - if firewalld is running, allow port 8000
    ~~~


# Sample Output

  - Here's a sample output of the script running:

    ~~~
    Prometheus exporter running on port 8000
    Password for admin@LINUX.EXAMPLE.COM:
    Total users: 1
    Total groups: 6
    Total hosts: 1
    Total replicas: 1
    Total sudo rules: 0
    Total HBAC rules: 2
    Total DNS zones: 2
    Total certificates: 10
    Total LDAP entries: 526
    Total LDAP users: 3
    Total LDAP groups: 8
    ipa: INFO: The ipactl command was successful
    Directory Service (dirsrv@*.service) status: RUNNING
    krb5kdc Service (krb5kdc.service) status: RUNNING
    kadmin Service (kadmin.service) status: RUNNING
    named Service (named.service) status: RUNNING
    httpd Service (httpd.service) status: RUNNING
    ipa-custodia Service (ipa-custodia.service) status: RUNNING
    pki-tomcatd Service (pki-tomcatd.target) status: RUNNING
    smb Service (smb.service) status: RUNNING
    winbind Service (winbind.service) status: RUNNING
    ipa-otpd Service (ipa-otpd.socket) status: RUNNING
    ipa-dnskeysyncd Service (ipa-dnskeysyncd.service) status: RUNNING
    Certificates expiring soon: 0
    Replication latency: 0.5
    dirsrv@LINUX-EXAMPLE-COM.service uptime: 2498438.4528472424
    krb5kdc.service uptime: 2498437.4945693016
    kadmin.service uptime: 2498437.5272693634
    named.service uptime: 2498436.56122756
    httpd.service uptime: 2498435.5943431854
    ipa-custodia.service uptime: 2498435.622569561
    smb.service uptime: 2498423.668035507
    winbind.service uptime: 2498422.6993317604
    ipa-otpd.socket uptime: 2498422.728649378
    ipa-dnskeysyncd.service uptime: 2498422.7603578568
    Active users: 1
    Locked users: 0
    Inactive users: 0
    Users with expiring passwords: 0
    Group admins has 1 members
    Group editors has 0 members
    Group ipausers has 0 members
    Group linux_admins has 0 members
    Group linux_admins_external has 0 members
    Group trust admins has 1 members
    Running logconv.pl script...
    logconv.pl output:
    Access Log Analyzer 8.2
    Command: logconv.pl /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.rotationinfo /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.20240513-095515 /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.20240514-095518 /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.20240517-095528 /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.20240515-095521 /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.20240518-095601 /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.20240519-095604 /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.20240511-095509 /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.20240512-095512 /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.20240516-095524
    Processing 11 Access Log(s)...

    [011] /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.20240511-095509	size (bytes):      2317873

    [010] /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.20240512-095512	size (bytes):      2319779

    [009] /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.20240513-095515	size (bytes):      2502419

    [008] /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.20240514-095518	size (bytes):      2402352

    [007] /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.20240515-095521	size (bytes):      2714512

    [006] /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.20240516-095524	size (bytes):      2306250

    [005] /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.20240517-095528	size (bytes):      2403188

    [004] /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.20240518-095601	size (bytes):      2324392

    [003] /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.20240519-095604	size (bytes):      2579004

    [002] /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.rotationinfo	size (bytes):         1071

    [001] /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access	size (bytes):     18927129
        25000 Lines Processed          4983596 of     18927129 bytes (26.330%)
        50000 Lines Processed         11665775 of     18927129 bytes (61.635%)
        75000 Lines Processed         18624147 of     18927129 bytes (98.399%)


    Total Log Lines Analysed:  170062


    ----------- Access Log Output ------------

    Start of Logs:    11/May/2024:09:54:55.230219129
    End of Logs:      20/May/2024:22:40:05.730843167

    Processed Log Time:  9 Days, 12 Hours, 45 Minutes, 10.500622336 Seconds

    Restarts:                      0
    Secure Protocol Versions:
      - TLS1.3 128-bit AES-GCM (297 connections)

    Peak Concurrent Connections:   4
    Total Operations:              77823
    Total Results:                 75095
    Overall Performance:           96.5%

    Total Connections:             4353          (0.01/sec)  (0.32/min)
    - LDAP Connections:           3864          (0.00/sec)  (0.28/min)
    - LDAPI Connections:          332           (0.00/sec)  (0.02/min)
    - LDAPS Connections:          157           (0.00/sec)  (0.01/min)
    - StartTLS Extended Ops:      140           (0.00/sec)  (0.01/min)

    Searches:                      67547         (0.08/sec)  (4.92/min)
    Modifications:                 979           (0.00/sec)  (0.07/min)
    Adds:                          0             (0.00/sec)  (0.00/min)
    Deletes:                       0             (0.00/sec)  (0.00/min)
    Mod RDNs:                      0             (0.00/sec)  (0.00/min)
    Compares:                      0             (0.00/sec)  (0.00/min)
    Binds:                         4338          (0.01/sec)  (0.32/min)

    Average wtime (wait time):     0.000528216
    Average optime (op time):      0.001284505
    Average etime (elapsed time):  0.001809618

    Proxied Auth Operations:       0
    Persistent Searches:           0
    Internal Operations:           0
    Entry Operations:              0
    Extended Operations:           280
    Abandoned Requests:            0
    Smart Referrals Received:      0

    VLV Operations:                4679
    VLV Unindexed Searches:        0
    VLV Unindexed Components:      2738
    SORT Operations:               1941

    Entire Search Base Queries:    305
    Paged Searches:                5360
    Unindexed Searches:            0
    Unindexed Components:          172
    Invalid Attribute Filters:     0
    FDs Taken:                     4353
    FDs Returned:                  4352
    Highest FD Taken:              242

    Broken Pipes:                  0
    Connections Reset By Peer:     0
    Resource Unavailable:          0
    Max BER Size Exceeded:         0

    Binds:                         4338
    Unbinds:                       4043
    -----------------------------------
    - LDAP v2 Binds:              0
    - LDAP v3 Binds:              4177
    - AUTOBINDs(LDAPI):           161
    - SSL Client Binds:           0
    - Failed SSL Client Binds:    0
    - SASL Binds:                 4018
      - GSS-SPNEGO: 2801
      - GSSAPI: 1056
      - EXTERNAL: 161
    - Directory Manager Binds:    4
    - Anonymous Binds:            0

    Cleaning up temp files...
    Done.

    logconv.pl metrics updated
    ~~~

  - Here's a sample output of the curl command:

    ~~~
    # HELP python_gc_objects_collected_total Objects collected during gc
    # TYPE python_gc_objects_collected_total counter
    python_gc_objects_collected_total{generation="0"} 1850.0
    python_gc_objects_collected_total{generation="1"} 379.0
    python_gc_objects_collected_total{generation="2"} 0.0
    # HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
    # TYPE python_gc_objects_uncollectable_total counter
    python_gc_objects_uncollectable_total{generation="0"} 0.0
    python_gc_objects_uncollectable_total{generation="1"} 0.0
    python_gc_objects_uncollectable_total{generation="2"} 0.0
    # HELP python_gc_collections_total Number of times this generation was collected
    # TYPE python_gc_collections_total counter
    python_gc_collections_total{generation="0"} 261.0
    python_gc_collections_total{generation="1"} 23.0
    python_gc_collections_total{generation="2"} 2.0
    # HELP python_info Python platform information
    # TYPE python_info gauge
    python_info{implementation="CPython",major="3",minor="9",patchlevel="18",version="3.9.18"} 1.0
    # HELP process_virtual_memory_bytes Virtual memory size in bytes.
    # TYPE process_virtual_memory_bytes gauge
    process_virtual_memory_bytes 2.36843008e+08
    # HELP process_resident_memory_bytes Resident memory size in bytes.
    # TYPE process_resident_memory_bytes gauge
    process_resident_memory_bytes 8.030208e+07
    # HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
    # TYPE process_start_time_seconds gauge
    process_start_time_seconds 1.71622704283e+09
    # HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
    # TYPE process_cpu_seconds_total counter
    process_cpu_seconds_total 1.79
    # HELP process_open_fds Number of open file descriptors.
    # TYPE process_open_fds gauge
    process_open_fds 9.0
    # HELP process_max_fds Maximum number of open file descriptors.
    # TYPE process_max_fds gauge
    process_max_fds 1024.0
    # HELP freeipa_users_total Total number of FreeIPA users
    # TYPE freeipa_users_total gauge
    freeipa_users_total 1.0
    # HELP freeipa_groups_total Total number of FreeIPA groups
    # TYPE freeipa_groups_total gauge
    freeipa_groups_total 6.0
    # HELP freeipa_hosts_total Total number of FreeIPA hosts
    # TYPE freeipa_hosts_total gauge
    freeipa_hosts_total 1.0
    # HELP freeipa_replicas_total Total number of FreeIPA replicas
    # TYPE freeipa_replicas_total gauge
    freeipa_replicas_total 1.0
    # HELP freeipa_sudo_rules_total Total number of FreeIPA sudo rules
    # TYPE freeipa_sudo_rules_total gauge
    freeipa_sudo_rules_total 0.0
    # HELP freeipa_hbac_rules_total Total number of FreeIPA HBAC rules
    # TYPE freeipa_hbac_rules_total gauge
    freeipa_hbac_rules_total 2.0
    # HELP freeipa_dns_zones_total Total number of DNS zones
    # TYPE freeipa_dns_zones_total gauge
    freeipa_dns_zones_total 2.0
    # HELP freeipa_certificates_total Total number of certificates
    # TYPE freeipa_certificates_total gauge
    freeipa_certificates_total 10.0
    # HELP freeipa_certificates_expiring_soon Number of certificates expiring soon
    # TYPE freeipa_certificates_expiring_soon gauge
    freeipa_certificates_expiring_soon 0.0
    # HELP freeipa_replication_latency Replication latency between FreeIPA servers
    # TYPE freeipa_replication_latency gauge
    freeipa_replication_latency 0.5
    # HELP freeipa_service_uptime Uptime of FreeIPA services
    # TYPE freeipa_service_uptime gauge
    freeipa_service_uptime{service="dirsrv@*.service"} 1.0
    freeipa_service_uptime{service="krb5kdc.service"} 2.4950858754734993e+06
    freeipa_service_uptime{service="kadmin.service"} 2.4950859129490852e+06
    freeipa_service_uptime{service="named.service"} 2.4950849516251087e+06
    freeipa_service_uptime{service="httpd.service"} 2.4950839903361797e+06
    freeipa_service_uptime{service="ipa-custodia.service"} 2.4950840363357067e+06
    freeipa_service_uptime{service="pki-tomcatd.target"} 1.0
    freeipa_service_uptime{service="smb.service"} 2.4950720917503834e+06
    freeipa_service_uptime{service="winbind.service"} 2.4950711296663284e+06
    freeipa_service_uptime{service="ipa-otpd.socket"} 2.4950711736752987e+06
    freeipa_service_uptime{service="ipa-dnskeysyncd.service"} 2.495071217415571e+06
    freeipa_service_uptime{service="dirsrv@LINUX-EXAMPLE-COM.service"} 2.495086838447809e+06
    # HELP freeipa_active_user_accounts Number of active user accounts
    # TYPE freeipa_active_user_accounts gauge
    freeipa_active_user_accounts 1.0
    # HELP freeipa_inactive_user_accounts Number of inactive user accounts
    # TYPE freeipa_inactive_user_accounts gauge
    freeipa_inactive_user_accounts 0.0
    # HELP freeipa_locked_user_accounts Number of locked user accounts
    # TYPE freeipa_locked_user_accounts gauge
    freeipa_locked_user_accounts 0.0
    # HELP freeipa_password_expirations Number of users with expiring passwords
    # TYPE freeipa_password_expirations gauge
    freeipa_password_expirations 0.0
    # HELP freeipa_group_memberships Number of users in each group
    # TYPE freeipa_group_memberships gauge
    freeipa_group_memberships{group="admins"} 1.0
    freeipa_group_memberships{group="editors"} 0.0
    freeipa_group_memberships{group="ipausers"} 0.0
    freeipa_group_memberships{group="linux_admins"} 0.0
    freeipa_group_memberships{group="linux_admins_external"} 0.0
    freeipa_group_memberships{group="trust admins"} 1.0
    # HELP ldap_entries_total Total number of LDAP entries
    # TYPE ldap_entries_total gauge
    ldap_entries_total 526.0
    # HELP ldap_users_total Total number of LDAP user entries
    # TYPE ldap_users_total gauge
    ldap_users_total 3.0
    # HELP ldap_groups_total Total number of LDAP group entries
    # TYPE ldap_groups_total gauge
    ldap_groups_total 8.0
    # HELP ldap_threads Number of LDAP threads
    # TYPE ldap_threads gauge
    ldap_threads 20.0
    # HELP ldap_current_connections Number of current LDAP connections
    # TYPE ldap_current_connections gauge
    ldap_current_connections 15.0
    # HELP ldap_total_connections Total number of LDAP connections
    # TYPE ldap_total_connections gauge
    ldap_total_connections 6128.0
    # HELP ldap_ops_initiated Number of LDAP operations initiated
    # TYPE ldap_ops_initiated gauge
    ldap_ops_initiated 232733.0
    # HELP ldap_ops_completed Number of LDAP operations completed
    # TYPE ldap_ops_completed gauge
    ldap_ops_completed 232732.0
    # HELP ldap_entries_sent Number of LDAP entries sent
    # TYPE ldap_entries_sent gauge
    ldap_entries_sent 206990.0
    # HELP ldap_bytes_sent Number of LDAP bytes sent
    # TYPE ldap_bytes_sent gauge
    ldap_bytes_sent 3.07277406e+08
    # HELP ldap_anonymous_binds Number of anonymous LDAP binds
    # TYPE ldap_anonymous_binds gauge
    ldap_anonymous_binds 0.0
    # HELP ldap_unauth_binds Number of unauthenticated LDAP binds
    # TYPE ldap_unauth_binds gauge
    ldap_unauth_binds 0.0
    # HELP ldap_simple_auth_binds Number of simple authenticated LDAP binds
    # TYPE ldap_simple_auth_binds gauge
    ldap_simple_auth_binds 153.0
    # HELP ldap_search_ops Number of LDAP search operations
    # TYPE ldap_search_ops gauge
    ldap_search_ops 174134.0
    # HELP logconv_peak_concurrent_connections Peak Concurrent Connections
    # TYPE logconv_peak_concurrent_connections gauge
    logconv_peak_concurrent_connections 4.0
    # HELP logconv_total_operations Total Operations
    # TYPE logconv_total_operations gauge
    logconv_total_operations 75762.0
    # HELP logconv_total_results Total Results
    # TYPE logconv_total_results gauge
    logconv_total_results 73064.0
    # HELP logconv_overall_performance Overall Performance
    # TYPE logconv_overall_performance gauge
    logconv_overall_performance 96.4
    # HELP logconv_total_connections Total Connections
    # TYPE logconv_total_connections gauge
    logconv_total_connections 4206.0
    # HELP logconv_ldap_connections Number of LDAP Connections
    # TYPE logconv_ldap_connections gauge
    logconv_ldap_connections 3735.0
    # HELP logconv_ldapi_connections Number of LDAPI Connections
    # TYPE logconv_ldapi_connections gauge
    logconv_ldapi_connections 320.0
    # HELP logconv_ldaps_connections Number of LDAPS Connections
    # TYPE logconv_ldaps_connections gauge
    logconv_ldaps_connections 151.0
    # HELP logconv_starttls_extended_ops Number of StartTLS Extended Ops
    # TYPE logconv_starttls_extended_ops gauge
    logconv_starttls_extended_ops 133.0
    # HELP logconv_searches Number of Searches
    # TYPE logconv_searches gauge
    logconv_searches 0.0
    # HELP logconv_modifications Number of Modifications
    # TYPE logconv_modifications gauge
    logconv_modifications 975.0
    # HELP logconv_adds Number of Adds
    # TYPE logconv_adds gauge
    logconv_adds 0.0
    # HELP logconv_deletes Number of Deletes
    # TYPE logconv_deletes gauge
    logconv_deletes 0.0
    # HELP logconv_mod_rdns Number of Mod RDNs
    # TYPE logconv_mod_rdns gauge
    logconv_mod_rdns 0.0
    # HELP logconv_compares Number of Compares
    # TYPE logconv_compares gauge
    logconv_compares 0.0
    # HELP logconv_binds Number of Binds
    # TYPE logconv_binds gauge
    logconv_binds 0.0
    # HELP logconv_avg_wtime Average wait time
    # TYPE logconv_avg_wtime gauge
    logconv_avg_wtime 0.000529113
    # HELP logconv_avg_optime Average operation time
    # TYPE logconv_avg_optime gauge
    logconv_avg_optime 0.001279598
    # HELP logconv_avg_etime Average elapsed time
    # TYPE logconv_avg_etime gauge
    logconv_avg_etime 0.001805612
    ~~~

# Troubleshooting

  - Ensure the FreeIPA client and necessary packages are installed.
  - Check the FreeIPA and LDAP connection parameters.
  - Verify that the log files for logconv.pl are present in the specified directory.


- To ensure the freeipa_exporter.py script runs correctly, you need to install the following Python packages:
    1. prometheus_client
    2. ldap3
    3. requests
    4. ipalib

- You can install these packages using pip. Here is the command to install all the required packages:

  ~~~
  pip3 install prometheus_client ldap3 requests ipalib flask
  ~~~


- Here's a brief overview of each package:
  - prometheus_client: Provides Prometheus instrumentation for Python applications.
  - ldap3: A pure Python LDAP client library.
  - requests: A simple, yet elegant HTTP library for Python.
  - ipalib: FreeIPA API client library.


- Installing the Packages


  - Run the following command to install all the necessary packages:

    - If the packages are installed, these commands will display information about each package, including the version number and installation location. If any package is not installed, the command will return an error.

        - Required RPM Packages
          1. python3-prometheus_client
          2. python3-ldap3
          3. python3-requests
          4. python3-ipalib


- Installation Command

  - You can use dnf or yum to install these packages. Here is the command to install all the required packages:

    ~~~
    sudo dnf install python3-prometheus_client python3-ldap3 python3-requests python3-ipalib
    ~~~
