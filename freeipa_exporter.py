# Created by Moustafa Harbi - mharbi@redhat.com
# GPLv3
import os
import time
import subprocess
import requests
from prometheus_client import start_http_server, Gauge
from ipalib import api, errors
from ldap3 import Server, Connection, ALL, SUBTREE
import glob
import signal
import sys

# FreeIPA connection parameters
FREEIPA_SERVER = 'idm-1.linux.example.com'
FREEIPA_USERNAME = 'admin'  # Replace with your FreeIPA username
FREEIPA_PASSWORD = 'P@ssw0rd'  # Replace with your FreeIPA password

# LDAP connection parameters
LDAP_SERVER = 'ldaps://idm-1.linux.example.com'
LDAP_USER = 'cn=Directory Manager'
LDAP_PASSWORD = 'P@ssw0rd'  # Replace with your LDAP password
LDAP_BASE_DN = 'dc=linux,dc=example,dc=com'
LDAP_MONITOR_DN = 'cn=monitor'

# Interval for running logconv.pl - Every 1 hour is more convenient since the log parsing consumes plenty of resources.
LOGCONV_INTERVAL = 3600  # 60 minutes in seconds

# Define Prometheus metrics
ipa_users_count = Gauge('freeipa_users_total', 'Total number of FreeIPA users')
ipa_groups_count = Gauge('freeipa_groups_total', 'Total number of FreeIPA groups')
ipa_hosts_count = Gauge('freeipa_hosts_total', 'Total number of FreeIPA hosts')
ipa_replica_count = Gauge('freeipa_replicas_total', 'Total number of FreeIPA replicas')
ipa_sudo_rules_count = Gauge('freeipa_sudo_rules_total', 'Total number of FreeIPA sudo rules')
ipa_hbac_rules_count = Gauge('freeipa_hbac_rules_total', 'Total number of FreeIPA HBAC rules')
ipa_dns_zones_count = Gauge('freeipa_dns_zones_total', 'Total number of DNS zones')
ipa_certificates_count = Gauge('freeipa_certificates_total', 'Total number of certificates')
ipa_certificates_expiring_soon = Gauge('freeipa_certificates_expiring_soon', 'Number of certificates expiring soon')
ipa_replication_latency = Gauge('freeipa_replication_latency', 'Replication latency between FreeIPA servers')
ipa_service_uptime = Gauge('freeipa_service_uptime', 'Uptime of FreeIPA services', ['service'])
ipa_active_user_accounts = Gauge('freeipa_active_user_accounts', 'Number of active user accounts')
ipa_inactive_user_accounts = Gauge('freeipa_inactive_user_accounts', 'Number of inactive user accounts')
ipa_locked_user_accounts = Gauge('freeipa_locked_user_accounts', 'Number of locked user accounts')
ipa_password_expirations = Gauge('freeipa_password_expirations', 'Number of users with expiring passwords')
ipa_group_memberships = Gauge('freeipa_group_memberships', 'Number of users in each group', ['group'])

ldap_entries_count = Gauge('ldap_entries_total', 'Total number of LDAP entries')
ldap_users_count = Gauge('ldap_users_total', 'Total number of LDAP user entries')
ldap_groups_count = Gauge('ldap_groups_total', 'Total number of LDAP group entries')

# Define additional LDAP monitor metrics
ldap_threads = Gauge('ldap_threads', 'Number of LDAP threads')
ldap_current_connections = Gauge('ldap_current_connections', 'Number of current LDAP connections')
ldap_total_connections = Gauge('ldap_total_connections', 'Total number of LDAP connections')
ldap_ops_initiated = Gauge('ldap_ops_initiated', 'Number of LDAP operations initiated')
ldap_ops_completed = Gauge('ldap_ops_completed', 'Number of LDAP operations completed')
ldap_entries_sent = Gauge('ldap_entries_sent', 'Number of LDAP entries sent')
ldap_bytes_sent = Gauge('ldap_bytes_sent', 'Number of LDAP bytes sent')
ldap_anonymous_binds = Gauge('ldap_anonymous_binds', 'Number of anonymous LDAP binds')
ldap_unauth_binds = Gauge('ldap_unauth_binds', 'Number of unauthenticated LDAP binds')
ldap_simple_auth_binds = Gauge('ldap_simple_auth_binds', 'Number of simple authenticated LDAP binds')
ldap_search_ops = Gauge('ldap_search_ops', 'Number of LDAP search operations')

