# Name: Mayank Karnati

import configparser  # Used to read configuration files
import logging       # Used for logging messages to a file
import socket        # Used for network communication
import json          # Used for serializing/deserializing JSON
import pickle        # Used to save/load Python objects to/from a file
import os            # Used for file path operations

class Server:

    def __init__(self):
        # Initialize configuration parser and logger
        self.config = configparser.ConfigParser()
        self.logger = logging.getLogger(__name__)

        # Variables related to the todo list
        self.listName = ""
        self.listInitialized = False
        self.filename : str = "mylist.pkl"
        self.todoList = []

        # Variables for server configuration and logging
        self.serverHost : str = ""
        self.serverPort = 0
        self.logFile = ""
        self.logLevel = ""
        self.logFileMode = ""

    def readConfig(self):
        # Read configuration from file 'serverconfig'
        self.config.read("serverconfig")
        self.serverHost = self.config["project3"]["serverHost"]
        self.serverPort = int(self.config["project3"]["serverPort"])
        self.logFile = self.config["logging"]["logFile"]
        self.logLevel = self.config["logging"]["logLevel"]
        self.logFileMode = self.config["logging"]["logFileMode"]

    def loggerManager(self):
        # Set up logging with format and specified log level
        FORMAT = '%(asctime)s: %(levelname)s %(message)s'
        log_level = getattr(logging, self.logLevel.upper(), None)
        logging.basicConfig(filename=self.logFile, level=log_level, filemode=self.logFileMode, format=FORMAT)
        self.logger.info("3461 Project3 Server starting")

    @staticmethod
    def save_list(data, filename):
        # Save the given data (todo list and name) to a pickle file
        with open(filename, 'wb') as file:
            pickle.dump(data, file)

    @staticmethod
    def load_list(filename):
        # Load the todo list from a pickle file if it exists
        try:
            with open(filename, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return None

    def processPackage(self, cmd, param):
        # Handle commands sent by the client and return response and message
        cmd = cmd.upper()
        response = "INFO"
        parameter = ""

        if cmd == "QUIT":
            # Save list if initialized and quit
            if self.listInitialized:
                Server.save_list((self.listName, self.todoList), self.filename)
            response = "QUIT"
            parameter = "Server shutting down"

        elif cmd == "CREATE":
            # Create a new todo list if one doesn't already exist
            if not self.listInitialized:
                self.listInitialized = True
                self.listName = param
                self.todoList = []
                response = "CREATED"
                parameter = f"Created a TODO list with name {param}"
            else:
                response = "WARNING"
                parameter = f"List already exists: {self.listName}"

        elif cmd == "ADD":
            # Add a new item to the list if not already present
            if self.listInitialized:
                if param not in self.todoList:
                    self.todoList.append(param)
                    response = "ADDED"
                    parameter = f"Added - {param} - to TODO list"
                else:
                    response = "WARNING"
                    parameter = f"Item already exists in list: {param}"
            else:
                response = "ERROR"
                parameter = "No list created. Use CREATE first."

        elif cmd == "REMOVE":
            # Remove an item from the list if it exists
            if self.listInitialized:
                if param in self.todoList:
                    self.todoList.remove(param)
                    response = "REMOVED"
                    parameter = f"Removed element - {param} - from TODO list"
                else:
                    response = "WARNING"
                    parameter = f"Item not found: {param}"
            else:
                response = "ERROR"
                parameter = "No list created. Use CREATE first."

        elif cmd == "DELETE":
            # Delete the entire list if it matches the name
            if self.listInitialized and self.listName == param:
                self.listInitialized = False
                self.listName = ""
                self.todoList = []
                if os.path.exists(self.filename):
                    os.remove(self.filename)
                response = "DELETED"
                parameter = f"Deleted TODO list {param}"
            else:
                response = "WARNING"
                parameter = f"No such list to delete: {param}"

        elif cmd == "SHOW":
            # Show current items in the list
            if self.listInitialized:
                response = "SHOW"
                parameter = ",".join(self.todoList) if self.todoList else "(List is empty)"
            else:
                response = "ERROR"
                parameter = "No list created. Use CREATE first."

        else:
            # Handle unsupported commands
            self.logger.setLevel(logging.ERROR)
            self.logger.error("The request is not supported.")
            print("The request is not supported.")
            self.logger.setLevel(logging.INFO)
            response = "ERROR"
            parameter = "Unsupported command."

        return (response, parameter)

    def task(self):
        # Load previously saved list if available
        restored = Server.load_list(self.filename)
        if restored:
            self.listName, self.todoList = restored
            self.listInitialized = True
            self.logger.info(f"Restored list '{self.listName}' from previous session.")

        # Set up server socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.serverHost, self.serverPort))
            s.listen()
            print(f"Server listening on port {self.serverPort}")
            self.logger.info(f"Server listening on port {self.serverPort}")

            # Accept a connection
            conn, addr = s.accept()
            with conn:
                print(f"Connection accepted from {addr[0]}")
                self.logger.info(f"Connection accepted from {addr[0]}")

                while True:
                    # Receive data from the client
                    data = conn.recv(1024)
                    if not data:
                        break

                    # Log received request
                    self.logger.info(f"Server request: {data}")
                    load = json.loads(data)
                    cmd, parameter = load["command"], load["parameter"]

                    # Process the request
                    response, parameter = self.processPackage(cmd, parameter)

                    # Send response back to client
                    jsonStr = json.dumps({"response": response, "parameter": parameter})
                    self.logger.info(f"Server response: {jsonStr}")
                    conn.sendall(str.encode(jsonStr))

                    # Quit condition
                    if response == "QUIT":
                        break

                print("\nServer shutting down...")
                self.logger.info("Shutting down...")

# Launch server
server = Server()
server.readConfig()
server.loggerManager()
server.task()
