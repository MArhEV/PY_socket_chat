# PY_socket_chat
text communicator on sockets written in Python3
The project is written in Python 3 and it is used for text communication between two or more (up to 5
with the possibility of extending or shrinking through changing one constant in code). Program uses a
functionality of network sockets. It is possible to set a session on a loopback address on one PC or
between a few users in one network.

Najpierw należy uruchomić serwer. Po wyświetleniu przez niego komunikatu o czekaniu na połączenie
należy uruchomić klienta. Jako że program służy do wymiany wiadomości na drodze klient-klient a nie
jedynie klient-serwer, należy uruchomić co najmniej dwa procesy klienta aby zaobserwować działanie
programu. W oknie klienta w przypadku uruchomienia na jednym PC należy dwa pierwsze komunikaty
&quot;przeklikać&quot;. W innym wypadku należy podać adres serwera w formacie IPv4 i ustalony (byle służący do
komunikacji TCP). następnie należy wpisać swoją nazwę użytkownika. Na tym etapie możliwa jest
wymiana wiadomości z innymi użytkownikami.
Aby wysłać wiadomość prywatną należy użyć w wiadomości znacznika w formacie @username (np.
jeżeli chcemy wysłac wiadomość o treści &quot;cześć!&quot; do Alka, wpisujemy &quot;@Alek cześć!&quot;.
Aby wyjść należy wpisać wiadomość o treści &quot;!q&quot;.
Otworzenie pliku z zapisem konwersacji jest możliwe dopiero po odłączeniu wszystkich klientów i
zamknięciu serwera.
