import socket
import datetime
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process


class Server:
    def __init__(self, m, num):
        self.m = m
        self.n = num
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("127.0.0.1", 10001))
        self.sock.listen(socket.SOMAXCONN)

    def process(self):
        all_processes = []
        for i in range(self.n):
            proc = Process(target=self.prom, args=())
            all_processes.append(proc)
            proc.start()

        for i in range(self.n):
            all_processes[i].join()

    def prom(self):
        conn, addr = self.sock.accept()
        self.threads(conn)

    def threads(self, conn):
        with ThreadPoolExecutor(max_workers=self.m) as pool:
            results = [pool.submit(self.client(conn))]

    def client(self, conn):
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


if __name__ == "__main__":
    m = int(input('Please input number of Threadings: '))
    n = int(input('Please input number of Processes: '))
    serv = Server(m, n)
    serv.process()
