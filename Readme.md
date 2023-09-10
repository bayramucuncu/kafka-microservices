# Kafka Cluster with 2 zookeeper, 2 broker nodes

# Connect to kafka container
docker exec -it [container id] /bin/bash 

## Kafka topic commands
 - List topics 
   - kafka-topics --bootstrap-server kafka-1:29092 --list
 - Create topic 
   - kafka-topics --bootstrap-server kafka-1:29092 --create --partitions 2 --replication-factor 2 --topic orders
 - Delete topic 
   - kafka-topics --bootstrap-server kafka-1:29092 --delete --topic orders
 - Describe topic
   - kafka-topics --bootstrap-server localhost:29092 --describe --topic orders
 - Consumer group list
   -  kafka-consumer-groups --bootstrap-server localhost:29092 --list

## Kafka message commands
- Add message from console 
  - kafka-console-producer --bootstrap-server kafka-1:29092 --topic orders
- Get message from console after consumer connected
  - kafka-console-consumer --bootstrap-server kafka-1:29092 --topic orders
- Get message from console after from beginning
  - kafka-console-consumer --bootstrap-server kafka-1:29092 --topic orders --from-beginning

# Running Microservices
1. Run docker compose command in terminal
    - docker-compose up
2. Run following apps:
   - order_process.py
   - inventory_process.py
   - payment_process.py
   - delivery_process
   - report_process.py