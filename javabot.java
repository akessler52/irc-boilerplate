

import java.util.List;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Scanner;

public class javabot {

    public static void main(String[] args) throws Exception {
        String server = "dot";
        String nick = "javabot";
        String login = "javabot";
        String channel = "#asdf";
        String line = null;
        List<String> L1 = new ArrayList<String>();
        Socket socket = new Socket(server, 6667);
        BufferedWriter writer = new BufferedWriter(
                new OutputStreamWriter(socket.getOutputStream( )));
        BufferedReader reader = new BufferedReader(
                new InputStreamReader(socket.getInputStream( )));
        writer.write("NICK " + nick + "\r\n");
        writer.write("USER " + login + " 8 * : laughingman\r\n");
        writer.flush( );
        while ((line = reader.readLine( )) != null) {
            if (line.indexOf("004") >= 0) {
                break;}
            else if (line.indexOf("433") >= 0) {
                System.out.println("Nickname is already in use.");
                return;}}
        writer.write("JOIN " + channel + "\r\n");
        writer.flush( );
        
        
        
        
        
        while ((line = reader.readLine( )) != null) {
        	if (line.contains("PING")==true) {
                // We must respond to PINGs to avoid being disconnected.
                writer.write("PONG " + line.substring(5) + "\r\n");
                writer.flush( );
        	}
            if (line.contains("~test")==true) {
            	writer.write("PRIVMSG " + channel + " :HELLO WORLD\r\n");
                writer.flush( );
            }
        }
    }
}
