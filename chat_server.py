import socket
import threading
import tkinter as tk
import time

client_count = 0

HOST = '127.0.0.1'
PORT = 65432

# Simple encryption (for demonstration purposes only - NOT SECURE for real-world use)
def encrypt(message):
    encrypted = ""
    for char in message:
        encrypted += chr(ord(char) + 1)
    return encrypted

def decrypt(message):
    decrypted = ""
    for char in message:
        decrypted += chr(ord(char) - 1)
    return decrypted

def handle_client(client_socket, client_address):
    global client_count
    client_id = client_count
    client_count += 1
    print(f"Accepted connection from {client_address} (ID: {client_id})")
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            decrypted_data = decrypt(data)
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            print(f"Received from {client_address} (ID: {client_id}): {decrypted_data}")
            # Broadcast to other clients
            for c in clients:
                if c != client_socket:
                    c.send(encrypt(f"[{timestamp}] Client {client_id}: {decrypted_data}").encode())
        except Exception as e:
            print(f"Error handling client {client_address} (ID: {client_id}): {e}")
            break
    client_socket.close()
    clients.remove(client_socket)
    print(f"Client {client_address} (ID: {client_id}) disconnected")

def accept_connections():
    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

def send_message():
    message = entry.get()
    if message:
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        encrypted_message = encrypt(message)
        for client in clients:
            client.send(encrypt(f"[{timestamp}] You: {message}").encode())
        message_list.insert(tk.END, f"[{timestamp}] You: {message}")
        message_list.see(tk.END)
        entry.delete(0, tk.END)

# Server setup
HOST = '127.0.0.1'
PORT = 65432
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
clients = []

# GUI setup
root = tk.Tk()
root.title("Simple Chat Server")

message_list = tk.Listbox(root, width=50, height=20)
message_list.pack(expand=True, fill="both")

entry = tk.Entry(root)
entry.pack()

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()

root.mainloop()

