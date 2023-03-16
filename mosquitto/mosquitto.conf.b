# following two lines required for > v2.0
listener 1883
allow_anonymous true

# MQTT over TLS/SSL with certificates
listener 8888
protocol mqtt
require_certificate true
cafile /etc/mosquitto/certs/ca.crt
keyfile /etc/mosquitto/certs/server.key
certfile /etc/mosquitto/certs/server.crt
tls_version tlsv1


persistence true
log_dest file /etc/mosquitto/mosquitto.log