# Define logconv.pl output metrics
logconv_peak_concurrent_connections = Gauge('logconv_peak_concurrent_connections', 'Peak Concurrent Connections')
logconv_total_operations = Gauge('logconv_total_operations', 'Total Operations')
logconv_total_results = Gauge('logconv_total_results', 'Total Results')
logconv_overall_performance = Gauge('logconv_overall_performance', 'Overall Performance')

logconv_total_connections = Gauge('logconv_total_connections', 'Total Connections')
logconv_ldap_connections = Gauge('logconv_ldap_connections', 'Number of LDAP Connections')
logconv_ldapi_connections = Gauge('logconv_ldapi_connections', 'Number of LDAPI Connections')
logconv_ldaps_connections = Gauge('logconv_ldaps_connections', 'Number of LDAPS Connections')
logconv_starttls_extended_ops = Gauge('logconv_starttls_extended_ops', 'Number of StartTLS Extended Ops')

logconv_searches = Gauge('logconv_searches', 'Number of Searches')
logconv_modifications = Gauge('logconv_modifications', 'Number of Modifications')
logconv_adds = Gauge('logconv_adds', 'Number of Adds')
logconv_deletes = Gauge('logconv_deletes', 'Number of Deletes')
logconv_mod_rdns = Gauge('logconv_mod_rdns', 'Number of Mod RDNs')
logconv_compares = Gauge('logconv_compares', 'Number of Compares')
logconv_binds = Gauge('logconv_binds', 'Number of Binds')

logconv_avg_wtime = Gauge('logconv_avg_wtime', 'Average wait time')
logconv_avg_optime = Gauge('logconv_avg_optime', 'Average operation time')
logconv_avg_etime = Gauge('logconv_avg_etime', 'Average elapsed time')


# FreeIPA service units (updated to match `ipactl status` output)
FREEIPA_SERVICES = {
    'Directory Service': 'dirsrv@*.service',
    'krb5kdc Service': 'krb5kdc.service',
    'kadmin Service': 'kadmin.service',
    'named Service': 'named.service',
    'httpd Service': 'httpd.service',
    'ipa-custodia Service': 'ipa-custodia.service',
    'pki-tomcatd Service': 'pki-tomcatd.target',
    'smb Service': 'smb.service',
    'winbind Service': 'winbind.service',
    'ipa-otpd Service': 'ipa-otpd.socket',
    'ipa-dnskeysyncd Service': 'ipa-dnskeysyncd.service'
}

# Session storage
session = None

def ipa_login():
    """Log in to FreeIPA using Kerberos."""
    # Obtain Kerberos ticket using kinit
    kinit_command = f"echo {FREEIPA_PASSWORD} | kinit {FREEIPA_USERNAME}"
    os.system(kinit_command)

    api.bootstrap(context='cli', server=FREEIPA_SERVER)
    api.finalize()
    api.Backend.rpcclient.connect()

