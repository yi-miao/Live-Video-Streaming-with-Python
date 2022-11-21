import socket
import cv2
import pickle,struct
from pynput import keyboard
from pynput.keyboard import Key

k=Key.enter

def on_press(key):
    global k
    k=key

listener = keyboard.Listener(
    on_press=on_press)
listener.start()

host = '192.168.0.219'
port = 5000
packet_size = 4096

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))
data = b""
payload_size = struct.calcsize("Q")
while True:
	while len(data) < payload_size:
		packet = client.recv(packet_size)
		if not packet: break
		data += packet

	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	msg_size = struct.unpack("Q",packed_msg_size)[0]
	
	while len(data) < msg_size:
		data += client.recv(packet_size)
	frame_data = data[:msg_size]
	data = data[msg_size:]

	frame = pickle.loads(frame_data)
	cv2.imshow("Streaming ", frame)
	cv2.waitKey(1)
	if k==Key.esc:
		break

client.close()
cv2.destroyAllWindows()
listener.stop()