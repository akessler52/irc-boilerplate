#BOILERBOT.py                         

#This code is intended to be a simple boilerplate for building a simple python bot.To better understand whats goin on, I recommend going through and commenting every single line with its purpose in the bot.
# https://docs.python.org/2/
# https://tools.ietf.org/html/rfc2812i
import socket              
import string
import this
                    
HOST ="dot" #yakko.cs.wmich.edu  
PORT = 6667                
NICK ="boilerbot"                                                                
IDENT = 'boilerbot'                                                                
REALNAME = 'boilerbot'                                                            
readbuffer = ""                                                                  
channel = "#asdf"                                                                
readbuffer = ''                                                                  
                                                                                 
s = socket.socket( )                                                             
print "Connecting to server: "+HOST                                              
                                                                                 
s.connect((HOST, PORT))                                                          
s.send("NICK %s\r\n" % NICK)                                                     
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))                       
s.send("JOIN #asdf\r\n")                                                         
s.send("PRIVMSG %s :CAWWW, CAWW\r\n" % channel)                
                                                                                 

print NICK,"Running"                                                           
                                                                                 
                                                                                 
def sendmessage(message):                                                        
        s.send('PRIVMSG ' +channel+' :'+message+'\r\n')                          
                                                                                  
while 1:                                                                         
        data = s.recv(2048)                                                      
        print data                                                                           
        if data.find('PING') != -1:                                              
                s.send('PONG' + data.split()[1]+'\r\n')                          
        if data.find("test") != -1:                                             
                sendmessage("BOILER BOT ALIVE")      
             
