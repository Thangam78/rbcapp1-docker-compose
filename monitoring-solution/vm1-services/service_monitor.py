#!/usr/bin/env python3
import json
import os
import socket
import psutil
import datetime
import socket as skt

def check_rabbitmq_port(host="localhost", port=5672):
    """Check if RabbitMQ is listening on the AMQP port"""
    try:
        with skt.create_connection((host, port), timeout=2):
            return "UP"
    except Exception:
        return "DOWN"

def check_service_process(service_name):
    """Check if a service process is running"""
    process_map = {
        'apache': ['apache2', 'httpd'],
        'postgresql': ['postgres']
    }
    target_processes = process_map.get(service_name.lower(), [service_name])
    
    for proc in psutil.process_iter(['name', 'cmdline']):
        proc_name = proc.info['name'].lower() if proc.info['name'] else ""
        cmdline = " ".join(proc.info['cmdline'] or []).lower()
        for target in target_processes:
            if target.lower() in proc_name or target.lower() in cmdline:
                return "UP"
    return "DOWN"

def monitor_services():
    """Monitor services and create JSON files"""
    services = ["apache", "rabbitmq", "postgresql"]
    host_name = socket.gethostname()
    output = {}
    
    for service in services:
        if service == "rabbitmq":
            status = check_rabbitmq_port()
        else:
            status = check_service_process(service)
        
        output[service] = status
        
        # Save individual JSON files
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/{service}-status-{timestamp}.json"
        os.makedirs("output", exist_ok=True)
        with open(filename, 'w') as f:
            json.dump({"service_name": service, "service_status": status, "host_name": host_name}, f, indent=2)
        
        print(f"Created: {filename} - {service}: {status}")
    
    # Print combined JSON for API response
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    monitor_services()
