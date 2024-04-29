import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

public class EmailSender {
    public static void main(String[] args) {
        String serverAddress = "127.0.0.1"; // IP address of the local machine
        int serverPort = 25; // Port number of the local SMTP server

        try {
            // Connect to the local SMTP server
            Socket socket = new Socket(serverAddress, serverPort);
            System.out.println("Connected to local SMTP server.");

            // Get input and output streams for the socket
            BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter writer = new PrintWriter(socket.getOutputStream(), true);

            // Send email message
            writer.println("HELO localhost");
            writer.println("MAIL FROM: <sender@example.com>");
            writer.println("RCPT TO: <recipient@example.com>");
            writer.println("DATA");
            writer.println("Subject: Test Email");
            writer.println();
            writer.println("This is a test email message.");
            writer.println(".");
            writer.println("QUIT");

            // Read server responses
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
                if (line.startsWith("250 ")) {
                    // SMTP server indicates successful operation
                    break;
                }
            }

            // Close resources
            reader.close();
            writer.close();
            socket.close();
            System.out.println("Disconnected from local SMTP server.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}