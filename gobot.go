package main
import(
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
	"time"
)

func main(){
	if len(os.Args) != 5{
		fmt.Println("host, port, nick, channel required as args.")
		os.Exit(1)
	}
	host, port, nick, channel := os.Args[1], ":" + os.Args[2], os.Args[3], os.Args[4]
	conn := connect(host, port)
	setnick(conn, nick)
	identify(conn, nick)
	time.Sleep(500 * time.Millisecond)
	join(conn, channel)
	time.Sleep(500 * time.Millisecond)
	listen(conn)
} // end main

func connect(host, port string) (net.Conn){
	conn, err := net.Dial("tcp", host + port)
	if err != nil{
		fmt.Println(err)
		os.Exit(1)
	}
	return conn;
}

func setnick(conn net.Conn, nick string){
	mesg := fmt.Sprintf("NICK %s\r\n", nick)
	_, err := conn.Write([]byte(mesg))
	if err != nil{
		fmt.Printf("Could not set NICK: ")
		fmt.Println(err)
		os.Exit(1)
	}
}

func identify(conn net.Conn, nick string){
	mesg := fmt.Sprintf("USER %s 0 * :%s\r\n", nick, nick)
	_, err := conn.Write([]byte(mesg))
	if err != nil{
		fmt.Println(err)
		os.Exit(1)
	}
}

func join(conn net.Conn, channel string){
	mesg := fmt.Sprintf("JOIN #%s\r\n", channel)
	_, err := conn.Write([]byte(mesg))
	if err != nil{
		fmt.Println(err)
		os.Exit(1)
	}
}

func chansay(conn net.Conn, channel, mesg string){
	mesg = fmt.Sprintf("PRIVMESG #%s :%s\r\n", channel, mesg)
	_, err := conn.Write([]byte(mesg))
	if err != nil{
		fmt.Printf("Could not write to channel: ")
		fmt.Println(err)
	}
} // end chansay

func pong(conn net.Conn, resp string){
	fmt.Println(resp)
	mesg := fmt.Sprintf("PONG %s\r\n", resp)
	_, err := conn.Write([]byte(mesg))
	if err != nil{
		fmt.Printf("Could not send pong: ")
		fmt.Println(err)
	}
}

func listen(conn net.Conn){
	reader := bufio.NewReader(conn)
	// Begin infinite loop of listening
	for{
		line, err := reader.ReadString('\n')
		if err != nil{
			fmt.Println(err)
			// No graceful recovery here
		}
		if len(line) > 0 {
			line = strings.TrimRight(line, "\t\r\n")
		}
		if strings.Split(line, " ")[0] == "PING"{
			pong(conn, strings.Split(line, " ")[1])
		}
		fmt.Println(line)
	}
}
