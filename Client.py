import socket
import string
import select
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)

s.connect(("0.0.0.0", 9876))

sys.stdout.write(">Welcome Stranger \n")
sys.stdout.write(">What is your Alias? \n")
alias = sys.stdin.readline()
sys.stdout.write(">Welcome " + alias + "I will connect you to others! \n")
sys.stdout.write(">Press :q anytime in order to exit! \n")
sys.stdout.write(">")
sys.stdout.flush()

while True:
    streams = [sys.stdin, s]

    # Monitor for inputs.
    readable, writable, err = select.select(streams, [], [])

    for sock in readable:
        if sock == s:
            # server message
            data = sock.recv(1024)
            if not data:
                sys.exit()
            else:
                sys.stdout.write(data.decode())
                sys.stdout.write(">")
                sys.stdout.flush()

        else:
            # client message
            msg = sys.stdin.readline()
            if msg.strip() == ":q":
                raise exit()
            s.send((alias + "    " + msg).encode())
            sys.stdout.write(">")
            sys.stdout.flush()
