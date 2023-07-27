import threading
import socket
import datetime
import sqlite3

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

host = '127.0.0.1'
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
aliases = []
server_running = True
DATABASE_FILE = "chat_messages.db"

db_lock = threading.Lock()

def initialize_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            sender TEXT,
            message TEXT
        )
    ''')

    conn.commit()
    conn.close()


def broadcast(message, sender="Server"):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message_with_timestamp = f'[{timestamp}] {message}'

    # Store the message in the database
    with db_lock:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (timestamp, sender, message) VALUES (?, ?, ?)',
                       (timestamp, sender, message))
        conn.commit()
        conn.close()

    # Broadcast the message
    for client in clients:
        try:
            client.send(message_with_timestamp.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message to client: {e}")

def handle_client(client):
    global server_running
    alias = None

    try:
        alias = client.recv(1024).decode('utf-8')
        if alias:
            clients.append(client)
            aliases.append(alias)
            client.send('You are now connected!\n'.encode('utf-8'))
            broadcast(f'{alias} has connected to the chat room!', alias )

        while server_running:
            try:
                message = client.recv(1024)
                if not message:
                    break
                decoded_message = message.decode('utf-8')
 
                broadcast(decoded_message, alias)
            except Exception as e:
                print(f"Error receiving message from client {alias}: {e}")
                break

    except Exception as e:
        print(f"Error handling client {alias}: {e}")

    finally:
        if alias:
            if client in clients:
                clients.remove(client)
            if alias in aliases:
                aliases.remove(alias)

            broadcast(f'{alias} has left the chat room!', alias)
            client.close()
            print(f"{bcolors.FAIL}{alias} has disconnected. {bcolors.ENDC}")

def receive():
    initialize_database()
    print(bcolors.OKGREEN + "Server is running." +  bcolors.ENDC)

    global server_running
    new_connection = True  #new connection
    while server_running:

        try:
            if new_connection:
                client, address = server.accept()
                print(f'{bcolors.HEADER}Connection is established with {str(address)}{bcolors.ENDC}')
                new_connection = False 
                thread = threading.Thread(target=handle_client, args=(client,))
                thread.start()
            else:
                client, address = server.accept()
                thread = threading.Thread(target=handle_client, args=(client,))
                thread.start()
        except Exception as e:
            print(f"Error accepting a connection: {e}")
            if not server_running:
                break


if __name__ == "__main__":
    try:
        receive()
    except KeyboardInterrupt:
        print("\nServer shuts down.")
        server_running = False
        for client in clients:
            client.close()
        server.close()


