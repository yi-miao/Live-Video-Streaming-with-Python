import socket
import cv2
import pickle, struct
from pynput import keyboard
from pynput.keyboard import Key

k=Key.enter

def on_press(key):
    global k
    k=key

listener = keyboard.Listener(
	on_press=on_press)
listener.start()

host = "192.168.0.219"
port = 5000
window_size = (320,320)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))
cap = cv2.VideoCapture(0)
while(cap.isOpened()):
	ret, frame = cap.read()
	frame = cv2.resize(frame, window_size, cv2.IMREAD_UNCHANGED)
	a = pickle.dumps(frame)
	message = struct.pack("Q",len(a))+a
	client.sendall(message)
	if k==Key.esc:
		break

cap.release()  
client.close()
listener.stop()

