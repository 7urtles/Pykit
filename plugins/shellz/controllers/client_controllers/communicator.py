import os
import json
import platform
import subprocess

from dotenv import load_dotenv
from websocket import create_connection, WebSocket
from websocket._exceptions import WebSocketConnectionClosedException




####################################################################################################

class Communicator:
	def __init__(self) -> None:
		load_dotenv()
		self.websocket = self.connect(
			# os.getenv('HOST_PUBLIC_IP'),
			# os.getenv('PORT')
			input('Enter host IP: '),
			input('Enter host port: ')
		)
		try:
			self.client_details = {
				'ip':self.websocket.sock.getsockname()[0],
				'hostname':platform.uname()[1],
				'username':subprocess.getoutput('whoami')
			}
		except AttributeError as e:
			self.close(e)

	def connect(self, host, port) -> WebSocket:
		try:
			websocket = create_connection(f"ws://{host}:{port}")
		except ConnectionRefusedError as e:
			self.close(e)
		else:
			return websocket

	def send(self, data:str) -> None:
		message = json.dumps({"content" : data})
		try:
			self.websocket.send(message)
		except WebSocketConnectionClosedException as e:
			self.close(e)

	def listen(self) -> dict:
		try:
			data = json.loads(self.websocket.recv())
			if data["keyword"] == 'exit':
				self.close()
		except WebSocketConnectionClosedException as e:
			self.close(e)		
		return data


	def close(self, error=None) -> None:
		try:
			self.websocket.close()
		except WebSocketConnectionClosedException as e:
			error = e
		except AttributeError as e:
			error = e
		if error: print(error)
		exit()