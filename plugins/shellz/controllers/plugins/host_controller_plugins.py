import json




def client_details() -> dict:
	return {
		'keyword' : 'client_details',
	}
	


def client_cwd() -> dict:
	return {
		'keyword' : 'client_cwd',
	}
	


def decrypt(decryption_key:str, files:list) -> dict:
	"""
	Append dencryption key to command string
	"""
	return {
		'keyword' : 'decrypt',
		'files' : files,
		'decryption_key' : decryption_key
	}
	


def encrypt(encryption_key:str, files:list) -> dict:
	"""
	Append encryption key to command string
	"""
	return {
		'keyword' : 'encrypt',
		'files' : files,
		'encryption_key' : encryption_key
	}
	