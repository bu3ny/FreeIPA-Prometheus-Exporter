# FreeIPA and LDAP Prometheus Exporter

  - This script collects metrics from FreeIPA and LDAP and exposes them for Prometheus monitoring.

# Prerequisites
- Ensure you have the following installed on your system:
    - Python 3.9 or higher
    - FreeIPA client
    - Prometheus client library for Python
    - LDAP3 library for Python
    - Flask

# Required Python Packages

  - You can install the required Python packages using pip:

    ~~~
    # pip install prometheus_client ldap3 requests flask ipalib
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
          curl http://localhost:8000/metrics
          ~~~

3. Configure Prometheus to Scrape Metrics:

  - Add the following job configuration to your Prometheus configuration file (prometheus.yml):

    ~~~
    global:
    scrape_interval: 15s # Adjust the scrape interval as needed

    scrape_configs:
    - job_name: 'freeipa_metrics'
        static_configs:
        - targets: ['localhost:8000'] # Assuming your Python script is running on localhost port 8000 - change it to match the IPA Server IP
        metrics_path: /metrics # Specify the endpoint where metrics are exposed
    ~~~


# Sample Output

  - Here's a sample output of the script running:

    ~~~
    [root@idm-1 prom_exporter]# python3 freeipa_exporter-v12.py
    2024-05-24 11:56:05,375 - INFO - Prometheus exporter running on port 8000
    Password for admin@LINUX.EXAMPLE.COM:
    2024-05-24 11:56:05,808 - INFO - Discovered Directory Service: dirsrv@LINUX-EXAMPLE-COM.service
    2024-05-24 11:56:06,247 - INFO - Total users: 1
    2024-05-24 11:56:06,877 - INFO - Total groups: 6
    2024-05-24 11:56:07,262 - INFO - Total hosts: 1
    2024-05-24 11:56:07,647 - INFO - Total sudo rules: 0
    2024-05-24 11:56:08,027 - INFO - Total HBAC rules: 2
    2024-05-24 11:56:08,436 - INFO - Total certificates: 10
    2024-05-24 11:56:08,991 - INFO - Total LDAP entries: 526
    2024-05-24 11:56:08,997 - INFO - Total LDAP users: 3
    2024-05-24 11:56:09,004 - INFO - Total LDAP groups: 8
    ipa: INFO: The ipactl command was successful
    2024-05-24 11:56:12,456 - INFO - krb5kdc Service (krb5kdc.service) status: RUNNING
    2024-05-24 11:56:12,457 - INFO - kadmin Service (kadmin.service) status: RUNNING
    2024-05-24 11:56:12,457 - INFO - named Service (named.service) status: RUNNING
    2024-05-24 11:56:12,457 - INFO - httpd Service (httpd.service) status: RUNNING
    2024-05-24 11:56:12,457 - INFO - ipa-custodia Service (ipa-custodia.service) status: RUNNING
    2024-05-24 11:56:12,457 - INFO - pki-tomcatd Service (pki-tomcatd@pki-tomcat.service) status: RUNNING
    2024-05-24 11:56:12,457 - INFO - smb Service (smb.service) status: RUNNING
    2024-05-24 11:56:12,457 - INFO - winbind Service (winbind.service) status: RUNNING
    2024-05-24 11:56:12,457 - INFO - ipa-otpd Service (ipa-otpd.socket) status: RUNNING
    2024-05-24 11:56:12,457 - INFO - ipa-dnskeysyncd Service (ipa-dnskeysyncd.service) status: RUNNING
    2024-05-24 11:56:12,457 - INFO - Directory Service (dirsrv@LINUX-EXAMPLE-COM.service) status: RUNNING
    2024-05-24 11:56:12,722 - INFO - Certificates expiring soon: 0
    2024-05-24 11:56:12,722 - INFO - Replication latency: 0.5
    2024-05-24 11:56:12,764 - INFO - krb5kdc.service uptime: 43497.76041722298
    2024-05-24 11:56:12,802 - INFO - kadmin.service uptime: 43497.80181193352
    2024-05-24 11:56:12,837 - INFO - named.service uptime: 43496.8374581337
    2024-05-24 11:56:12,872 - INFO - httpd.service uptime: 43494.872322797775
    2024-05-24 11:56:12,910 - INFO - ipa-custodia.service uptime: 43493.91032123566
    2024-05-24 11:56:12,951 - INFO - pki-tomcatd@pki-tomcat.service uptime: 43479.95148611069
    2024-05-24 11:56:12,987 - INFO - smb.service uptime: 43479.98678565025
    2024-05-24 11:56:13,027 - INFO - winbind.service uptime: 43479.02730536461
    2024-05-24 11:56:13,069 - INFO - ipa-otpd.socket uptime: 43479.06884098053
    2024-05-24 11:56:13,109 - INFO - ipa-dnskeysyncd.service uptime: 43479.108805418015
    2024-05-24 11:56:13,154 - INFO - dirsrv@LINUX-EXAMPLE-COM.service uptime: 43498.15442228317
    2024-05-24 11:56:13,428 - INFO - Active users: 1
    2024-05-24 11:56:13,428 - INFO - Locked users: 0
    2024-05-24 11:56:13,428 - INFO - Inactive users: 0
    2024-05-24 11:56:13,727 - INFO - Users with expiring passwords: 0
    2024-05-24 11:56:14,274 - INFO - Group admins has 1 members
    2024-05-24 11:56:14,509 - INFO - Group editors has 0 members
    2024-05-24 11:56:15,139 - INFO - Group ipausers has 0 members
    2024-05-24 11:56:15,507 - INFO - Group linux_admins has 0 members
    2024-05-24 11:56:16,295 - INFO - Group linux_admins_external has 0 members
    2024-05-24 11:56:16,655 - INFO - Group trust admins has 1 members
    2024-05-24 11:56:16,655 - INFO - Running logconv.pl script...
    2024-05-24 11:56:17,790 - INFO - logconv.pl output:
    Access Log Analyzer 8.2
    Command: logconv.pl /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access.rotationinfo
    Processing 1 Access Log(s)...

    [001] /var/log/dirsrv/slapd-LINUX-EXAMPLE-COM/access	size (bytes):      8818244
        25000 Lines Processed          6743772 of      8818244 bytes (76.475%)


    Total Log Lines Analysed:  32444


    ----------- Access Log Output ------------

    Start of Logs:    23/May/2024:23:51:15.085804290
    End of Logs:      24/May/2024:11:56:16.628592861

    Processed Log Time:  12 Hours, 5 Minutes, 1.542793216 Seconds

    Restarts:                      1
    Secure Protocol Versions:
      - TLS1.3 client bound as uid=pkidbuser,ou=People,o=ipaca (11 connections)
      - TLS1.3 128-bit AES-GCM; client CN=CA Subsystem,O=LINUX.EXAMPLE.COM; issuer CN=Certificate Authority,O=LINUX.EXAMPLE.COM (11 connections)
      - TLS1.3 128-bit AES-GCM (73 connections)
      - TLS1.2 128-bit AES-GCM (1 connections)

    Peak Concurrent Connections:   29
    Total Operations:              14728
    Total Results:                 14488
    Overall Performance:           98.4%

    Total Connections:             942           (0.02/sec)  (1.30/min)
    - LDAP Connections:           789           (0.02/sec)  (1.09/min)
    - LDAPI Connections:          106           (0.00/sec)  (0.15/min)
    - LDAPS Connections:          47            (0.00/sec)  (0.06/min)
    - StartTLS Extended Ops:      38            (0.00/sec)  (0.05/min)

    Searches:                      13283         (0.31/sec)  (18.32/min)
    Modifications:                 52            (0.00/sec)  (0.07/min)
    Adds:                          0             (0.00/sec)  (0.00/min)
    Deletes:                       0             (0.00/sec)  (0.00/min)
    Mod RDNs:                      0             (0.00/sec)  (0.00/min)
    Compares:                      0             (0.00/sec)  (0.00/min)
    Binds:                         944           (0.02/sec)  (1.30/min)

    Average wtime (wait time):     0.000632765
    Average optime (op time):      0.001312601
    Average etime (elapsed time):  0.001942145

    Proxied Auth Operations:       0
    Persistent Searches:           5
    Internal Operations:           0
    Entry Operations:              0
    Extended Operations:           76
    Abandoned Requests:            0
    Smart Referrals Received:      0

    VLV Operations:                373
    VLV Unindexed Searches:        0
    VLV Unindexed Components:      144
    SORT Operations:               229

    Entire Search Base Queries:    60
    Paged Searches:                694
    Unindexed Searches:            0
    Unindexed Components:          35
    Invalid Attribute Filters:     0
    FDs Taken:                     942
    FDs Returned:                  927
    Highest FD Taken:              255

    Broken Pipes:                  0
    Connections Reset By Peer:     0
    Resource Unavailable:          0
    Max BER Size Exceeded:         0

    Binds:                         944
    Unbinds:                       842
    ----------------------------------
    - LDAP v2 Binds:              0
    - LDAP v3 Binds:              892
    - AUTOBINDs(LDAPI):           52
    - SSL Client Binds:           0
    - Failed SSL Client Binds:    0
    - SASL Binds:                 859
      - GSS-SPNEGO: 701
      - GSSAPI: 95
      - EXTERNAL: 63
    - Directory Manager Binds:    0
    - Anonymous Binds:            0

    Cleaning up temp files...
    Done.

    2024-05-24 11:56:17,791 - INFO - logconv.pl metrics updated
    2024-05-24 11:56:18,178 - INFO - Total replicas: 1
    2024-05-24 11:56:18,571 - INFO - Total DNS zones: 2
    ~~~



  - Here's a sample output of the curl command:



    ~~~
    [root@idm-1 prom_exporter]# curl localhost:8000/metrics
    # HELP python_gc_objects_collected_total Objects collected during gc
    # TYPE python_gc_objects_collected_total counter
    python_gc_objects_collected_total{generation="0"} 2464.0
    python_gc_objects_collected_total{generation="1"} 87.0
    python_gc_objects_collected_total{generation="2"} 6.0
    # HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
    # TYPE python_gc_objects_uncollectable_total counter
    python_gc_objects_uncollectable_total{generation="0"} 0.0
    python_gc_objects_uncollectable_total{generation="1"} 0.0
    python_gc_objects_uncollectable_total{generation="2"} 0.0
    # HELP python_gc_collections_total Number of times this generation was collected
    # TYPE python_gc_collections_total counter
    python_gc_collections_total{generation="0"} 323.0
    python_gc_collections_total{generation="1"} 29.0
    python_gc_collections_total{generation="2"} 2.0
    # HELP python_info Python platform information
    # TYPE python_info gauge
    python_info{implementation="CPython",major="3",minor="9",patchlevel="18",version="3.9.18"} 1.0
    # HELP process_virtual_memory_bytes Virtual memory size in bytes.
    # TYPE process_virtual_memory_bytes gauge
    process_virtual_memory_bytes 2.50507264e+08
    # HELP process_resident_memory_bytes Resident memory size in bytes.
    # TYPE process_resident_memory_bytes gauge
    process_resident_memory_bytes 9.4134272e+07
    # HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
    # TYPE process_start_time_seconds gauge
    process_start_time_seconds 1.71653719792e+09
    # HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
    # TYPE process_cpu_seconds_total counter
    process_cpu_seconds_total 1.77
    # HELP process_open_fds Number of open file descriptors.
    # TYPE process_open_fds gauge
    process_open_fds 8.0
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
    freeipa_service_uptime{service="krb5kdc.service"} 43330.866621255875
    freeipa_service_uptime{service="kadmin.service"} 43330.90213441849
    freeipa_service_uptime{service="named.service"} 43329.93708014488
    freeipa_service_uptime{service="httpd.service"} 43327.97226405144
    freeipa_service_uptime{service="ipa-custodia.service"} 43327.00596547127
    freeipa_service_uptime{service="pki-tomcatd@pki-tomcat.service"} 43313.04147672653
    freeipa_service_uptime{service="smb.service"} 43313.07425546646
    freeipa_service_uptime{service="winbind.service"} 43312.10667347908
    freeipa_service_uptime{service="ipa-otpd.socket"} 43312.14158701897
    freeipa_service_uptime{service="ipa-dnskeysyncd.service"} 43312.18088722229
    freeipa_service_uptime{service="dirsrv@LINUX-EXAMPLE-COM.service"} 43331.2125582695
    # HELP freeipa_service_status Status of FreeIPA services (1 = running, 0 = not running)
    # TYPE freeipa_service_status gauge
    freeipa_service_status{service="krb5kdc.service"} 1.0
    freeipa_service_status{service="kadmin.service"} 1.0
    freeipa_service_status{service="named.service"} 1.0
    freeipa_service_status{service="httpd.service"} 1.0
    freeipa_service_status{service="ipa-custodia.service"} 1.0
    freeipa_service_status{service="pki-tomcatd@pki-tomcat.service"} 1.0
    freeipa_service_status{service="smb.service"} 1.0
    freeipa_service_status{service="winbind.service"} 1.0
    freeipa_service_status{service="ipa-otpd.socket"} 1.0
    freeipa_service_status{service="ipa-dnskeysyncd.service"} 1.0
    freeipa_service_status{service="dirsrv@LINUX-EXAMPLE-COM.service"} 1.0
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
    ldap_total_connections 906.0
    # HELP ldap_ops_initiated Number of LDAP operations initiated
    # TYPE ldap_ops_initiated gauge
    ldap_ops_initiated 15705.0
    # HELP ldap_ops_completed Number of LDAP operations completed
    # TYPE ldap_ops_completed gauge
    ldap_ops_completed 15704.0
    # HELP ldap_entries_sent Number of LDAP entries sent
    # TYPE ldap_entries_sent gauge
    ldap_entries_sent 27765.0
    # HELP ldap_bytes_sent Number of LDAP bytes sent
    # TYPE ldap_bytes_sent gauge
    ldap_bytes_sent 5.3235908e+07
    # HELP ldap_anonymous_binds Number of anonymous LDAP binds
    # TYPE ldap_anonymous_binds gauge
    ldap_anonymous_binds 0.0
    # HELP ldap_unauth_binds Number of unauthenticated LDAP binds
    # TYPE ldap_unauth_binds gauge
    ldap_unauth_binds 0.0
    # HELP ldap_simple_auth_binds Number of simple authenticated LDAP binds
    # TYPE ldap_simple_auth_binds gauge
    ldap_simple_auth_binds 32.0
    # HELP ldap_search_ops Number of LDAP search operations
    # TYPE ldap_search_ops gauge
    ldap_search_ops 12793.0
    # HELP logconv_peak_concurrent_connections Peak Concurrent Connections
    # TYPE logconv_peak_concurrent_connections gauge
    logconv_peak_concurrent_connections 29.0
    # HELP logconv_total_operations Total Operations
    # TYPE logconv_total_operations gauge
    logconv_total_operations 14071.0
    # HELP logconv_total_results Total Results
    # TYPE logconv_total_results gauge
    logconv_total_results 13835.0
    # HELP logconv_overall_performance Overall Performance
    # TYPE logconv_overall_performance gauge
    logconv_overall_performance 98.3
    # HELP logconv_total_connections Total Connections
    # TYPE logconv_total_connections gauge
    logconv_total_connections 899.0
    # HELP logconv_ldap_connections Number of LDAP Connections
    # TYPE logconv_ldap_connections gauge
    logconv_ldap_connections 752.0
    # HELP logconv_ldapi_connections Number of LDAPI Connections
    # TYPE logconv_ldapi_connections gauge
    logconv_ldapi_connections 102.0
    # HELP logconv_ldaps_connections Number of LDAPS Connections
    # TYPE logconv_ldaps_connections gauge
    logconv_ldaps_connections 45.0
    # HELP logconv_starttls_extended_ops Number of StartTLS Extended Ops
    # TYPE logconv_starttls_extended_ops gauge
    logconv_starttls_extended_ops 36.0
    # HELP logconv_searches Number of Searches
    # TYPE logconv_searches gauge
    logconv_searches 0.0
    # HELP logconv_modifications Number of Modifications
    # TYPE logconv_modifications gauge
    logconv_modifications 52.0
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
    logconv_avg_wtime 0.000637914
    # HELP logconv_avg_optime Average operation time
    # TYPE logconv_avg_optime gauge
    logconv_avg_optime 0.001315688
    # HELP logconv_avg_etime Average elapsed time
    # TYPE logconv_avg_etime gauge
    logconv_avg_etime 0.001950432
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
    5. flask

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
