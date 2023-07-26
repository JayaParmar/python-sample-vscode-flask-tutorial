import queue
import threading
import time

# Function to process a message
def process_message(message):
    print(f"Processing message: {message}")
    time.sleep(2)  # Simulating some work being done
    print(f"Message processed: {message}")

# Function to enqueue messages
def enqueue_messages(message_queue, messages):
    for message in messages:
        message_queue.put(message)

# Number of messages to enqueue
NUM_MESSAGES = 5

# Create a queue
message_queue = queue.Queue()

# Create a list of messages
messages = [f"Message {i+1}" for i in range(NUM_MESSAGES)]

# Enqueue messages in the queue
enqueue_thread = threading.Thread(target=enqueue_messages, args=(message_queue, messages))
enqueue_thread.start()

# Create and start threads to process the messages concurrently
NUM_THREADS = 3  # You can adjust this number as per your requirement

for _ in range(NUM_THREADS):
    processing_thread = threading.Thread(target=process_message, args=(message_queue,))
    processing_thread.start()

# Wait for all threads to complete
enqueue_thread.join()
message_queue.join()

print("All messages processed.")
