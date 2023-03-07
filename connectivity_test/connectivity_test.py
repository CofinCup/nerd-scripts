import subprocess
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
    network1 = ipaddress.ip_network("172.23.0.0/17")
    network2 = ipaddress.ip_network("172.24.0.0/17")
    network3 = ipaddress.ip_network("172.25.0.0/17")
    network4 = ipaddress.ip_network("172.26.0.0/17")
    network5 = ipaddress.ip_network("172.27.0.0/17")
    network6 = ipaddress.ip_network("172.28.0.0/17")
    network7 = ipaddress.ip_network("172.29.0.0/17")
    print("Starting scanning for {} and {}".format(network1, network2))

    # Increase the maximum number of open files that can be opened by the process
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))

    # Scan network1
    reachable_hosts1 = scan_network(network1)
    print("Scanning finished for {} - {} hosts found".format(network1, len(reachable_hosts1)))

    # Scan network2
    reachable_hosts2 = scan_network(network2)
    print("Scanning finished for {} - {} hosts found".format(network2, len(reachable_hosts2)))

    reachable_hosts3 = scan_network(network3)
    print("Scanning finished for {} - {} hosts found".format(network3, len(reachable_hosts3)))

    reachable_hosts4 = scan_network(network4)
    print("Scanning finished for {} - {} hosts found".format(network4, len(reachable_hosts4)))

    reachable_hosts5 = scan_network(network5)
    print("Scanning finished for {} - {} hosts found".format(network5, len(reachable_hosts5)))

    reachable_hosts6 = scan_network(network6)
    print("Scanning finished for {} - {} hosts found".format(network5, len(reachable_hosts6)))

    reachable_hosts7 = scan_network(network7)
    print("Scanning finished for {} - {} hosts found".format(network5, len(reachable_hosts7)))