import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.net.ServerSocket;
import java.util.*;
import java.util.Random;
import java.util.Base64;

public class Email {
    // Define the HTML templates
    static final String INDEX_HTML = "<!DOCTYPE html>\n" +
            "<html lang=\"en\">\n" +
            "<head>\n" +
            "    <meta charset=\"UTF-8\">\n" +
            "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n" +
            "    <title>Quiz</title>\n" +
            "</head>\n" +
            "<body>\n" +
            "    <h1>%s</h1>\n" +
            "    <form action=\"/submit\" method=\"post\">\n" +
            "        %s\n" +
            "        <input type=\"submit\" value=\"Submit\">\n" +
            "    </form>\n" +
            "</body>\n" +
            "</html>";

    static final String RESULT_HTML = "<!DOCTYPE html>\n" +
            "<html lang=\"en\">\n" +
            "<head>\n" +
            "    <meta charset=\"UTF-8\">\n" +
            "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n" +
            "    <title>Result</title>\n" +
            "</head>\n" +
            "<body>\n" +
            "    <h1>%s</h1>\n" +
            "    <a href=\"/\">Next Question</a>\n" +
            "</body>\n" +
            "</html>";

    // Define the questions
    static String[][] questions = {
            { "The successor of IPv4 is:", "-TCP", "-Ethernet", "+IPv6", "-None of the above" },
            { "DNS normally uses the following transport layer protocol:", "-TCP", "+UDP", "-IEEE 802.3",
                    "-All of the above" }
    };

    // Email configuration
    static String smtpServer = "smtp.mailtrap.io";
    static int smtpPort = 587;
    static String senderEmail = "kumbishonhiwa@gmail.com";
    static String senderPassword = "fjapfohxaovlxtvp";
    static String recipientEmail = "kumbidiscord.com";

    public static void main(String[] args) throws Exception {
        // Initialize a server socket on port 8080
        ServerSocket serverSocket = new ServerSocket(8080);
        System.out.println("Server running on port 8080...");

        // Continuously accept incoming connections
        while (true) {
            // Accept a new client connection
            Socket clientSocket = serverSocket.accept();
            System.out.println("New client connected: " + clientSocket.getInetAddress().getHostAddress());

            // Read the request data from the client
            BufferedReader reader = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            StringBuilder requestDataBuilder = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null && !line.isEmpty()) {
                requestDataBuilder.append(line).append("\r\n");
            }
            String requestData = requestDataBuilder.toString();
            // Handle the request
            handleRequest(clientSocket, requestData);
            // Close the client socket
            clientSocket.close();
        }
    }

    static String findCorrectAnswer(String[] question) {
        for (String answer : question) {
            if (answer.startsWith("+")) {
                return answer.substring(1);
            }
        }
        return "";
    }

    static String generateHtmlQuestion(String[] question) {
        StringBuilder html = new StringBuilder();
        html.append(String.format("<h2>%s</h2>\n", question[0]));
        html.append("<ul>\n");
        for (int i = 1; i < question.length; i++) {
            html.append(String.format("    <li><input type=\"radio\" name=\"answer\" value=\"%s\">%s</li>\n",
                    question[i].substring(1), question[i].substring(1)));
        }
        html.append("</ul>\n");
        return String.format(INDEX_HTML, "Quiz", html.toString());
    }

    static String generateHtmlResult(String result) {
        return String.format(RESULT_HTML, result);
    }

    static void handleRequest(Socket client_socket, String request_data) {
        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(client_socket.getInputStream()));
            BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(client_socket.getOutputStream()));

            String[] request_lines = request_data.split("\r\n");
            String[] request_line = request_lines[0].split(" ");
            String method = request_line[0];
            String path = request_line[1];
            String answer = "";

            if (method.equals("GET")) {
                if (path.equals("/")) {
                    Random rand = new Random();
                    String[] question = questions[rand.nextInt(questions.length)];
                    answer = findCorrectAnswer(question);
                    String response_body = generateHtmlQuestion(question);
                    String response = String.format("HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s",
                            response_body.length(), response_body);
                    writer.write(response);
                    writer.flush();
                } else {
                    String response = "HTTP/1.1 404 Not Found\r\n\r\n404 Not Found";
                    writer.write(response);
                    writer.flush();
                }
            } else if (method.equals("POST")) {
                if (path.equals("/submit")) {
                    String user_answer = "";
                    for (String line : request_lines) {
                        if (line.startsWith("answer=")) {
                            user_answer = line.split("=")[1];
                            break;
                        }
                    }

                    String result;
                    if (user_answer.equals(answer)) {
                        result = "Correct! Well done!";
                    } else {
                        result = String.format("Sorry, the correct answer is: %s", answer);
                    }
                    // Send email with the quiz result
                    sendEmail("Quiz Result", result);

                    String response_body = generateHtmlResult(result);
                    String response = String.format("HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s",
                            response_body.length(), response_body);
                    writer.write(response);
                    writer.flush();
                } else {
                    String response = "HTTP/1.1 404 Not Found\r\n\r\n404 Not Found";
                    writer.write(response);
                    writer.flush();
                }
            } else {
                String response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n405 Method Not Allowed";
                writer.write(response);
                writer.flush();
            }

            client_socket.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    static void sendEmail(String subject, String message) throws Exception {
        String smtpServer = "smtp.mailtrap.io";
        int port = 25; // Mailtrap SMTP port without SSL
        String username = "15f90971b5eca2";
        String password = "71bc1827e45fcc";

        // Sender and recipient details
        String senderEmail = "your_email@example.com";
        String recipientEmail = "recipient@example.com";

        
        // Construct the email content
        String emailMessage = String.format("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s",
                senderEmail, recipientEmail, subject, message);

        try (Socket socket = new Socket(smtpServer, port)) {
            BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));

            // Receive the server's greeting
            System.out.println(reader.readLine());

            // Send HELO command
            writer.write("HELO example.com\r\n");
            writer.flush();
            System.out.println(reader.readLine());

            // Send AUTH LOGIN command
            writer.write("AUTH LOGIN\r\n");
            writer.flush();
            System.out.println(reader.readLine());

            // Send base64 encoded username
            String encodedUsername = Base64.getEncoder().encodeToString(username.getBytes());
            writer.write(encodedUsername + "\r\n");
            writer.flush();
            System.out.println(reader.readLine());

            // Send base64 encoded password
            String encodedPassword = Base64.getEncoder().encodeToString(password.getBytes());
            writer.write(encodedPassword + "\r\n");
            writer.flush();
            System.out.println(reader.readLine());

            // Send MAIL FROM command
            writer.write(String.format("MAIL FROM:<%s>\r\n", senderEmail));
            writer.flush();
            System.out.println(reader.readLine());

            // Send RCPT TO command
            writer.write(String.format("RCPT TO:<%s>\r\n", recipientEmail));
            writer.flush();
            System.out.println(reader.readLine());

            // Send DATA command
            writer.write("DATA\r\n");
            writer.flush();
            System.out.println(reader.readLine());

            // Send email content
            writer.write(emailMessage);
            writer.flush();

            // Send end-of-message marker
            writer.write("\r\n.\r\n");
            writer.flush();
            System.out.println(reader.readLine());

            // Send QUIT command
            writer.write("QUIT\r\n");
            writer.flush();
            System.out.println(reader.readLine());
        }

        System.out.println("Email sent successfully!");
    }
}
