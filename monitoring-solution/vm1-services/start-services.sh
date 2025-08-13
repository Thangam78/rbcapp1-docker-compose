#!/bin/bash
set -e

echo "Starting services with Supervisor..."

# Initialize PostgreSQL if first run
if [ ! -d "/var/lib/postgresql/12/main" ]; then
    echo "Initializing PostgreSQL..."
    su - postgres -c "/usr/lib/postgresql/12/bin/initdb -D /var/lib/postgresql/12/main"
fi

# Ensure correct permissions
chown -R postgres:postgres /var/lib/postgresql
chown -R rabbitmq:rabbitmq /var/lib/rabbitmq

# Start Supervisor in foreground
exec /usr/bin/supervisord -n -c /etc/supervisor/conf.d/services.conf

rabbitmq-plugins enable rabbitmq_management
rabbitmq-plugins enable rabbitmq_management_agent
rabbitmq-plugins enable rabbitmq_web_dispatch

# Then start rabbitmq-server
rabbitmq-server
