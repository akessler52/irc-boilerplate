#!/usr/bin/env python
"""BOILERBOT.py

This code is intended to be a simple boilerplate
for building a simple python bot.
To better understand whats goin on,
I recommend going through and commenting
every single line with its purpose in the bot.

Fully python 3 compatible but will also
run just fine on python 2

https://docs.python.org/3/
https://tools.ietf.org/html/rfc2812i
"""

import socket

HOST = "dot"  # must be run from yakko to connect directly
PORT = 6667
NICK = "boilerbot"
IDENT = 'boilerbot'
REALNAME = 'boilerbot'
CHANNEL = "#asdf"

SOCK = socket.socket()
print("Connecting to server: " + HOST)
SOCK.connect((HOST, PORT))


def sendraw(string):
    """encode and send to server without processing"""
    print('>', string.strip())
    SOCK.send(string.encode())


def privmsg(message):
    """Send a message to CHANNEL"""
    msg = "PRIVMSG %s :%s\r\n" % (CHANNEL, message)
    sendraw(msg)


def nick(nickname):
    """Set IRC nick"""
    sendraw("NICK %s\r\n" % nickname)


def user(ident, name):
    """Set IRC user"""
    sendraw("USER %s 0 * :%s\r\n" % (ident, name))


def join(chan):
    """Join IRC channel"""
    sendraw("JOIN %s\r\n" % chan)


def pong(response):
    """Send PONG response to server PING"""
    sendraw("PONG %s\r\n" % response)


def listen():
    """Listen forever on socket"""
    while 1:
        data = SOCK.recv(2048).decode()
        for line in data.splitlines():
            print(line)
            if 'PING' == line.split()[0]:
                pong(line.split()[1])
            if 'PRIVMSG' in line:
                if '!test' in line:
                    privmsg("BOILER BOT ALIVE")

                if 'roll call' in line:
                    privmsg("CAWW, CAWW")

                if ':hi boilerbot' in line:
                    sender = line.split("!")[0][1:]
                    privmsg("%s: hi" % sender)


if __name__ == "__main__":
    nick(NICK)
    user(IDENT, REALNAME)
    join(CHANNEL)

    privmsg("Hello, I am %s" % NICK)
    print(NICK, "Running")

    listen()
