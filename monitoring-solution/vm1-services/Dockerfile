FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    apache2 \
    rabbitmq-server \
    postgresql \
    postgresql-contrib \
    python3 \
    python3-pip \
    curl \
    ansible \
    erlang-nox \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r /app/requirements.txt
RUN pip install --upgrade ansible jinja2


# Copy Supervisor config
COPY supervisor.conf /etc/supervisor/conf.d/services.conf
COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.conf
RUN rabbitmq-plugins enable --offline rabbitmq_management

# Copy application files
COPY . /app/
WORKDIR /app

# Make start script executable
RUN chmod +x start-services.sh

EXPOSE 5000 80 5672 5432

# Start Supervisor as the main process
CMD ["/app/start-services.sh"]
