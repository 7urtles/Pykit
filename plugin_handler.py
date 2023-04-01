import sys
import subprocess
from pathlib import Path
from functools import partial


class PluginLoader:
	"""Config class for handling Flask related menu options"""
	def __init__(self):
		self.status_bar = "Home"
		self.location = Path('./plugins')
		self.excluded_names = [
			'__pycache__',
			'menu.py',
			'plugin_handler.py',
			'pykit.py',
			'requirements.txt',
			'venv',
		]
		self.plugins = self.gather_plugins()
	
	def gather_plugins(self):
		plugins = {
			folder.name:self.plugins_from_folder(folder) \
			for folder in self.location.iterdir() \
				if folder.is_dir() and folder.name not in self.excluded_names
		}
		return dict(sorted(plugins.items()))

	def plugins_from_folder(self, folder):
		folder_dict = {}
		for file in Path(folder).iterdir():
			if file.is_file() and file.name.endswith('.py'):
				if file.name not in self.excluded_names:
					folder_dict[file.name] = partial(self.run_plugin, file)
		return folder_dict

	def run_plugin(self, plugin):
		plugin_output = subprocess.call([sys.executable, plugin])
		input('\n[enter to continue]')