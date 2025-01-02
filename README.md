# IoT-Devices-Monitoring-Platform
Platform used for monitoring data provided by IoT devices, processing them through a MQTT Broker and storing them in an InfluxDB instance using microservices.
# Overview
I chose to implement the homework in Python:3.10, using the 'paho-mqtt' module(being familiar with it from the laboratory),
with a MQTT Broker based on eclipse-mosquitto(also from the laboratory). The InfluxDB image I chose from Docker Hub is 2.7,
because I am using 'influxdb-client' in python(which requires an InfluxDB version >= 2.x as I've observed) and Grafana has
the latest version.
# Workflow
I use a script for simulating data sent by IoT devices(publish.py) to the MQTT Broker. Once received, the data is processed
by the adapter(checked for correct format, timestamp and non-numerical values) and added to the InfluxDB client instance with
<location>/<station> as measurement, 'location' and 'station' as tags and each field with its corresponding value. For data
visualization, the http://<eth0>:80 can be accessed(localhost:80 address was not working and I don't know why but I would really
appreciate an explanation regarding this). By creating a Grafana Dashboard, the graph will appear depending on the Flux query.
I am using Flux instead of InfluxQL. The queries from my dashboards were generated in the InfluxDB UI available at http://<eth0>:8086
with the authentication details available in the stack.yml file('tsdb' service). The data source in Grafana was also configured
using InfluxDB with Flux as query language and all the other environment variables from the stack.yml file.
# Running
The program can be started using the 'run.sh' script which basically just joins a swarm node on the eth0 address of the host machine
(again, I don't know why I can only run it like this) if not already part of one, pulls the python image from Docker Hub if not
present, builds the required Docker images and deploys them in swarm mode. For cleaning, the 'clean.sh' script may be used.
The log messages for the adapter can be accessed with: docker service logs scd3_adapter. The data always remains, even if the stack
is removed and all the services are stopped, because of the volumes used for the 'tsdb' and 'influxdb' services, both saved in /var/lib.
