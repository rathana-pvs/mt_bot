import json
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion # New Import
from publish_action import publish_message, success, failure
from db import find_by_acc_id, update_existing_bot

# from database import find_by_acc_id, update_by_acc_id

# ... (BROKER, PORT, TOPIC, map_function setup) ...
# Configuration
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "9Z4nU6wmx2o2Kz81" # Change this to be unique!

# Updated on_connect signature for API version 2
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected successfully!")
        client.subscribe(TOPIC)
    else:
        print(f"Failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        print(data, msg.properties)
        # Using match to handle different actions
        response_topic = getattr(msg.properties, 'ResponseTopic', None)
        match data.get("action"):
            case "find_data_acc_id":
                acc_id = data.get("acc_id")
                result = find_by_acc_id(acc_id)
                if result:
                    publish_message(client, response_topic, result)
                else:
                    failure(client, response_topic)
            case "update_data_acc_id":
                update_payload = data.get('payload')
                print(update_payload)
                result = update_existing_bot(update_payload)
                if result:
                    success(client, response_topic)
            case _:
                print(f"Unknown action received: {data.get('action')}")

    except Exception as e:
        print(f"Error processing message: {e}")



# Initialize the client with the required API version
client_connection = mqtt.Client(CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
client_connection.on_connect = on_connect
client_connection.on_message = on_message

# 2. MUST CONNECT FIRST
print(f"Connecting to {BROKER}...")
client_connection.connect(BROKER, PORT, 60)

client_connection.loop_forever()
# ... (Rest of your connection code) ...
