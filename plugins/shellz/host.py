
import os
import asyncio

from controllers.host_controllers.controller import Host
from dotenv import load_dotenv



async def main(host, port, encryption_key):
	server = Host(host, port, encryption_key)
	await server.run()


if __name__ == "__main__":
	load_dotenv()
	access_choices = {'1':'127.0.0.1', '2':'0.0.0.0'}
	#host = os.getenv('HOST_LOCAL_IP')
	host = access_choices[input("[1] Local Access\n[2] Public Access\n>")]
	port = input("Listen Port: ")
	#port = os.getenv('PORT')
	encryption_key = os.getenv('ENCRYPTION_KEY')

	asyncio.run(main(host, port, encryption_key))
