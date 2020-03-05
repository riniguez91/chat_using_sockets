import socket
import threading
import sys
import pickle
import os

# Un programa no consume recursos mientras que un proceso si

class Servidor():
	def __init__(self, port = input("Porfavor introduzca numero de puerto: "), host=socket.gethostname()):
		self.clientes = []
		self.sock = socket.socket()
		self.sock.bind((str(host), int(port)))
		self.sock.listen(20)
		self.sock.setblocking(False)

		aceptar = threading.Thread(target=self.aceptarC)
		procesar = threading.Thread(target=self.procesarC)
		
		print("Su ip actual es", socket.gethostbyname(host))

		aceptar.daemon = True
		aceptar.start()
		print("		___Hilo de aceptar empezado en modo DAEMON")

		procesar.daemon = True
		procesar.start()
		print("		___Hilo de procesar empezado en modo DAEMON")

		while True:
			msg = int(input('SALIR = 1\n'))
			if msg == 1:
				print("**** TALOGOOO *****")
				self.sock.close()
				sys.exit()
			else:
				pass

	def broadcast(self, msg, cliente):
		for c in self.clientes:
			try:
				if c != cliente:
					c.send(msg)
			except:
				self.clientes.remove(c)

	def aceptarC(self):
		while True:
			try:
				conn, addr = self.sock.accept()
				print(f"\nConexion aceptada via {addr}\n")
				conn.setblocking(False)
				self.clientes.append(conn)
			except:
				pass

	def procesarC(self):
		while True:
			if len(self.clientes) > 0:
				for c in self.clientes:
					try:
						data = c.recv(32)
						if data:
							print("Conexiones ahora mismo", len(self.clientes))
							print(pickle.loads(data))
							self.broadcast(data,c)
					except:
						pass

s = Servidor()