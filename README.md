


# 1. Clone the repo.
```bash
git clone https://github.com/Thangam78/rbcapp1-docker-compose.git
cd rbcapp1-docker-compose/monitoring-solution
```

# 2. Build and start VMs
docker-compose up -d

# 3. Wait 60 seconds for services to initialize
sleep 60

# 4. Verify services are running
docker-compose exec vm1-services ps aux | grep -E "(apache|rabbitmq|postgresql)"

# 5. Test Apache web server
curl http://localhost:80

# 6. Test service monitoring
```bash
docker-compose exec vm1-services python3 service_monitor.py

```

# 7. Test REST API
```bash
curl -X POST http://localhost:5000/add -H "Content-Type: application/json" -d '{"service_name":"apache2","service_status":"UP","host_name":"vm1-host"}'
curl http://localhost:5000/healthcheck
curl http://localhost:5000/healthcheck/apache
curl http://localhost:5000/healthcheck/postgresql
curl http://localhost:5000/healthcheck/rabbitmq
````
# 8. Test ansible playbook
```bash
docker-compose exec vm1-services ansible-playbook /app/assignment.yml -i /app/inventory_local.ini -e action=verify_install
docker-compose exec vm1-services ansible-playbook /app/assignment.yml -i /app/inventory_local.ini -e action=check-status
docker-compose exec vm1-services ansible-playbook /app/assignment.yml -i /app/inventory_local.ini -e action=check-disk
```
# 9. Verify Elasticsearch
```bash
curl http://localhost:9200/_cluster/health
curl http://localhost:9200/service-status/_search
```

# 10. Test sales data filtering
docker-compose exec vm1-services python3 sales-filter.py
