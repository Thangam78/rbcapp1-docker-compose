#!/usr/bin/env python3
import json
import os
import socket
import subprocess
from datetime import datetime
import psutil

def check_service_status(service_name):
    """Check if a service is running"""
    try:
        # Map service names to process names
        process_map = {
            'httpd': ['apache2'],
            'apache2': ['apache2'],
            'rabbitmq': ['rabbitmq-server', 'beam.smp'],
            'postgresql': ['postgres']
        }
        
        target_processes = process_map.get(service_name.lower(), [service_name])
        
        # Check if any of the target processes are running
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            proc_name = proc.info['name'].lower()
            cmdline = ' '.join(proc.info['cmdline'] or []).lower()
            
            for target in target_processes:
                if target.lower() in proc_name or target.lower() in cmdline:
                    return "UP"
        return "DOWN"
    except Exception as e:
        print(f"Error checking {service_name}: {e}")
        return "DOWN"

def monitor_services():
    """Monitor services and create JSON files"""
    services = ["apache2", "rabbitmq", "postgresql"]
    host_name = socket.gethostname()
    
    for service in services:
        status = check_service_status(service)
        
        json_data = {
            "service_name": service,
            "service_status": status,
            "host_name": host_name
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/{service}-status-{timestamp}.json"
        
        os.makedirs("output", exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(json_data, f, indent=2)
        
        print(f"Created: {filename} - {service}: {status}")

if __name__ == "__main__":
    monitor_services()