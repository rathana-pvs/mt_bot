import time
import paho.mqtt.client as mqtt

# Configuration
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "my_unique_test_topic/123" # Change this to be unique!

# Define what happens when we connect
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully!")
        # Subscribe to the topic upon connection
        client.subscribe(TOPIC)
    else:
        print(f"Connect failed with code {rc}")

# Define what happens when a message is received
def on_message(client, userdata, msg):
    print(f"Message received on {msg.topic}: {msg.payload.decode()}")

# Initialize the client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to HiveMQ
print(f"Connecting to {BROKER}...")
client.connect(BROKER, PORT, 60)

# Start the network loop in the background
client.loop_start()

try:
    while True:
        # Publish a message every 5 seconds
        message = input("Enter a message: ")
        client.publish(TOPIC, message)
        print(f"Publishing: {message}")
        client.publish(TOPIC, message)
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    client.loop_stop()
    client.disconnect()