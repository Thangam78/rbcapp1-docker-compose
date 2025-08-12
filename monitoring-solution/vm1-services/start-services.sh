#!/bin/bash

# Initialize PostgreSQL data directory if it doesn't exist
if [ ! -d "/var/lib/postgresql/12/main" ]; then
    sudo -u postgres /usr/lib/postgresql/12/bin/initdb -D /var/lib/postgresql/12/main
fi

# Start supervisor to manage all services
/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
