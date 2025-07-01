# Name: Mayank Karnati

import configparser  # For reading configuration files
import logging       # For logging activity to a file
import socket        # For TCP socket communication
import json          # For encoding and decoding JSON messages

class Client:

    def __init__(self):
        # Initialize configuration parser and logger
        self.config = configparser.ConfigParser()
        self.logger = logging.getLogger(__name__)

        # Client configuration parameters
        self.serverHost : str = ""
        self.serverPort = 0
        self.logFile = ""
        self.logLevel = ""
        self.logFileMode = ""

    def readConfig(self):
        # Read client configuration from 'clientconfig' file
        self.config.read("clientconfig")
        self.serverHost = self.config["project3"]["serverHost"]
        self.serverPort = int(self.config["project3"]["serverPort"])
        self.logFile = self.config["logging"]["logFile"]
        self.logLevel = self.config["logging"]["logLevel"]
        self.logFileMode = self.config["logging"]["logFileMode"]

    def loggerManager(self):
        # Configure logging with format and level from config file
        FORMAT = '%(asctime)s: %(levelname)s %(message)s'
        log_level = getattr(logging, self.logLevel.upper(), None)
        logging.basicConfig(filename=self.logFile, level=log_level, filemode=self.logFileMode, format=FORMAT)
        self.logger.info("3461 Project3 Client starting")

    def processPayload(self, socketObj, cmd, parameter) -> bool:
        # Build and send JSON payload to server, process the response
        jsonStr = json.dumps({"command" : cmd, "parameter" : parameter})
        self.logger.info(f"Server request: {jsonStr}")
        socketObj.sendall(str.encode(jsonStr))  # Send encoded JSON string

        data = socketObj.recv(1024)  # Receive response
        self.logger.info(f"Server response: {data}")

        load = json.loads(data)  # Decode response
        response = load["response"]
        parameter = load["parameter"]

        # Handle different server responses
        if response == "QUIT":
            print(parameter)
            return True

        elif response == "SHOW":
            if parameter == "(List is empty)":
                print(parameter)
            else:
                toDoList = parameter.split(",")
                for i, item in enumerate(toDoList, 1):
                    print(f"{i}. {item}")

        elif response in {"WARNING", "ERROR"}:
            print(f"Response: {response}\nParameter: {parameter}")

        else:
            print(f"Parameter element received: {parameter}")

        return False

    def isCmdValid(self, cmd) -> bool:
        # Check if command is in the allowed set
        return cmd in {"add", "create", "delete", "help", "quit", "remove", "show"}

    def checkCmdFormat(self, tokens) -> bool:
        # Validate if commands that require parameters have them
        cmd = tokens[0].lower()
        if cmd in {"add", "create", "delete", "remove"}:
            return len(tokens) >= 2
        return True

    def printUsage(self):
        # Display usage instructions
        print("\nUsage:")
        print("\tadd <item>\t\t- Add list item")
        print("\tcreate <list name>\t- Create list")
        print("\tdelete <list name>\t- Delete list")
        print("\thelp\t\t\t- Help")
        print("\tquit\t\t\t- Quit")
        print("\tremove <item>\t\t- Remove list item")
        print("\tshow\t\t\t- Show items")

    def task(self):
        # Start client socket, handle user input and server communication
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.serverHost, self.serverPort))  # Connect to server
            print(f"Connected to server {self.serverHost} on port {self.serverPort}")
            self.logger.info(f"Connected to server {self.serverHost} on port {self.serverPort}")
            quit = False

            while not quit:
                # Read command from user
                line = input("\nEnter an input string: ")
                self.logger.info(f"Entered string = {line}")
                tokens = line.split()

                # Handle empty input
                if len(line) == 0:
                    print("No command was entered ...")
                    self.printUsage()
                    self.logger.setLevel(logging.ERROR)
                    self.logger.error("No command was entered ...")
                    self.logger.setLevel(logging.INFO)
                    continue

                # Handle invalid commands
                if not self.isCmdValid(tokens[0].lower()):
                    print(f"Invalid command entered: {tokens[0].upper()}")
                    self.printUsage()
                    self.logger.setLevel(logging.ERROR)
                    self.logger.error(f"Invalid command entered: {tokens[0].upper()}")
                    self.logger.setLevel(logging.INFO)
                    continue

                # Handle missing arguments
                if not self.checkCmdFormat(tokens):
                    print(f"Missing element in command: {tokens[0].upper()}")
                    self.printUsage()
                    self.logger.setLevel(logging.ERROR)
                    self.logger.error(f"Missing element in command: {tokens[0].upper()}")
                    self.logger.setLevel(logging.INFO)
                    continue

                # Show help text if requested
                if tokens[0].lower() == "help":
                    self.printUsage()
                    continue

                # Prepare command and parameter
                tokens[0] = tokens[0].upper()
                line = " ".join(tokens[1:])

                # Send command to server and check for termination
                quit = self.processPayload(s, tokens[0], line)

            print("Shutting down ...")
            self.logger.info("Shutting down ...")

# Instantiate and run the client
client = Client()
client.readConfig()
client.loggerManager()
client.task()
