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
    print(f"Conexión aceptada de {client_address} (ID: {client_id})")
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            decrypted_data = decrypt(data)
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            print(f"Recibido de {client_address} (ID: {client_id}): {decrypted_data}")
            
            # Dar prioridad a los mensajes de emergencia
            is_emergency = decrypted_data.startswith("[EMERGENCIA] ")
            
            # Transmitir a otros clientes
            for c in clients:
                if c != client_socket:
                    if is_emergency:
                        # Enviar mensaje de emergencia inmediatamente
                        c.send(encrypt(f"[{timestamp}] [EMERGENCIA] Cliente {client_id}: {decrypted_data[12:]}").encode())
                    else:
                        # Enviar mensajes normales
                        c.send(encrypt(f"[{timestamp}] Cliente {client_id}: {decrypted_data}").encode())
        except Exception as e:
            print(f"Error al manejar el cliente {client_address} (ID: {client_id}): {e}")
            break
    client_socket.close()
    clients.remove(client_socket)
    print(f"Cliente {client_address} (ID: {client_id}) desconectado")

def accept_connections():
    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

def send_message(is_emergency=False):
    message = entry.get()
    if message:
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        prefix = "[EMERGENCIA] " if is_emergency else ""
        encrypted_message = encrypt(f"{prefix}{message}")
        for client in clients:
            client.send(encrypt(f"[{timestamp}] {prefix}Servidor: {message}").encode())
        message_list.insert(tk.END, f"[{timestamp}] {prefix}Servidor: {message}")
        message_list.see(tk.END)
        entry.delete(0, tk.END)

def send_emergency_message():
    send_message(is_emergency=True)

# Server setup
HOST = '127.0.0.1'
PORT = 65432
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
clients = []

# GUI setup
root = tk.Tk()
root.title("Servidor de Chat Simple")

message_list = tk.Listbox(root, width=50, height=20)
message_list.pack(expand=True, fill="both")

entry = tk.Entry(root)
entry.pack()

button_frame = tk.Frame(root)
button_frame.pack()

send_button = tk.Button(button_frame, text="Enviar", command=send_message)
send_button.pack(side=tk.LEFT)

emergency_button = tk.Button(button_frame, text="Emergencia", command=send_emergency_message, bg="red", fg="white")
emergency_button.pack(side=tk.LEFT)

accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()

root.mainloop()

