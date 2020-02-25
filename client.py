import socket
import threading
import time
import signal
import sys


class FORMAT:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'
    NOCOLOR = '\x1b[0m'


class CLI:
    BUFSIZ = 1024
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    kill_receive_thread = False

    def __init__(self):
        try:
            host = input(FORMAT.GREEN + FORMAT.BOLD + 'Enter host ' + FORMAT.END + '(press enter for default): ')
            port = input(FORMAT.GREEN + FORMAT.BOLD + 'Enter port ' + FORMAT.END + '(press enter for default): ')
            if not port:
                port = 33000
            else:
                port = int(port)

            addr = (host, port)
        except ValueError:
            print(FORMAT.RED + "Please enter valid data in format or leave blank" + FORMAT.END)
            sys.exit()
        except KeyboardInterrupt:
            sys.exit()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(addr)
        except ConnectionRefusedError:
            print(FORMAT.RED + "Cannot connect to server!" + FORMAT.END)
            sys.exit()
        else:
            print(FORMAT.GREEN + "Connection established!" + FORMAT.END)

    def receive(self):
        while True:
            try:
                self.client_socket.settimeout(3.0)
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                if not msg:
                    break
                if msg.split(" ", 1)[0] == "#@!Hi":
                    tmp = msg.replace('#@!', '')
                    print(FORMAT.BOLD + tmp + FORMAT.END)
                elif msg.split(" ", 1)[0] == "!@#Enter":
                    tmp = msg.replace('!@#', '')
                    print(FORMAT.BOLD + tmp + FORMAT.END)
                elif msg == "!q":
                    print(FORMAT.RED + "Connection lost" + FORMAT.END)
                    exit_client()
                    break
                elif msg.split(" ", 1)[1] == "left the chat :c":
                    print(FORMAT.RED + msg + FORMAT.END)
                else:
                    tmp1 = msg.split(" ", 1)[0]
                    tmp2 = msg.split(" ", 1)[1]
                    print(FORMAT.BOLD + FORMAT.BLUE + tmp1, FORMAT.END + tmp2)
            except socket.timeout:
                if self.kill_receive_thread:
                    break
                else:
                    continue
            except socket.error:
                break
            # except Exception as inst:
            # print(FORMAT.RED + "An error occured:")
            # print(inst)
            # break

    def send(self, my_msg):
        msg = my_msg
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "!q":
            self.client_socket.close()


cl = CLI()


def exit_client():
    #  print(FORMAT.YELLOW + FORMAT.BOLD + "Exiting..." + FORMAT.END)
    animation = "|/-\\"
    i = 0
    while i != 7:
        print(FORMAT.YELLOW + FORMAT.BOLD + "Exiting..." + FORMAT.END + animation[i % len(animation)], end="\r"),
        i = i + 1
        time.sleep(0.2)
    print(FORMAT.RED + "You have left the chat" + FORMAT.END)
    cl.send("!q")
    cl.kill_receive_thread = True
    # cl.receive_thread.join()
    sys.exit(0)


def signal_handler(sig, frame):
    exit_client()


signal.signal(signal.SIGINT, signal_handler)
cl.receive_thread = threading.Thread(target=cl.receive)
cl.receive_thread.start()
while True:
    try:
        msg = input()
        if msg == "!q":
            exit_client()
        else:
            cl.send(msg)
    except Exception as inst:
        print(FORMAT.RED + "Unknown error occured" + FORMAT.END)
        break
