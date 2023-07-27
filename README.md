# cpe400 final project
# Demo
https://drive.google.com/file/d/13lAJjlnLLnG5OVbhB5lbzze9oX0eO821/view?usp=drive_link

______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________


# server.py

## Description

Server that allows multiple clients to connect and communicate with each other in real-time through a socket connection. Messages sent by clients are broadcasted to all connected clients, and the server stores all chat messages in an SQLite database.


## Functions

### `initialize_database()`

This function connects to the SQLite database and if it doesn't exist already then it creates a table named 'messages'.


### `broadcast(message, sender="Server")`

This function is responsible for sending messages to all connected clients in the chat room. It appends the current timestamp to the provided message and the sender (set to "Server"). It stores this message in the database table "messages" by entering a section protected by a lock (db_lock). After storing the message, it broadcasts it to all connected clients by iterating through the list of clients and sending the message using the send() method of their respective sockets. In case of any error during the message sending process, it prints an error message.

#### Parameters

- `message`: A string with the message to be sent.
- `sender`: A string representing the sender of the message which indicates that the message is from the server.


### `handle_client(client)`

This function is managing individual client connections. When a client connects to the server, this function is called, taking the connected socket (client) as an argument. The function starts by receiving the client's alias, adding the client and alias to their lists, and sending a welcome message to the client and broadcasting the client's connection to all other clients. It then enters a continuous loop to listen for incoming messages from other clients. When a message is received, it is decoded into a string and broadcasted to all clients. If any exception occurs or if the client exits the chat room, it removes the client's alias from the list of connected clients, and broadcasts a disconnection message to other clients.

#### Parameters

- `client`: An object representing the connection with the connected client.


### `receive()`

The receive() function sets up a loop to continuously accept client connections. When a client connection is established, a new thread is created. The function runs until server_running is set to False, and any errors during the connection handling process are caught and printed.

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

This function creates a graphical user interface (GUI) for the chat client. When called, it initializes a new window and creates a text widget for displaying incoming messages (message_text) and an entry widget for typing messages (input_entry). It defines two inner functions, send_message() and receive_messages().

#### Parameters

- `alias`: The username of the logged-in user.

### `send_message()`

This function is responsible for sending messages entered by the user in the input_entry widget to the server. It encodes the message along with the client's alias and sends it using the client.send() method. After sending the message, it clears the input_entry widget.

### `receive_messages()`

This function runs in a continuous loop to receive messages from the server and display them in the message_text widget. It decodes the received message, inserts it into the message_text widget at the end, and appends a new line.

### `register_user()`

This function controls the registration process for a new user. When called, the function retrieves the entered username and password from the corresponding entry widgets (register_username_entry and register_password_entry). It then hashes the password using the SHA-256 algorithm. The function then connects to a SQLite database file (DATABASE_FILE). It checks if the entered username already exists in the database, and if the username is not found (data is None), it inserts the new user's username and hashed password into the "users" table. If the username already exists, it displays an error message indicating that the username is already taken. Afterwards, the function clears the username and password entry widgets for the next registration attempt.

### `login_user()`

This function controls the login process. When called, the function retrieves the entered username and password from the corresponding entry widgets (login_username_entry and login_password_entry). It then hashes the entered password using the SHA-256 algorithm.

The function proceeds to connect to the SQLite database file (DATABASE_FILE) checks if the entered username and hashed password match any existing user in the "users" table. If a match is found (user is not None), it logs in. The function deletes the contents of the username and password entry widgets, updates an error label to indicate a successful login, and then destroys the login window.

After a successful login, the function sets up a socket connection to the server at IP address '127.0.0.1' and port 59000. The global client variable is used to store the socket. The user's username is sent to the server using the socket's send() method in UTF-8 encoded format.

Finally, the function calls the open_chat_window(username) function, which opens the chat window. The user's username is passed as an argument to the open_chat_window() function. If the login is unsuccessful, an error message indicating an invalid username or password is displayed in the error label.

#### Return Value

- If the login is successful, the function returns the username of the logged-in user.
- If the login fails, the function returns `None`.

## Execution

The `authenticate()` function sets up the login and registration window using Tkinter. The user can either log in with existing credentials or register as a new user.

If the login is successful, the `open_chat_window()` function creates a new window for the chat interface. The user can send and receive messages through a socket connection with the server.

# client.py
This file is the client side of the program that uses sockets over a TCP/IP network.It starts by importing the necessary modules , and then it sets up the socket connection. The host variable represents the IP address of the server to connect to, and the port variable specifies the port number to use. The client creates a TCP socket using socket.socket() and then connects to the server using client.connect().
