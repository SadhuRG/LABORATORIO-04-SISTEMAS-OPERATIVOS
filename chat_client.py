import socket
import threading
import tkinter as tk

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

def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            decrypted_data = decrypt(data)
            if decrypted_data.startswith("[EMERGENCIA]"):
                message_list.insert(tk.END, decrypted_data + "\n", 'emergency')
            else:
                message_list.insert(tk.END, decrypted_data + "\n")
            message_list.see(tk.END)
        except Exception as e:
            print(f"Error al recibir mensaje: {e}")
            break

def send_message(is_emergency=False):
    message = entry.get()
    if message:
        prefix = "[EMERGENCIA] " if is_emergency else ""
        encrypted_message = encrypt(f"{prefix}{message}")
        client_socket.send(encrypted_message.encode())
        message_list.insert(tk.END, f"Tú: {prefix}{message}")
        message_list.see(tk.END)
        entry.delete(0, tk.END)

def send_emergency_message():
    send_message(is_emergency=True)

# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# GUI setup
root = tk.Tk()
root.title("Cliente de Chat Simple")

message_list = tk.Text(root, width=50, height=20)
message_list.pack(expand=True, fill="both")
message_list.tag_configure('emergency', background='red', foreground='white')

entry = tk.Entry(root)
entry.pack()

button_frame = tk.Frame(root)
button_frame.pack()

send_button = tk.Button(button_frame, text="Enviar", command=send_message)
send_button.pack(side=tk.LEFT)

emergency_button = tk.Button(button_frame, text="Emergencia", command=send_emergency_message, bg="red", fg="white")
emergency_button.pack(side=tk.LEFT)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

root.mainloop()