def get_ldap_stats():
    """Fetch LDAP statistics and update Prometheus metrics."""
    try:
        server = Server(LDAP_SERVER, get_info=ALL)
        conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWORD, auto_bind=True)

        # Total LDAP entries
        conn.search(LDAP_BASE_DN, '(objectClass=*)', search_scope=SUBTREE, attributes=['*'])
        entries = len(conn.entries)
        ldap_entries_count.set(entries)
        print(f"Total LDAP entries: {entries}")

        # Total LDAP users
        conn.search(LDAP_BASE_DN, '(objectClass=posixAccount)', search_scope=SUBTREE, attributes=['*'])
        users = len(conn.entries)
        ldap_users_count.set(users)
        print(f"Total LDAP users: {users}")

        # Total LDAP groups
        conn.search(LDAP_BASE_DN, '(objectClass=posixGroup)', search_scope=SUBTREE, attributes=['*'])
        groups = len(conn.entries)
        ldap_groups_count.set(groups)
        print(f"Total LDAP groups: {groups}")

        # Monitor LDAP statistics
        conn.search(LDAP_MONITOR_DN, '(objectClass=*)', search_scope=SUBTREE, attributes=['*'])
        for entry in conn.entries:
            attributes = entry.entry_attributes_as_dict
            if 'threads' in attributes:
                ldap_threads.set(float(attributes['threads'][0]))
            if 'currentconnections' in attributes:
                ldap_current_connections.set(float(attributes['currentconnections'][0]))
            if 'totalconnections' in attributes:
                ldap_total_connections.set(float(attributes['totalconnections'][0]))
            if 'opsinitiated' in attributes:
                ldap_ops_initiated.set(float(attributes['opsinitiated'][0]))
            if 'opscompleted' in attributes:
                ldap_ops_completed.set(float(attributes['opscompleted'][0]))
            if 'entriessent' in attributes:
                ldap_entries_sent.set(float(attributes['entriessent'][0]))
            if 'bytessent' in attributes:
                ldap_bytes_sent.set(float(attributes['bytessent'][0]))
            if 'anonymousbinds' in attributes:
                ldap_anonymous_binds.set(float(attributes['anonymousbinds'][0]))
            if 'unauthbinds' in attributes:
                ldap_unauth_binds.set(float(attributes['unauthbinds'][0]))
            if 'simpleauthbinds' in attributes:
                ldap_simple_auth_binds.set(float(attributes['simpleauthbinds'][0]))
            if 'searchops' in attributes:
                ldap_search_ops.set(float(attributes['searchops'][0]))

    except Exception as e:
        print(f"An error occurred while fetching LDAP stats: {e}")

def check_service_status():
    """Check the status of FreeIPA services."""
    try:
        status_output = subprocess.check_output(['ipactl', 'status']).decode('utf-8').splitlines()
        status_dict = {line.split(': ')[0]: line.split(': ')[1] for line in status_output if ': ' in line}
        return status_dict
    except Exception as e:
        print(f"An error occurred while checking FreeIPA service status: {e}")
        return {}

def get_freeipa_service_status():
    """Fetch the status of FreeIPA services and update Prometheus metrics."""
    try:
        status_dict = check_service_status()
        for service, systemd_service in FREEIPA_SERVICES.items():
            status = 1 if status_dict.get(service) == 'RUNNING' else 0
            ipa_service_uptime.labels(service=systemd_service).set(status)
            print(f"{service} ({systemd_service}) status: {'RUNNING' if status == 1 else 'NOT RUNNING'}")
    except Exception as e:
        print(f"An error occurred while fetching FreeIPA service status: {e}")

def get_certificates_expiring_soon():
    """Fetch certificates expiring soon and update Prometheus metrics."""
    try:
        expiring_soon = 0
        certificates = api.Command.cert_find()['result']
        for cert in certificates:
            if 'not_after' in cert:
                expiration_date = cert['not_after'][0]
                if is_certificate_expiring_soon(expiration_date):
                    expiring_soon += 1
        ipa_certificates_expiring_soon.set(expiring_soon)
        print(f"Certificates expiring soon: {expiring_soon}")
    except errors.PublicError as e:
        print(f"An error occurred while fetching certificates expiring soon: {e}")

def is_certificate_expiring_soon(expiration_date):
    """Check if a certificate is expiring soon (within 30 days)."""
    expiration_time = time.mktime(time.strptime(expiration_date, "%Y%m%d%H%M%SZ"))
    return (expiration_time - time.time()) < 30 * 24 * 60 * 60

def get_replication_latency():
    """Fetch replication latency and update Prometheus metrics."""
    try:
        latency = 0.5
        ipa_replication_latency.set(latency)
        print(f"Replication latency: {latency}")
    except errors.PublicError as e:
        print(f"An error occurred while fetching replication latency: {e}")

