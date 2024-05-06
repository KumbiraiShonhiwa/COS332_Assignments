import socket
import random

# ANSI escape sequences for screen manipulation
CLEAR_SCREEN = "\x1b[2J"
MOVE_CURSOR = "\x1b[{};{}H"

# Function to read questions from a file

def read_questions_from_file(filename):
    questions = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        question = ""
        options = []
        correct_options = []
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith('+'):
                    correct_options.append(line[1:].strip())
                elif line.startswith('-'):
                    options.append(line[1:].strip())
                else:
                    if question:
                        if not correct_options:
                            options.append("None of the above")
                            correct_options.append("None of the above")
                        questions.append((question, options, correct_options))
                    question = line
                    options = []
                    correct_options = []
        if question:  # Handle the last question
            if not correct_options:
                options.append("None of the above")
                correct_options.append("None of the above")
            questions.append((question, options, correct_options))
    return questions

# Function to format the question and options

def addAllOptions(options, correct_options):
    for option in correct_options:
        options.append(option)
    return options


# def format_question_and_options(question, options):
#     formatted_question = f"{CLEAR_SCREEN}{question}\n\n"
#     for idx, option in enumerate(options):
#         formatted_question += f"{chr(ord('A') + idx)}. {option}\n"
#     return formatted_question

def format_question_and_options(question, options):
    letter_options = [f"{chr(i+65)}. {option}" for i,
                      option in enumerate(options)]
    return f"{question}\r\n{' '.join(letter_options)}"

# Function to check if the answer is correct


# def is_correct(answer, correct_options):
#     if answer.upper() in correct_options:
#         return True
#     return False
def is_correct(answer, options, correct_options):
    correct_letters = [chr(i+65)
                       for i in range(len(options)) if correct_options[0] == options[i]]
    return answer.upper() in correct_letters


def removeCorrectOptions(options, correct_options):
    for option in correct_options:
        options.remove(option)
    return options

# Function to run the quiz server

def run_quiz_server(questions_file, port=55555):
    start = True
    # Read questions from file
    questions = read_questions_from_file(questions_file)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(5)
    print(f"Server is listening on port {port}...")

    while start:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")

        while True:
            # Randomly select a question
            question, options, correct_options = random.choice(questions)
            options = addAllOptions(options, correct_options)
            # Format question and options
            formatted_question = format_question_and_options(
                question, options)

            # Send question to client
            client_socket.sendall(formatted_question.encode())

            # Receive answer from client
            client_answer = client_socket.recv(10240).strip().decode('utf-8')

            # Check if the answer is correct

            if is_correct(client_answer, options, correct_options):
                client_socket.sendall(
                    b"\r\nCongratulations! Your answer is correct.\r\n")
                options = removeCorrectOptions(options, correct_options)
            else:
                correct_answer = ", ".join(correct_options)
                client_socket.sendall(
                    f"\r\nSorry, the correct answer is: {correct_answer}\r\n".encode())
                options = removeCorrectOptions(options, correct_options)

            # Ask if user wants to continue
            client_socket.sendall(b"Do you want to continue? (y/n): \r\n")
            continue_choice = client_socket.recv(1024).strip().decode('utf-8')
            if continue_choice.lower() != 'y':
                client_socket.sendall(b"Thanks for playing. Goodbye!\r\n")
                start = False
                client_socket.close()
                break
            else:
                client_socket.sendall(b"Let's continue!\r\n")

        # Ask if server should continue listening
        # server_socket.sendall(b"Do you want to continue listening? (y/n): ")
        # listen_choice = server_socket.recv(1024).strip().decode('utf-8')
        # if listen_choice.lower() != 'y':
        #     server_socket.sendall(b"Server is shutting down. Goodbye!\r\n")
        #     server_socket.close()
        #     break
        # else:
        #     server_socket.sendall(b"Let's continue listening!\n")
        server_socket.close()


# Run the quiz server
if __name__ == "__main__":
    print("Starting quiz server...")
    run_quiz_server("questions.txt")
