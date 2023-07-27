import threading
import socket
import tkinter as tk
from hashlib import sha256
import sqlite3
DATABASE_FILE = "users.db"



def authenticate():
    login_window = tk.Tk()
    login_window.title("Login")

    login_username_label = tk.Label(login_window, text="Username:")
    login_username_label.pack()
    login_username_entry = tk.Entry(login_window)
    login_username_entry.pack()

    login_password_label = tk.Label(login_window, text="Password:")
    login_password_label.pack()
    login_password_entry = tk.Entry(login_window, show="*")
    login_password_entry.pack()

    login_error_label = tk.Label(login_window, text="", fg="red")
    login_error_label.pack()


def open_chat_window(alias):
    window = tk.Tk()
    window.title("Chat Client")

    message_text = tk.Text(window)
    message_text.pack()

    input_entry = tk.Entry(window)
    input_entry.pack()

    #handle sending messages
    def send_message():
        message = f'{alias}: {input_entry.get()}'
        client.send(message.encode('utf-8'))
        input_entry.delete(0, tk.END)

    #handle receiving messages
    def receive_messages():
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                message_text.insert(tk.END, message + "\n")
            except:
                print('Error!')
                client.close()
                break

    #button for sending messages
    send_button = tk.Button(window, text="Send", command=send_message)
    send_button.pack()

    #separate thread for receiving messages
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    # Start the event loop
    window.mainloop()


def register_user():
    username = register_username_entry.get()
    password = register_password_entry.get()

    # Hash  password
    hashed_password = sha256(password.encode()).hexdigest()

    # Insert user into the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()

    register_username_entry.delete(0, tk.END)
    register_password_entry.delete(0, tk.END)
    register_error_label.config(text="User registered successfully.")


def login_user():
    username = login_username_entry.get()
    password = login_password_entry.get()

    # Hash entered password
    hashed_password = sha256(password.encode()).hexdigest()

    # Check if the username and hashed password match
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    user = cursor.fetchone()
    conn.close()

    if user:
        login_username_entry.delete(0, tk.END)
        login_password_entry.delete(0, tk.END)
        login_error_label.config(text="Login successful.")
        login_window.destroy()

        # Socket setup
        host = '127.0.0.1'
        port = 59000
        global client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        # Send alias to server
        client.send(username.encode('utf-8'))

        # Open chat window
        open_chat_window(username)
        return username

    else:
        login_error_label.config(text="Invalid username or password.")


# window for login
login_window = tk.Tk()
login_window.title("Login")

# labels and entries for username and password
login_username_label = tk.Label(login_window, text="Username:")
login_username_label.pack()
login_username_entry = tk.Entry(login_window)
login_username_entry.pack()

login_password_label = tk.Label(login_window, text="Password:")
login_password_label.pack()
login_password_entry = tk.Entry(login_window, show="*")
login_password_entry.pack()

login_error_label = tk.Label(login_window, text="", fg="red")
login_error_label.pack()

#button for login
login_button = tk.Button(login_window, text="Login", command=login_user)
login_button.pack()

#labels and entries for registration
register_username_label = tk.Label(login_window, text="New Username:")
register_username_label.pack()
register_username_entry = tk.Entry(login_window)
register_username_entry.pack()

register_password_label = tk.Label(login_window, text="New Password:")
register_password_label.pack()
register_password_entry = tk.Entry(login_window, show="*")
register_password_entry.pack()

register_error_label = tk.Label(login_window, text="", fg="red")
register_error_label.pack()

#button for registration
register_button = tk.Button(login_window, text="Register", command=register_user)
register_button.pack()

#event loop for login window
login_window.mainloop()

