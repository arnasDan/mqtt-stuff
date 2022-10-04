import paho.mqtt.client as mqtt
import json

MQTT_ADDRESS = '192.168.0.123'
MQTT_LAMP_TOPIC = 'zigbee2mqtt/socket'
MQTT_STRIP_TOPIC = 'zigbee2mqtt/wled/api'
MQTT_CLIENT_ID = 'LedStripLink'
LED_STRIP_PAYLOAD_OFF = json.dumps({ "on": False })
LED_STRIP_PAYLOAD_ON = json.dumps({ "ps": 2})
#TODO: track state and don't turn off if turned on manually (= lamp isn't on)
def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_LAMP_TOPIC)

def parse_mqtt_message(topic, payload):
    try:
        parsed = json.loads(payload)
        return parsed['state'] == 'ON'
    except Exception as e:
        print(e)
        return False

def send_led_strip_trigger(client, is_on):
    message = LED_STRIP_PAYLOAD_ON if is_on else LED_STRIP_PAYLOAD_OFF
    client.publish(MQTT_STRIP_TOPIC, message)

def on_message(client, userdata, msg):
    print(msg.topic + ' ' + str(msg.payload))
    is_lamp_on = parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    send_led_strip_trigger(client, is_lamp_on)

def main():
    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()

if __name__ == '__main__':
    main()
