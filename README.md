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
    2. Verify Metrics Exposure:


      - You can verify the metrics exposure by accessing http://localhost:8000 in your web browser or using curl:

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
    Total users: 1
    Total groups: 6
    Total hosts: 1
    Total replicas: 1
    Total sudo rules: 0
    Total HBAC rules: 2
    Total DNS zones: 2
    Total certificates: 10
    Certificates expiring soon: 0
    Replication latency: 0.5
    dirsrv@*.service status: RUNNING
    krb5kdc.service status: RUNNING
    kadmin.service status: RUNNING
    named.service status: RUNNING
    httpd.service status: RUNNING
    ipa-custodia.service status: RUNNING
    pki-tomcatd.target status: RUNNING
    smb.service status: RUNNING
    winbind.service status: RUNNING
    ipa-otpd.socket status: RUNNING
    ipa-dnskeysyncd.service status: RUNNING
    Running logconv.pl script...
    logconv.pl output:
    ...
    logconv.pl metrics updated
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
  pip3 install prometheus_client ldap3 requests ipalib
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
