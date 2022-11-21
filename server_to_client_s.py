import socket
import threading
import cv2
import pickle,struct

host = '192.168.0.219'
port = 5000
window_size = (320,320)

def Streaming(name, sock, cap):
	while(sock and cap.isOpened()):
		try:
			ret, frame = cap.read()
			frame = cv2.resize(frame, window_size, cv2.IMREAD_UNCHANGED)
			a = pickle.dumps(frame)
			message = struct.pack("Q",len(a))+a
			sock.sendall(message)
		except:
			sock.close()
			break
        
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen(5)
print("Listening at:",(host,port))
cap = cv2.VideoCapture(0)
while True:        
	client, addr = server.accept()
	print('Connected from :',addr)
	t = threading.Thread(target = Streaming, args = ("Streaming", client, cap))
	t.start()

cap.release()  
server.close()