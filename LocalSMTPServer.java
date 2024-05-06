
// import javax.mail.*;
// import javax.mail.internet.*;
import java.util.Properties;
import java.io.*;
import java.net.*;

public class LocalSMTPServer {
    public static void main(String[] args) {
        int port = 25;
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Server is listening on port " + port);
            while (true) {
                Socket socket = serverSocket.accept();
                System.out.println("New client connected");
                Thread clientThread = new Thread(new ClientHandler(socket));
                clientThread.start();
            }
        } catch (IOException e) {
            System.out.println("Server exception: " + e.getMessage());
            e.printStackTrace();
        }
    }

    static class ClientHandler implements Runnable {
        private Socket socket;

        public ClientHandler(Socket socket) {
            this.socket = socket;
        }
        
        @Override
        public void run() {
            try {
                BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));

                writer.write("220 Welcome to Local SMTP Server\r\n");
                writer.flush();

                String line = "";
                while ((line = reader.readLine()) != null) {
                    System.out.println("Client: " + line);
                    if (line.startsWith("HELO")) {
                        writer.write("250 Hello\r\n");
                        writer.flush();
                    } else if (line.startsWith("MAIL FROM:")) {
                        writer.write("250 OK\r\n");
                        writer.flush();
                    } else if (line.startsWith("RCPT TO:")) {
                        writer.write("250 OK\r\n");
                        writer.flush();
                    } else if (line.startsWith("DATA")) {
                        writer.write("354 Start mail input; end with <CRLF>.<CRLF>\r\n");
                        writer.flush();
                        String email = "";
                        while ((line = reader.readLine()) != null) {
                            System.out.println("Client: " + line);
                            if (line.equals(".")) {
                                break;
                            }
                            email += line + "\r\n";
                        }
                        System.out.println("Email: " + email);
                        writer.write("250 OK\r\n");
                        writer.flush();
                    } else if (line.startsWith("QUIT")) {
                        writer.write("221 Bye\r\n");
                        writer.flush();
                        socket.close();
                        break;
                    } else {
                        writer.write("500 Command not recognized\r\n");
                        writer.flush();
                    }
                }
            } catch (IOException e) {
                System.out.println("Client exception: " + e.getMessage());
                e.printStackTrace();
            }
        }
    }
}
