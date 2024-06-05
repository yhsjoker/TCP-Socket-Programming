import socket
import threading

import config
import utils


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((config.DEFAULT_IP, config.DEFAULT_PORT))
    server_socket.listen(5)

    while True:
        sock, addr = server_socket.accept()
        threading.Thread(target=tcp_link, args=(sock, addr)).start()


def tcp_link(sock, addr):
    print('Connected by', addr)

    pkg = utils.unpack_msg(sock.recv(1024).decode('utf-8'))
    if pkg is None or len(pkg) == 0 or pkg[0] != 1:
        sock.close()
        return

    n = pkg[1]
    sock.send(utils.pack_agree().encode('utf-8'))

    for i in range(n):
        pkg = utils.unpack_msg(sock.recv(1024).decode('utf-8'))
        if pkg is None or len(pkg) == 0 or pkg[0] != 3:
            sock.close()
            return
        sock.send(utils.pack_response(pkg[1][::-1]).encode('utf-8'))


if __name__ == '__main__':
    main()
