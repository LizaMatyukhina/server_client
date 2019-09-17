import socket


class Client:
    def __init__(self):
        with socket.create_connection(("127.0.0.1", 10001)) as sock:
            sock.settimeout(7)
            try:
                command = input('Please, input the number of a command (only INT): '
                                + '\n' + '1. Hour' + '\n'
                                + '2. Minutes' + '\n'
                                + '3. Seconds' + '\n'
                                + '4. STOP!' + '\n')
                while command != '4':
                    if command == '1':
                        sock.sendall("hour".encode("utf8"))
                    elif command == '2':
                        sock.sendall("minutes".encode("utf8"))
                    elif command == '3':
                        sock.sendall("seconds".encode("utf8"))

                    while True:
                        try:
                            data = sock.recv(1024)
                            print(data.decode("utf-8"))
                            if not data:
                                break

                        except socket.timeout:
                            break
                    command = input()

            except socket.timeout:
                print('send data timout')
            except socket.error as ex:
                print('send data error', ex)


if __name__ == "__main__":
    cl = Client()
