import ssl
import socket
import smtplib
from email.mime.text import MIMEText #used to create plaintext
from email.mime.multipart import MIMEMultipart #used to create multiple part text,html,attachments
from imap_tools import MailBox
import webbrowser

HOST = 'localhost'
PORT = 5569
cert_file = "certificate.crt"
key_file = "private.key"

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile=cert_file, keyfile=key_file)
#smtp
EMAIL = "ai7923665@gmail.com"
PASSWORD = "fzhreeasaiojhhzf"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
#imap
MAIL_USERNAME = "ai7923665@gmail.com"
MAIL_PASSWORD = "fzhreeasaiojhhzf"

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  #connects to smtp server of gmail using tls encryption
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

def retrieve_emails():
    emails = []
    try:
        with MailBox("imap.gmail.com").login(MAIL_USERNAME, MAIL_PASSWORD, "INBOX") as mb:
            for msg in mb.fetch(limit=2, reverse=True, mark_seen=False):
                emails.append(f"Subject: {msg.subject}, Date: {msg.date}, Body: {msg.text}")
    except Exception as e:
        emails.append(f"Failed to retrieve emails: {e}")
    return "\n".join(emails)

def process_message(message, in_ollama_chat):
    if message.lower() == 'start':
        return (
            "Hi there!!!\n"
            "Enter the number for your service...\n"
            "1 - I want Course name.\n"
            "2 - I want Professor name.\n"
            "3 - I want to know the tuition fees and the cost of re-registering the subject.\n"
            "4 - I want to know the Faculty departments.\n"
            "5 - File transfer.\n"
            "6 - Send email.\n"
            "7 - Retrieve sent emails.\n"
            "8 - How to register.\n"
            "9 - To Exit.",
            False
        )
    elif message == '1':
        return "Courses:\n- VR\n- Advantage Database\n- Network Programming\n- Parallel System\n- Computer Animation", False
    elif message == '2':
        return "Professors:\n- D.Fatima Gad Allah\n- D.Amr Amin\n- D.Mohamed Hanfy\n- D.Ahmed Adel\n- D.Marwa Abdel Azim\n- D.Noha El Shafeei", False
    elif message == '3':
        return "The tuition fees are $2100 per semester. Re-registering a subject costs $300.", False
    elif message == '4':
        return "The Faculty departments are: Computer Science, Artificial Intelligence, and Information Systems.", False
    elif message == '5':
        return "File transfer initiated. Send your file now.", False
    elif message == '6':
        send_email("alymostafaibrahim66@gmail.com", "Registration courses", "I want to know about the deadline to register for the course.")
        return "Email sent successfully.", False
    elif message == '7':
        emails = retrieve_emails()
        return f"Retrieved emails:\n{emails}", False
    elif message == '8':
        webbrowser.open("http://localhost:54512/?name=Abdo")
        return "Opening registration page...", False
    elif message == '9':
        return "Bye", False
    else:
        return "Invalid option. Please try again.", False#no further actions needed

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)#allow up to 5 clients
print(f"Server is running with SSL on port {PORT}...")

with ssl_context.wrap_socket(server_socket, server_side=True) as secure_socket:
    while True:
        client_socket, addr = secure_socket.accept()
        print(f"Connection established with {addr}")
        with client_socket:
            in_ollama_chat = False
            while True:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    if data == b"5":  # File transfer
                        with open("received_hassan.txt", "wb") as file:
                            while True:
                                chunk = client_socket.recv(1024)
                                if b"EOF" in chunk:
                                    file.write(chunk.replace(b"EOF", b""))
                                    break
                                file.write(chunk)#save file
                        with open("received_hassan.txt", "r") as file:
                            content = file.read() #store
                        client_socket.send(f"File received successfully:\n{content}".encode())
                    else:
                        response, in_ollama_chat = process_message(data.decode(), in_ollama_chat)
                        client_socket.send(response.encode())
                except Exception as e:
                    print(f"Error: {str(e)}")
                    break
