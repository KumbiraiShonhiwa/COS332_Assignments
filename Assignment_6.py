import socket
import random
import base64

# Define the HTML templates
INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiz</title>
</head>
<body>
    <h1>{question}</h1>
    <form action="/submit" method="post">
        {options}
        <input type="submit" value="Submit">
    </form>
</body>
</html>"""

RESULT_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Result</title>
</head>
<body>
    <h1>{result}</h1>
    <a href="/">Next Question</a>
</body>
</html>"""

# Define the questions
questions = [
    {
        'question': 'The successor of IPv4 is:',
        'options': ['-TCP', '-Ethernet', '+IPv6', '-None of the above']
    },
    {
        'question': 'DNS normally uses the following transport layer protocol:',
        'options': ['-TCP', '+UDP', '-IEEE 802.3', '-All of the above']
    },
]

question = ''
answer = ''

# Email configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_email = 'kumbishonhiwa@gmail.com'
sender_password = 'fjapfohxaovlxtvp'
recipient_email = 'kumbidiscord.com'

def generate_html_question(question_data):
    options_html = ''.join(f'<input type="radio" name="answer" value="{option}"> {option} <br>' for option in question_data['options'])
    return INDEX_HTML.format(question=question_data['question'], options=options_html)

def compare_questions(question, question_data):
    return question == question_data

def findCorrectAnswer(question):
    for q in questions:
        if compare_questions(question, q):
            for option in q['options']:
                if option.startswith('+'):
                    answer = option.split('+')[1]
                    return answer
    return None

def generate_html_result(result):
    return RESULT_HTML.format(result=result)

def send_email(result):
    global recipient_email

    # Connect to SMTP server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((smtp_server, smtp_port))
    response = server_socket.recv(1024).decode()
    if response[:3] != '220':
        print('Failed to connect to SMTP server. Exiting...')
        return

    # Send EHLO
    ehlo_command = 'EHLO gmail.com\r\n'
    server_socket.send(ehlo_command.encode())
    response = server_socket.recv(1024).decode()
    print(response)

    # Start TLS
    starttls_command = 'STARTTLS\r\n'
    server_socket.send(starttls_command.encode())
    response = server_socket.recv(1024).decode()
    print(response)

    # Send EHLO again after TLS
    try:
        server_socket.send(ehlo_command.encode())
        response = server_socket.recv(1024).decode()
        print(response)
    except ConnectionResetError:
        print("The connection was reset by the server.")
    # Handle the error here, e.g., by retrying the connection or exiting the program

    # Authenticate
    auth_command = f'AUTH PLAIN\r\n'
    server_socket.send(auth_command.encode())
    response = server_socket.recv(1024).decode()
    if response[:3] != '334':
        print('Failed to authenticate with SMTP server. Exiting...')
        return

    # Send encoded username
    username = base64.b64encode(sender_email.encode()).decode() + '\r\n'
    server_socket.send(username.encode())
    response = server_socket.recv(1024).decode()
    if response[:3] != '334':
        print('Failed to send username to SMTP server. Exiting...')
        return

    # Send encoded password
    password = base64.b64encode(sender_password.encode()).decode() + '\r\n'
    server_socket.send(password.encode())
    response = server_socket.recv(1024).decode()
    if response[:3] != '235':
        print('Failed to send password to SMTP server. Exiting...')
        return

    # Compose email
    email_from = f'From: {sender_email}\r\n'
    email_to = f'To: {recipient_email}\r\n'
    email_subject = 'Subject: Quiz Results\r\n'
    email_body = f'\r\nYour quiz result is: {result}'
    email_message = email_from + email_to + email_subject + email_body

    # Send email
    server_socket.send(f'MAIL FROM: <{sender_email}>\r\n'.encode())
    response = server_socket.recv(1024).decode()
    server_socket.send(f'RCPT TO: <{recipient_email}>\r\n'.encode())
    response = server_socket.recv(1024).decode()
    server_socket.send('DATA\r\n'.encode())
    response = server_socket.recv(1024).decode()
    server_socket.send(email_message.encode())
    server_socket.send('.\r\n'.encode())
    response = server_socket.recv(1024).decode()

    # Quit
    server_socket.send('QUIT\r\n'.encode())
    server_socket.close()

def handle_request(client_socket, request_data):
    global answer
    global question
    request_lines = request_data.split('\r\n')
    method, path, _ = request_lines[0].split(' ')
    if method == 'GET':
        if path == '/':
            question = random.choice(questions)
            answer = findCorrectAnswer(question)
            response_body = generate_html_question(question)
            response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n404 Not Found"
    elif method == 'POST':
        if path == '/submit':
            user_answer = ''
            for line in request_lines:
                if line.startswith('answer=%2B'):
                    user_answer = line.split('=%2B')[1]
                    break

            if user_answer == answer:
                result = "Correct! Well done!"
            else:
                result = f"Sorry, the correct answer is: {answer}"
            
            # Send email with the quiz result
            send_email(result)

            response_body = generate_html_result(result)
            response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}"
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n404 Not Found"
    else:
        response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n405 Method Not Allowed"

    client_socket.sendall(response.encode())
    client_socket.close()

def main():
    global recipient_email

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(10)

    print("Server is listening on port 8080...")

    while True:
        client_socket, _ = server_socket.accept()
        request_data = client_socket.recv(1024).decode('utf-8')
        handle_request(client_socket, request_data)

if __name__ == "__main__":
    # Prompt for the recipient email address
    main()
