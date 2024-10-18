
import time
import paho.mqtt.client as mqtt_client
import random
from uuid import getnode as get_mac
import hashlib

broker="broker.emqx.io"
pub_id=""

if not pub_id:
    raise RuntimeError("Publisher id is not defined. Run pub.py to get ID")

h = hashlib.new('sha256')
mac = get_mac()
h.update(str(mac).encode())
sub_id = h.hexdigest()[10:20]
def on_message(client, userdata, message):
    data = str(message.payload.decode("utf-8"))
    print("received message =", data)

client = mqtt_client.Client(
    mqtt_client.CallbackAPIVersion.VERSION2,
    sub_id
)
client.on_message=on_message

print("Connecting to broker",broker)
client.connect(broker)
client.loop_start()
print("Subcribing")
client.subscribe(f"lab/{pub_id}/led/state")
time.sleep(1800)
client.disconnect()
client.loop_stop()