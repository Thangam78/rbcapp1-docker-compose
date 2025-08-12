#!/usr/bin/env python3
from flask import Flask, request, jsonify
import json
import os
import time
from datetime import datetime
from elasticsearch import Elasticsearch
import subprocess

app = Flask(__name__)

# Wait for Elasticsearch to be ready
def wait_for_elasticsearch():
    es_url = os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200')
    max_retries = 30
    for i in range(max_retries):
        try:
            es = Elasticsearch([es_url], timeout=30, max_retries=10, retry_on_timeout=True)
            if es.ping():
                print("Connected to Elasticsearch")
                return es
        except Exception as e:
            print(f"Waiting for Elasticsearch... ({i+1}/{max_retries})")
            time.sleep(2)
    raise Exception("Could not connect to Elasticsearch")

es = wait_for_elasticsearch()

@app.route('/add', methods=['POST'])
def add_service_data():
    """Accept JSON file and write to Elasticsearch"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Add timestamp
        data['timestamp'] = datetime.now().isoformat()
        
        # Index to Elasticsearch
        result = es.index(index="service-status", body=data)
        
        return jsonify({"message": "Data added successfully", "id": result['_id']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/healthcheck', methods=['GET'])
def get_all_status():
    """Return all application statuses"""
    try:
        # Run monitoring script to get current status
        subprocess.run(['python3', 'service_monitor.py'], cwd='/app')
        
        # Get latest status from output files and send to Elasticsearch
        output_dir = '/app/output'
        if os.path.exists(output_dir):
            for filename in os.listdir(output_dir):
                if filename.endswith('.json'):
                    with open(os.path.join(output_dir, filename), 'r') as f:
                        data = json.load(f)
                        data['timestamp'] = datetime.now().isoformat()
                        es.index(index="service-status", body=data)
        
        # Get latest status from Elasticsearch
        query = {
            "query": {"match_all": {}},
            "sort": [{"timestamp": {"order": "desc"}}],
            "size": 100
        }
        
        result = es.search(index="service-status", body=query)
        
        services_status = {}
        for hit in result['hits']['hits']:
            service = hit['_source']['service_name']
            if service not in services_status:
                services_status[service] = hit['_source']['service_status']
        
        return jsonify(services_status), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/healthcheck/<service_name>', methods=['GET'])
def get_service_status(service_name):
    """Return specific application status"""
    try:
        query = {
            "query": {"term": {"service_name.keyword": service_name}},
            "sort": [{"timestamp": {"order": "desc"}}],
            "size": 1
        }
        
        result = es.search(index="service-status", body=query)
        
        if result['hits']['hits']:
            status = result['hits']['hits'][0]['_source']['service_status']
            return jsonify({service_name: status}), 200
        else:
            return jsonify({service_name: "NOT_FOUND"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)