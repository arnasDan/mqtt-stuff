import paho.mqtt.client as mqtt
import json

MQTT_ADDRESS = '192.168.0.123'
MQTT_LAMP_TOPIC = 'zigbee2mqtt/socket'
MQTT_STRIP_TOPIC = 'zigbee2mqtt/wled/api'
MQTT_CLIENT_ID = 'LedStripLink'

class LedStrip():
    __off_payload = json.dumps({ "on": False })
    __on_payload = json.dumps({ "ps": 2})
    __is_on = False

    def get_payload(self):
        return self.__on_payload if self.__is_on else self.__off_payload

    #TODO: fetch led strip preset via api and leave it alone if changed
    def update_state(self, state):
        state = bool(state)
        is_new_state = self.__is_on != state
        self.__is_on = state

        return is_new_state

led_strip = LedStrip()

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_LAMP_TOPIC)

def parse_mqtt_message(topic, payload):
    try:
        parsed = json.loads(payload)
        return parsed['state'] == 'ON'
    except Exception as e:
        print(e)
        return False

def send_led_strip_trigger(client, payload):
    client.publish(MQTT_STRIP_TOPIC, payload)

def on_message(client, userdata, msg):
    is_lamp_on = parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    is_state_changed = led_strip.update_state(is_lamp_on)

    if is_state_changed:
        send_led_strip_trigger(client, led_strip.get_payload())

def main():
    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()

if __name__ == '__main__':
    main()
