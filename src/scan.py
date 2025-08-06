import subprocess
import re
import requests
import threading

from animation import radar_animation

_scan_result = None

def _scan_worker():
    global _scan_result
    _scan_result = _scan_devices()

def scan(unique_key=None):
    global _scan_result
    _scan_result = None
    scan_thread = threading.Thread(target=_scan_worker)
    scan_thread.start()
    radar_animation(unique_key)
    scan_thread.join()
    return _scan_result

def _lookup_vendor(mac):
    try:
        resp = requests.get(f'https://api.macvendors.com/{mac}', timeout=2)
        if resp.status_code == 200:
            return resp.text
        else:
            return "Unknown"
    except Exception:
        return "Unknown"

def _scan_devices():
    """
    Scan the user's current network for all devices.
    Returns a list of dicts: [{'ip': ..., 'mac': ..., 'vendor': ...}, ...]
    """
    try:
        arp_output = subprocess.check_output(['arp', '-a']).decode()
    except Exception:
        return []

    devices = []
    for line in arp_output.splitlines():
        match = re.search(r'\((.*?)\) at ([0-9a-f:]+)', line, re.I)
        if match:
            ip = match.group(1)
            mac = match.group(2)
            vendor = _lookup_vendor(mac)
            devices.append({'ip': ip, 'mac': mac, 'vendor': vendor})
    return devices
