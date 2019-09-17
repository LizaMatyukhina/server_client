import socket
import datetime
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process


class Server(Process):
    def __init__(self, m, n):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.m = m
        self.n = n

    def connection(self):
        self.sock.bind(("127.0.0.1", 10001))
        self.sock.listen(socket.SOMAXCONN)
        conn, addr = self.sock.accept()
        conn.settimeout(8)
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                data = data.decode('utf8')
                now = datetime.datetime.now()
                hour = now.hour
                minutes = now.minute
                seconds = now.second

                if data == 'hour':
                    conn.sendall(str(hour).encode('utf8'))
                elif data == 'minutes':
                    conn.sendall(str(minutes).encode('utf8'))
                elif data == 'seconds':
                    conn.sendall(str(seconds).encode('utf8'))
                elif data == 'stop':
                    conn.close()
                    self.sock.close()

            except socket.timeout:
                break

    def run(self):
        with ThreadPoolExecutor(max_workers=self.m) as pool:
            results = [pool.submit(self.connection())]


if __name__ == "__main__":
    n = int(input('Please input number of Processes: '))
    m = int(input('Please input number of Threadings: '))
    serv = Server(m, n)
    serv.start()
    serv.join()
