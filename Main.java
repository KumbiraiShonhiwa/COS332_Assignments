import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.util.Base64;

public class Main {

    
    public static void main(String[] args) throws Exception {
        // Set up your email credentials and server details
        String smtpServer = "smtp.mailtrap.io";
        int port = 25; // Mailtrap SMTP port without SSL
        String username = "15f90971b5eca2";
        String password = "71bc1827e45fcc";

        // Sender and recipient details
        String senderEmail = "your_email@example.com";
        String recipientEmail = "recipient@example.com";

        // Create a message to send
        String subject = "Test Email from Java";
        String body = "This is a test email sent from Java using SMTP and Mailtrap.";

        // Construct the email content
        String emailMessage = String.format("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s",
                senderEmail, recipientEmail, subject, body);

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
