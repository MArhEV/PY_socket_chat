import socket  # funkcje gniazd sieciowych
import threading  # wątki
import datetime  # czas do zapisu w logach rozmów
import signal
import sys
import time


class FORMAT:  # formatowanie tekstu
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    IDK = '\033[90m'
    BOLD = '\033[1m'
    END = '\033[0m'
    NOCOLOR = '\x1b[0m'


class SRV:  # klasa serwera z definicjami metod uzywanych przez serwer
    clients = {}  # slownik klientów
    addresses = {}  # słownik adresów
    threads = []
    kill_threads = False
    HOST = ''
    PORT = 33000
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # stworzenie gniazda IPv4 z protokołem TCP
    SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # ustawienie opcji gniazda
    print(FORMAT.GREEN, "Socket created!", FORMAT.END)

    def __init__(self):  # konstruktor do bindowania gniazda
        self.SERVER.bind(self.ADDR)
        print(FORMAT.GREEN, "Socket bounded!", FORMAT.END)

    def __del__(self):
        self.SERVER.close()  # zamykanie serwera
        for client in self.clients:  # kończenie połączenia z klientami

            client.close()

    def get_clients(self):  # metoda zwracająca klientów
        return self.clients

    def add_client(self, client, name):  # metoda przypisująca klientom nazwy
        self.clients[client] = name

    def accept_conn(self):  # akceptowanie nowych połączeń
        while True:
            client, client_address = self.SERVER.accept()
            # print(FORMAT.IDK, "%s:%s joined!" % client_address, FORMAT.END)
            print(FORMAT.IDK, "'{}' joined!".format(client_address), FORMAT.END)  # rozwiazanie błędu Too few arguments
            # for format string
            client.send(bytes("!@#Enter your username: ", "utf8"))
            self.addresses[client] = client_address  # przypisanie do klienta jego adresu IP
            # threading.Thread(target=self.handle_client, args=(client,)).start()  # wystartowanie wątku wywołującego
            t = threading.Thread(target=self.handle_client, args=(client, lambda: self.kill_threads))
            self.threads.append(t)
            t.start()
            # metodę handle_client i przekazującego mu argument client

    def handle_client(self, client, stop):  # obsluga calego polaczenia z klientem
        # poniższy fragment wykonuje się tylko raz po dolączeniu klienta do serwera
        name = client.recv(self.BUFSIZ).decode("utf8")  # wpisanie swojej nazwy przez użytkownika
        welcome = '#@!Hi %s! Type !q to quit.' % name
        client.send(bytes(welcome, "utf8"))
        msg = "%s joined the chat!" % name
        f.write("%s joined the chat\n" % name)  # zapisanie do txt dołączenia klienta
        print(FORMAT.BLUE, "%s joined the chat" % name, FORMAT.END)
        self.broadcast(bytes(msg, "utf8"))
        self.clients[client] = name

        while True:
            try:
                # wykonywanie ciągle w pętli
                client.settimeout(3.0)
                msg = client.recv(self.BUFSIZ)  # odebranie wiadomości
                if not msg:
                    break
                if msg.decode("utf8")[0] == '@':  # jezeli po zdekodowaniu pierwszym znakiem jest @ to wiadomość priv
                    self.send_to_user(msg, name + ": ")
                elif msg != bytes("!q", "utf8"):
                    self.broadcast(msg, name + ": ", client)
                else:
                    # pozostaly warunek to !q czyli wyjście klienta z serwera
                    self.broadcast(bytes("%s left the chat :c" % name, "utf8"))
                    client.close()
                    print(FORMAT.BLUE, "%s left the chat" % name, FORMAT.END)
                    f.write("%s left the chat\n" % name)
                    del self.clients[client]  # kasowanie klienta ze słownika
                    break
            except socket.timeout:
                if stop():
                    break
                else:
                    continue
            except Exception as inst:
                print(FORMAT.IDK + "Connection with client lost" + FORMAT.END)
                del self.clients[client]

    def broadcast(self, msg, prefix="", poster=None):  # prefix = nazwa + :
        for sock in self.clients:
            if sock != poster:  # dla wszystkich gniazd
                sock.send(bytes(prefix, "utf8") + msg)
                tmp1 = msg.decode("utf8")
                txt = (prefix.split(':', 1)[0] + " to all: " + tmp1 + "\n")
                if txt.split(":", 2)[0] != "to all":  # żeby nie wypisywało wiadomości n razy (n liczba klientów)
                    print(" " + prefix.split(':', 1)[0] + " to all: " + tmp1)
                    f.write(txt)

    def send_to_user(self, msg, prefix=""):  # wiadomość prywatna
        tmp = msg.decode().split(" ", 1)[0]  # dzieli wiadomość po spacjach i przypisuje do tmp @nazwa
        tmp = tmp.replace('@', '')  # zastępuje @ niczym
        for client in self.clients:
            if self.clients[client] == tmp:  # szuka klienta o uzytej nazwie
                client.send(bytes(prefix, "utf8") + msg)
                tmp1 = msg.decode("utf8")
                print(" " + prefix.split(':', 1)[0] + " to " + tmp + ": " + tmp1)
                txt = (prefix.split(':', 1)[0] + " to " + tmp + ": " + tmp1 + "\n")
                f.write(txt)

    def exit(self):
        self.kill_threads = True  # ubijanie wątków
        self.broadcast(bytes("!q", "utf-8"))
        for t in self.threads:
            t.join()  # dołączanie wątków pobocznych do głównego


srv = SRV()


def signal_handler(sig, frame):
    animation = "|/-\\"
    i = 0
    while i != 7:
        print(FORMAT.YELLOW + FORMAT.BOLD + "Exiting... " + FORMAT.END + animation[i % len(animation)], end="\r"),
        i = i + 1
        time.sleep(0.2)
    global srv  # definicja zmiennej globalnej srv
    srv.exit()
    del srv  # zamykanie serwera
    sys.exit(0)


if __name__ == "__main__":  # definicja zmiennych interpretera python (plik źródłowy jako program glówny)
    signal.signal(signal.SIGINT, signal_handler)
    srv.SERVER.listen(5)  # podłączenie maksymalnie 5 użytkowników do serwera
    f = open("chat_log.txt", "w")  # utworzenie txt z prawem zapisu do pliku
    now = datetime.datetime.now()  # ustawienie czasu na chwilę obecną
    f.write(now.strftime("%Y-%m-%d %H:%M:%S\n"))
    print(FORMAT.YELLOW, "Waiting for connection...", FORMAT.END)
    srv.accept_conn()
    # ACCEPT_THREAD = threading.Thread(target=srv.accept_conn())  # akceptacja i wystartowanie wątku z accept_conn
    # ACCEPT_THREAD.start()
    while input == "!quit":
        f.close()  # zamknięcie pliku
        del srv
