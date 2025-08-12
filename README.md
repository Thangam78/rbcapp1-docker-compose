


# 1. Create project structure
mkdir -p monitoring-solution/{vm1-services/output,vm2-elasticsearch,test2}
cd monitoring-solution

# 2. Copy all files from the artifact above

# 3. Build and start VMs
docker-compose up -d

# 4. Wait 60 seconds for services to initialize
sleep 60

# 5. Verify services are running
docker-compose exec vm1-services ps aux | grep -E "(apache|rabbitmq|postgres)"

# 6. Test Apache web server
curl http://localhost:80

# 7. Test service monitoring
docker-compose exec vm1-services python3 service_monitor.py
docker-compose exec vm1-services python3 sales-filter.py

# 8. Test REST API
curl -X POST http://localhost:5000/add -H "Content-Type: application/json" -d '{"service_name":"apache2","service_status":"UP","host_name":"vm1-host"}'
curl http://localhost:5000/healthcheck
curl http://localhost:5000/healthcheck/apache2

# 9. Verify Elasticsearch
curl http://localhost:9200/_cluster/health
curl http://localhost:9200/service-status/_search

# 7. Test sales data filtering
docker-compose exec vm1-services python3 sales-filter.py
