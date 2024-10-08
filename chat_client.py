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
            message_list.insert(tk.END, decrypted_data)
            message_list.see(tk.END)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def send_message():
    message = entry.get()
    if message:
        encrypted_message = encrypt(message)
        client_socket.send(encrypted_message.encode())
        message_list.insert(tk.END, f"You: {message}")
        message_list.see(tk.END)
        entry.delete(0, tk.END)

# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# GUI setup
root = tk.Tk()
root.title("Simple Chat Client")

message_list = tk.Listbox(root, width=50, height=20)
message_list.pack(expand=True, fill="both")

entry = tk.Entry(root)
entry.pack()

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

root.mainloop()

