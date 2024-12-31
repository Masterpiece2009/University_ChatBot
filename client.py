import ssl
import socket
import tkinter as tk
from tkinter import scrolledtext, messagebox
import time
import os

HOST = 'localhost'
PORT = 5569

class ChatClientGUI:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("University Chat Interface")
        self.master.geometry("650x550")
        self.master.configure(bg="#1e1e2f")

        header = tk.Frame(self.master, bg="#3a3f58", pady=15)
        header.pack(fill=tk.X)
        title = tk.Label(
            header, text="University Chat Interface", font=("Helvetica", 18, "bold"),
            fg="white", bg="#3a3f58"
        )
        title.pack()

        self.chat_display = scrolledtext.ScrolledText(
            self.master, wrap=tk.WORD, width=70, height=20, font=("Helvetica", 12),
            bg="#2d2f3b", fg="#f2f2f2", highlightthickness=0, relief="flat"
        )
        self.chat_display.pack(padx=15, pady=(15, 10))
        self.chat_display.configure(state='disabled')

        bottom_frame = tk.Frame(self.master, bg="#1e1e2f")
        bottom_frame.pack(pady=(5, 15), padx=15, fill=tk.X)
        self.message_entry = tk.Entry(
            bottom_frame, width=55, font=("Helvetica", 12), bg="#3a3f58", fg="#f2f2f2",
            insertbackground="white", relief="flat"
        )
        self.message_entry.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ew")
        self.message_entry.bind("<Return>", self.send_message)
        self.send_button = tk.Button(
            bottom_frame, text="Send", font=("Helvetica", 12, "bold"), bg="#3a3f58",
            fg="white", activebackground="#5a5d6f", activeforeground="white",
            command=self.send_message, width=10, relief="flat"
        )
        self.send_button.grid(row=0, column=1, pady=5)

        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.ssl_context.load_verify_locations("certificate.crt")
        try:
            raw_socket = socket.create_connection((HOST, PORT))
            self.client_socket = self.ssl_context.wrap_socket(raw_socket, server_hostname=HOST)
            self.show_message("System: Connected securely to the server.", sender="system")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to the server: {str(e)}")
            self.master.quit()

        self.show_message("System: Welcome! Enter 'start' to see options or '0' to exit.", sender="system")

    def send_message(self, event=None):
        message = self.message_entry.get().strip()
        if message:
            self.show_message(message, sender="You")
            try:
                if message == "5":  # File transfer
                    self.send_file("hassan.txt")
                else:
                    self.client_socket.send(message.encode())
                server_response = self.client_socket.recv(1024)
                self.show_message(server_response.decode(), sender="Server")
            except Exception as e:
                messagebox.showerror("Connection Error", f"Error communicating with the server: {str(e)}")
                self.client_socket.close()
                self.master.quit()
            self.message_entry.delete(0, tk.END)

    def send_file(self, file_path):
        if not os.path.exists(file_path):
            self.show_message(f"Error: File '{file_path}' not found.", sender="system")
            return
        try:
            self.client_socket.send(b"5") # initiate file transfer
            time.sleep(0.1)
            with open(file_path, "rb") as file:
                while (data := file.read(1024)):
                    self.client_socket.sendall(data)
            self.client_socket.sendall(b"EOF")
            self.show_message("File sent successfully. Waiting for server response...", sender="system")
            server_response = self.client_socket.recv(4096)
            self.show_message(server_response.decode(), sender="Server")
        except Exception as e:
            self.show_message(f"Error sending file: {str(e)}", sender="system")

    def show_message(self, message, sender="System"):
        self.chat_display.config(state='normal')
        if sender == "You":
            tag = "user"
            self.chat_display.insert(tk.END, f"\nYou: {message}\n", tag)
        elif sender == "Server":
            tag = "server"
            self.chat_display.insert(tk.END, f"\nServer: {message}\n", tag)
        else:
            tag = "system"
            self.chat_display.insert(tk.END, f"\n{message}\n", tag)
        self.chat_display.tag_config("user", foreground="#8db6cd", font=("Helvetica", 12, "italic"))
        self.chat_display.tag_config("server", foreground="#98c379", font=("Helvetica", 12))
        self.chat_display.tag_config("system", foreground="#888888", font=("Helvetica", 12, "italic"))
        self.chat_display.config(state='disabled')
        self.animate_scroll_to_end()

    def animate_scroll_to_end(self):
        for i in range(5):
            self.chat_display.yview(tk.END)
            self.master.update_idletasks()
            time.sleep(0.03)

    def run(self):
        self.master.mainloop()

# Run the application
if __name__ == "__main__":
    app = ChatClientGUI()
    app.run()
