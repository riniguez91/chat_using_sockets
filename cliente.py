import threading
import sys
import socket
import pickle
import os

class Cliente():
	def __init__(self, host=str(input("Introduzca la ip del servidor: ")), port=int(input("Introduzca el numero del puerto "))):
		self.sock = socket.socket()
		self.port = port
		self.sock.connect((str(host), int(port)))
		hilo_recv_mensaje = threading.Thread(target=self.recibir)
		hilo_recv_mensaje.daemon = True
		hilo_recv_mensaje.start()
		print('Hilo con PID',os.getpid())
		print('Hilos activos', threading.active_count())

		while True:
			msg = input('\nEscriba texto ? ** Enviar = ENTER ** Abandonar Chat = 1 \n')
			if msg != 1 :
				self.enviar(msg)
			else:
				print(" **** TALOGOOO  ****")
				self.sock.close()
				sys.exit()

	def recibir(self):
		while True:
			try:
				data = self.sock.recv(32)
				if data:
					print(pickle.loads(data))
			except:
				pass

	def enviar(self, msg):
		self.sock.send(pickle.dumps(msg))

c = Cliente()

		