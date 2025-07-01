# TODO List TCP Client-Server

This project implements a Python-based TCP client-server application for managing a simple TODO list. The client sends JSON-encoded commands to the server, which maintains a persistent TODO list and responds accordingly.

## Features

- Create, add to, remove from, and delete TODO lists.
- View TODO list contents.
- Server persistence using Python pickle files.
- Configurable logging and networking via config files.
- Graceful shutdown and error handling.
- Command-line interaction for the client.

## Technologies Used

- **Python 3.x**
- **Sockets (TCP)**
- **JSON**
- **Pickle (for persistence)**
- **ConfigParser**
- **Logging**

## Getting Started

### Prerequisites

- Python 3.x installed on your system.
- The following files in the project directory:
  - `server.py`
  - `client.py`
  - `serverconfig`
  - `clientconfig`

### Installation

1️⃣ Clone or download the repository.

2️⃣ Ensure `serverconfig` and `clientconfig` contain correct host and port info.

Example `serverconfig`:
```ini
[project3]
serverHost = 127.0.0.1
serverPort = 7188

[logging]
logFile = karnati.10-project3-server.log
logLevel = INFO
logFileMode = w
```

Example `clientconfig`:
```ini
[project3]
serverHost = 127.0.0.1
serverPort = 7188

[logging]
logFile = karnati.10-project3-client.log
logLevel = INFO
logFileMode = w
```

### Running the server

```bash
python server.py
```

The server will:
- Start listening on the configured port.
- Restore any previously saved TODO list.

### Running the client

```bash
python client.py
```

The client will:
- Connect to the server.
- Accept commands interactively.

### Supported Client Commands

| Command | Description |
|----------|-------------|
| `create <listname>` | Create a new TODO list |
| `add <item>` | Add an item to the TODO list |
| `remove <item>` | Remove an item from the TODO list |
| `delete <listname>` | Delete the TODO list |
| `show` | Show all items in the list |
| `help` | Display usage instructions |
| `quit` | Disconnect and shut down server |

### Example Usage

```plaintext
Enter an input string: create todo
Enter an input string: add study
Enter an input string: show
1. study
Enter an input string: quit
```

## Logging

- Client log: `karnati.10-project3-client.log`
- Server log: `karnati.10-project3-server.log`

Logs include connection info, commands sent/received, and server responses.

## License

This project is licensed under the MIT License.
