# cpe400 final project
# Demo
https://drive.google.com/file/d/13lAJjlnLLnG5OVbhB5lbzze9oX0eO821/view?usp=drive_link

# server.py

## Description

Server that allows multiple clients to connect and communicate with each other in real-time through a socket connection. Messages sent by clients are broadcasted to all connected clients, and the server stores all chat messages in an SQLite database.


## Functions

### `initialize_database()`

This function connects to the SQLite database and if it doesn't exist already then it creates a table named 'messages'.


### `broadcast(message, sender="Server")`

This function sends a message to all connected clients and stores it in the database with the a timestamp and the sender's username.

#### Parameters

- `message`: A string with the message to be sent.
- `sender`: A string representing the sender of the message which indicates that the message is from the server.


### `handle_client(client)`

This function is responsible for handling communication with clients. It listens for messages from the client and broadcasts them to other clients. It also handles client connections, disconnections, and server shutdown.

#### Parameters

- `client`: An object representing the connection with the connected client.


### `receive()`

This function is the main loop that listens for incoming client connections. It accepts incoming connections, creates a new thread to handle each client, and keeps the server running until the server_running flag is set to False.


## Execution

The script first creates a socket and listens for incoming connections from clients on the specified host and port. Once a client connects, a new thread is created using the `handle_client()` function.

The server continuously listens for incoming connections until it is shut down. The server can be shut down by using Ctrl + C.

The chat messages sent by clients are broadcasted to all connected clients, and they are also stored in the SQLite database.



# authentication.py

## Description

This module provides an authentication mechanism. It allows users to log in or register as new users.


## Functions

### `authenticate()`

This function displays a window for user login and registration. Users can enter their credentials to log in or register.


### `open_chat_window(alias)`

This function creates a new window once the user is successfully logged in. It allows users to send and receive messages through a socket connection to the server.

#### Parameters

- `alias`: The username of the logged-in user.

### `send_message()`

This function is called when the user clicks the "Send" button in the chat window. It sends the user's message to the server.


### `receive_messages()`

This function continuously listens for incoming messages from the server. When a message is received, it is displayed in the chat window.


### `register_user()`

This function is called when the user clicks the "Register" button in the login window. It registers a new user by storing their username and hashed password in the SQLite database.


### `login_user()`

This function is called when the user clicks the "Login" button. It verifies the username and password.

#### Return Value

- If the login is successful, the function returns the username of the logged-in user.
- If the login fails, the function returns `None`.

## Execution

The `authenticate()` function sets up the login and registration window using Tkinter. The user can either log in with existing credentials or register as a new user.

If the login is successful, the `open_chat_window()` function creates a new window for the chat interface. The user can send and receive messages through a socket connection with the server.

