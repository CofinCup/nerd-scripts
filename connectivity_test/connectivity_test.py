import subprocess
import argparse
import ipaddress
import threading
import queue
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED, as_completed
import resource

def ping(ip, pbar):
    """
    Ping a given IP address and return True if the host is reachable, False otherwise.
    """
    try:
        output = subprocess.check_output(["ping", "-c", "1", "-W", "1", str(ip)], stderr=subprocess.DEVNULL)
        result = True
    except subprocess.CalledProcessError:
        result = False
    pbar.update(1)
    return result

def scan_network(network):
    """
    Scan all hosts in a given network and return a list of reachable hosts.
    """
    reachable_hosts = []
    ips = list(network.hosts())
    with tqdm(total=len(ips), desc="Scanning network {}".format(network)) as pbar:
        with ThreadPoolExecutor(max_workers=None) as executor:
            futures = []
            for ip in ips:
                futures.append(executor.submit(ping, ip, pbar))
            for future in as_completed(futures):
                if future.result():
                    reachable_hosts.append(str(future.result()))
    return reachable_hosts

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scan networks for reachable hosts')
    parser.add_argument('networks', metavar='CIDR address', type=str, nargs='+',
                        help='IP networks to scan(e.g. 172.25.0.0/17)')
    args = parser.parse_args()

    for network_str in args.networks:
        network = ipaddress.ip_network(network_str)
        print("Starting scanning for {}".format(network))

        # Increase the maximum number of open files that can be opened by the process
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))

        # Scan network
        reachable_hosts = scan_network(network)
        print("Scanning finished for {} - {} hosts found".format(network, len(reachable_hosts)))