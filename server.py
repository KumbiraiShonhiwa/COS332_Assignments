import socket
import base64

# Set up your email credentials and server details
smtp_server = 'smtp.mailtrap.io'
port = 25  # Mailtrap SMTP port without SSL
username = '15f90971b5eca2'
password = '71bc1827e45fcc'

# Sender and recipient details
sender_email = 'your_email@example.com'
recipient_email = 'recipient@example.com'

# Create a message to send
subject = 'Test Email from Python'
body = "This is a test email sent from Python using SMTP and Mailtrap."

# Construct the email content
email_message = f"""\
From: {sender_email}
To: {recipient_email}
Subject: {subject}

{body}
"""

# Establish a connection to the SMTP server
with socket.create_connection((smtp_server, port)) as server_socket:
    # Receive the server's greeting
    print(server_socket.recv(1024).decode())

    # Send HELO command
    server_socket.sendall(b'HELO example.com\r\n')
    print(server_socket.recv(1024).decode())

    server_socket.sendall(b'STARTTLS\r\n')
    print(server_socket.recv(1024).decode())

    server_socket.sendall(b'EHLO example.com\r\n')
    print(server_socket.recv(1024).decode())

    server_socket.sendall(b'AUTH LOGIN\r\n')
    print(server_socket.recv(1024).decode())

    # Send MAIL FROM command
    server_socket.sendall(f'MAIL FROM: <{sender_email}>\r\n'.encode())
    print(server_socket.recv(1024).decode())

    # Send RCPT TO command
    server_socket.sendall(f'RCPT TO: <{recipient_email}>\r\n'.encode())
    print(server_socket.recv(1024).decode())

    # Send DATA command
    server_socket.sendall(b'DATA\r\n')
    print(server_socket.recv(1024).decode())

    # Send email content
    server_socket.sendall(email_message.encode())
    # Send end-of-message marker
    server_socket.sendall(b'\r\n.\r\n')
    print(server_socket.recv(1024).decode())

    # Send QUIT command
    server_socket.sendall(b'QUIT\r\n')
    print(server_socket.recv(1024).decode())

print("Email sent successfully!")