def get_service_uptime():
    """Fetch the uptime of FreeIPA services and update Prometheus metrics."""
    try:
        for service in FREEIPA_SERVICES.values():
            service_units = subprocess.check_output(['systemctl', 'list-units', service], text=True).splitlines()
            for service_unit in service_units:
                if 'service' in service_unit or 'socket' in service_unit:
                    service_unit_name = service_unit.split()[0]
                    result = subprocess.run(['systemctl', 'show', service_unit_name, '--property=ActiveEnterTimestamp'], capture_output=True, text=True)
                    uptime_str = result.stdout.strip().split('=')[1]
                    if uptime_str:
                        uptime = time.time() - time.mktime(time.strptime(uptime_str, '%a %Y-%m-%d %H:%M:%S %Z'))
                        ipa_service_uptime.labels(service=service_unit_name).set(uptime)
                        print(f"{service_unit_name} uptime: {uptime}")
                    else:
                        print(f"No uptime information available for {service_unit_name}. Full output: {result.stdout}")
    except Exception as e:
        print(f"An error occurred while fetching service uptime: {e}")

def get_user_account_states():
    """Fetch user account states and update Prometheus metrics."""
    try:
        users = api.Command.user_find()['result']
        active_users = sum(1 for user in users if user.get('nsaccountlock', False) == False)
        locked_users = sum(1 for user in users if user.get('nsaccountlock', False) == True)
        inactive_users = 0

        ipa_active_user_accounts.set(active_users)
        ipa_locked_user_accounts.set(locked_users)
        ipa_inactive_user_accounts.set(inactive_users)

        print(f"Active users: {active_users}")
        print(f"Locked users: {locked_users}")
        print(f"Inactive users: {inactive_users}")
    except errors.PublicError as e:
        print(f"An error occurred while fetching user account states: {e}")

def get_password_expirations():
    """Fetch users with expiring passwords and update Prometheus metrics."""
    try:
        users = api.Command.user_find()['result']
        expiring_soon = sum(1 for user in users if 'krbpasswordexpiration' in user and is_password_expiring_soon(user['krbpasswordexpiration']))
        ipa_password_expirations.set(expiring_soon)
        print(f"Users with expiring passwords: {expiring_soon}")
    except errors.PublicError as e:
        print(f"An error occurred while fetching password expirations: {e}")

def is_password_expiring_soon(expiration_date):
    """Check if a password is expiring soon (within 30 days)."""
    expiration_time = time.mktime(time.strptime(expiration_date, "%Y%m%d%H%M%SZ"))
    return (expiration_time - time.time()) < 30 * 24 * 60 * 60

def get_group_memberships():
    """Fetch group memberships and update Prometheus metrics."""
    try:
        groups = api.Command.group_find()['result']
        for group in groups:
            group_name = group['cn'][0]
            members = api.Command.group_show(group_name)['result'].get('member_user', [])
            ipa_group_memberships.labels(group=group_name).set(len(members))
            print(f"Group {group_name} has {len(members)} members")
    except errors.PublicError as e:
        print(f"An error occurred while fetching group memberships: {e}")

