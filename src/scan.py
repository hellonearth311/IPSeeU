import socket
import ipaddress
import subprocess
import re
import requests

from concurrent.futures import ThreadPoolExecutor, as_completed


def get_mac_vendor(mac):
    try:
        response = requests.get(f"https://api.macvendors.com/{mac}", timeout=3)
        return response.text if response.status_code == 200 else "Unknown"
    except:
        return "Unknown"

def ping_host(ip):
    """Ping a single host to check if it's alive"""
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '1000', str(ip)], 
                              capture_output=True, text=True, timeout=3)
        return ip if result.returncode == 0 else None
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return None

def get_mac_address(ip):
    """Get MAC address for an IP using ARP table"""
    try:
        result = subprocess.run(['arp', '-n', str(ip)], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if str(ip) in line:
                    mac_match = re.search(r'([0-9a-f]{2}[:-]){5}[0-9a-f]{2}', line, re.IGNORECASE)
                    if mac_match:
                        return mac_match.group(0)
        return "Unknown"
    except subprocess.SubprocessError:
        return "Unknown"

def scan_network_no_root(ip_range, max_workers=50):
    """Scan network without requiring root privileges"""
    try:
        network = ipaddress.ip_network(ip_range, strict=False)
    except ValueError as e:
        print(f"Invalid IP range: {e}")
        return []
    
    print(f"Scanning network: {network}")
    print(f"This will scan {network.network_address} - {network.broadcast_address}")
    
    devices = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ip = {executor.submit(ping_host, ip): ip for ip in network.hosts()}
        
        for future in as_completed(future_to_ip):
            result = future.result()
            if result:
                print(f"Found device: {result}")
                mac = get_mac_address(result)
                devices.append({
                    'ip': str(result),
                    'mac': mac
                })
    
    return devices

def get_local_subnet():
    """Get the local subnet"""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        
        network = ipaddress.ip_network(local_ip + '/24', strict=False)
        return str(network)
    except Exception as e:
        print(f"Error getting local subnet: {e}")
        return "192.168.1.0/24"