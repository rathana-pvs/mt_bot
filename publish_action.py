import json


def success (client, topic):
    client.publish(topic, json.dumps({"type": "success"}))

def failure (client, topic):
    client.publish(topic, json.dumps({"type": "failure"}))

def publish_message(client, topic, message):
    client.publish(topic, json.dumps({"type": "data", "payload": message}))

def publish_log(client, topic, message):
    if topic:
        client.publish(topic, json.dumps({"type": "log", "log": message}))