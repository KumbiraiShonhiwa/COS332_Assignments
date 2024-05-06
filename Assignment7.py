import socket
import time

# Configuration
POP3_SERVER = 'pop.gmail.com'
POP3_PORT = 995 # Default POP3 port
YOUR_EMAIL = 'kumbishonhiwa@gmail.com'
YOUR_PASSWORD = 'pxkldkyltaofvslr'
WARNING_SUBJECT = 'Warning: You were BCCed on an email'

def download_email(server, email_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server, POP3_PORT))
        sock.recv(4096)  # Receive the welcome message
        sock.sendall(f"USER {YOUR_EMAIL}\r\n".encode())
        sock.recv(4096)  # Receive the response
        sock.sendall(f"PASS {YOUR_PASSWORD}\r\n".encode())
        sock.recv(4096)  # Receive the response
        sock.sendall(f"RETR {email_id}\r\n".encode())
        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data
        print(response.decode())
        return response

def has_bcc(email_data, your_email):
    lines = email_data.decode().lower().splitlines()
    for line in lines:
        if line.startswith('bcc:'):
            bcc_recipients = line.split(':')[1].strip().split(',')
            if your_email in bcc_recipients:
                return True
    return False

def send_warning_email(subject, body):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as smtp:
        smtp.connect(('smtp.gmail.com', 587))
        smtp.recv(4096)  # Receive the welcome message
        smtp.sendall(b"EHLO example.com\r\n")
        smtp.recv(4096)  # Receive the response
        smtp.sendall(b"STARTTLS\r\n")
        smtp.recv(4096)  # Receive the response
        smtp.sendall(f"AUTH LOGIN\r\n".encode())
        time.sleep(10)
        smtp.recv(4096)  # Receive the response
        time.sleep(10)
        smtp.sendall(f"{YOUR_EMAIL}\r\n".encode())
        time.sleep(10)
        smtp.recv(4096)  # Receive the response
        time.sleep(10)
        smtp.sendall(f"{YOUR_PASSWORD}\r\n".encode())
        time.sleep(10)
        smtp.recv(4096)  # Receive the response
        time.sleep(10)
        msg = f"From: {YOUR_EMAIL}\r\nTo: {YOUR_EMAIL}\r\nSubject: {subject}\r\n\r\n{body}\r\n.\r\n"
        time.sleep(10)
        smtp.sendall(f"MAIL FROM: <{YOUR_EMAIL}>\r\n".encode())
        time.sleep(10)
        smtp.recv(4096)  # Receive the response
        time.sleep(10)
        smtp.sendall(f"RCPT TO: <{YOUR_EMAIL}>\r\n".encode())
        time.sleep(10)
        smtp.recv(4096)  # Receive the response
        time.sleep(10)
        smtp.sendall(f"DATA\r\n".encode())
        time.sleep(10)
        smtp.recv(4096)  # Receive the response
        time.sleep(10)
        smtp.sendall(msg.encode())
        time.sleep(10)
        smtp.recv(4096)  # Receive the response
        time.sleep(10)
        smtp.sendall(b"QUIT\r\n")
        time.sleep(10)

def main():
    # Download the latest email (modify email_id if needed)
    email_data = download_email(POP3_SERVER, 1)

    # if has_bcc(email_data, YOUR_EMAIL):
        # Send warning email with original email subject in body
    # subject = f"{WARNING_SUBJECT} - {email_data.decode().splitlines()[0]}"
    # body = f"Original email subject: {subject}\n\nThis email was sent to you as a BCC recipient."
    send_warning_email("subject", "body")
    print('Done')

if __name__ == '__main__':
    main()
