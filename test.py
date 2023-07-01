import paho.mqtt.client as mqtt

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        # Subscribe to the desired topic upon successful connection
        client.subscribe("/topic/sample")
    else:
        print("Connection to MQTT broker failed")

def on_message(client, userdata, msg):
    print("Received message:", msg.topic, msg.payload)

# Create MQTT client instance
mqtt_client = mqtt.Client()

# Set the callback functions
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the MQTT broker
mqtt_client.connect("localhost", 1883)

# Start the MQTT client loop to process incoming messages
mqtt_client.loop_start()

# Keep the client running until interrupted
try:
    while True:
        pass
except KeyboardInterrupt:
    # Stop the MQTT client loop and disconnect
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
