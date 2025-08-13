FROM ubuntu:20.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    apache2 \
    rabbitmq-server \
    postgresql \
    postgresql-contrib \
    python3 \
    python3-pip \
    curl \
    systemctl \
    erlang-nox \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

# Configure services
RUN systemctl enable apache2
RUN systemctl enable rabbitmq-server
RUN systemctl enable postgresql

# Setup PostgreSQL
USER postgres
RUN /etc/init.d/postgresql start && \
    psql --command "CREATE USER testuser WITH SUPERUSER PASSWORD 'testpass';" && \
    createdb -O testuser testdb
USER root

# Configure supervisor to manage services
COPY supervisor.conf /etc/supervisor/conf.d/services.conf

# Copy application files
COPY . /app/
WORKDIR /app

# Make start script executable
RUN chmod +x start-services.sh

EXPOSE 5000 80 5672 5432

CMD ["/app/start-services.sh"]
