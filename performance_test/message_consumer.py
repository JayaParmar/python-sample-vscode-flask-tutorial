from kafka import KafkaConsumer

# Kafka broker address and port
bootstrap_servers = 'localhost:9092'

# Topic to consume messages from
topic = 'test_topic'

# Create a KafkaConsumer instance
consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers)

# Function to consume and process messages
def consume_messages():
    for message in consumer:
        print(f'Received message: {message.value.decode("utf-8")}')

if __name__ == '__main__':
    # Start consuming messages
    consume_messages()