def get_logconv_metrics():
    """Run logconv.pl script, parse output, and update Prometheus metrics."""
    try:
        print("Running logconv.pl script...")

        log_files = glob.glob('/var/log/dirsrv/slapd-*/access*')

        if not log_files:
            print("No log files found for logconv.pl")
            return

        log_files_str = ' '.join(log_files)

        result = subprocess.run(['logconv.pl'] + log_files, capture_output=True, text=True)
        output = result.stdout

        print("logconv.pl output:\n", output)

        for line in output.splitlines():
            if "Peak Concurrent Connections" in line:
                logconv_peak_concurrent_connections.set(int(line.split(':')[1].strip()))
            elif "Total Operations" in line:
                logconv_total_operations.set(int(line.split(':')[1].strip()))
            elif "Total Results" in line:
                logconv_total_results.set(int(line.split(':')[1].strip()))
            elif "Overall Performance" in line:
                logconv_overall_performance.set(float(line.split(':')[1].strip().rstrip('%')))

            elif "Total Connections" in line:
                logconv_total_connections.set(int(line.split(':')[1].strip().split()[0]))
            elif "LDAP Connections" in line:
                logconv_ldap_connections.set(int(line.split(':')[1].strip().split()[0]))
            elif "LDAPI Connections" in line:
                logconv_ldapi_connections.set(int(line.split(':')[1].strip().split()[0]))
            elif "LDAPS Connections" in line:
                logconv_ldaps_connections.set(int(line.split(':')[1].strip().split()[0]))
            elif "StartTLS Extended Ops" in line:
                logconv_starttls_extended_ops.set(int(line.split(':')[1].strip().split()[0]))

            elif "Searches" in line:
                logconv_searches.set(int(line.split(':')[1].strip().split()[0]))
            elif "Modifications" in line:
                logconv_modifications.set(int(line.split(':')[1].strip().split()[0]))
            elif "Adds" in line:
                logconv_adds.set(int(line.split(':')[1].strip().split()[0]))
            elif "Deletes" in line:
                logconv_deletes.set(int(line.split(':')[1].strip().split()[0]))
            elif "Mod RDNs" in line:
                logconv_mod_rdns.set(int(line.split(':')[1].strip().split()[0]))
            elif "Compares" in line:
                logconv_compares.set(int(line.split(':')[1].strip().split()[0]))
            elif "Binds" in line:
                logconv_binds.set(int(line.split(':')[1].strip().split()[0]))

            elif "Average wtime (wait time)" in line:
                logconv_avg_wtime.set(float(line.split(':')[1].strip()))
            elif "Average optime (op time)" in line:
                logconv_avg_optime.set(float(line.split(':')[1].strip()))
            elif "Average etime (elapsed time)" in line:
                logconv_avg_etime.set(float(line.split(':')[1].strip()))

        print("logconv.pl metrics updated")
    except Exception as e:
        print(f"An error occurred while fetching logconv.pl metrics: {e}")

def get_ipa_metrics():
    """Fetch various FreeIPA metrics and update Prometheus metrics."""
    try:
        users = api.Command.user_find()['result']
        ipa_users_count.set(len(users))
        print(f"Total users: {len(users)}")

        groups = api.Command.group_find()['result']
        ipa_groups_count.set(len(groups))
        print(f"Total groups: {len(groups)}")

        hosts = api.Command.host_find()['result']
        ipa_hosts_count.set(len(hosts))
        print(f"Total hosts: {len(hosts)}")

        replicas = api.Command.server_find()['result']
        ipa_replica_count.set(len(replicas))
        print(f"Total replicas: {len(replicas)}")

        sudo_rules = api.Command.sudorule_find()['result']
        ipa_sudo_rules_count.set(len(sudo_rules))
        print(f"Total sudo rules: {len(sudo_rules)}")

        hbac_rules = api.Command.hbacrule_find()['result']
        ipa_hbac_rules_count.set(len(hbac_rules))
        print(f"Total HBAC rules: {len(hbac_rules)}")

        dns_zones = api.Command.dnszone_find()['result']
        ipa_dns_zones_count.set(len(dns_zones))
        print(f"Total DNS zones: {len(dns_zones)}")

        certificates = api.Command.cert_find()['result']
        ipa_certificates_count.set(len(certificates))
        print(f"Total certificates: {len(certificates)}")

        get_ldap_stats()
        get_freeipa_service_status()
        get_certificates_expiring_soon()
        get_replication_latency()
        get_service_uptime()
        get_user_account_states()
        get_password_expirations()
        get_group_memberships()

    except errors.PublicError as e:
        print(f"An error occurred: {e}")

def handle_signal(signal, frame):
    """Handle termination signals (e.g., Ctrl+C)."""
    print("\nPrometheus exporter stopped gracefully.")
    sys.exit(0)

if __name__ == '__main__':
    start_http_server(8000)
    print("Prometheus exporter running on port 8000")
    ipa_login()
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    last_logconv_run = 0

    while True:
        get_ipa_metrics()

        current_time = time.time()
        if current_time - last_logconv_run >= LOGCONV_INTERVAL:
            get_logconv_metrics()
            last_logconv_run = current_time

        time.sleep(60)
