import random
import socket
import time
import config
import argparse
import utils


def main():
    args = get_args()
    contents = split_file_content(get_file_content(args.infile), args.Lmin, args.Lmax)

    server_address = args.ip, args.port
    client_socket = get_client_socket()
    client_socket.connect(server_address)

    client_socket.send(utils.pack_init(len(contents)).encode('UTF-8'))
    pkg = utils.unpack_msg(client_socket.recv(1024).decode('UTF-8'))
    if pkg[0] != 2:
        print('Invalid packet received')
        return

    rev_contents = []
    for seq_no, content in zip(range(1, len(contents) + 1), contents):
        print("第{}块：{}".format(seq_no, content))
        client_socket.send(utils.pack_request(content).encode('UTF-8'))
        pkg = utils.unpack_msg(client_socket.recv(1024).decode('UTF-8'))
        if pkg[0] != 4:
            print('Invalid packet received')
            return
        print("翻转后的第{}块：{}".format(seq_no, pkg[1]))
        rev_contents.append(pkg[1])

    save_file_content(args.outfile, rev_contents)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', default=config.DEFAULT_IP, type=str, help='IP address (default: 127.0.0.1)')
    parser.add_argument('-p', '--port', default=config.DEFAULT_PORT, type=int, help='port number (default: 12345)')
    parser.add_argument('-if', '--infile', default='test_in.txt', type=str, help='file to send')
    parser.add_argument('-of', '--outfile', default="test_out.txt", type=str, help='file to save')
    parser.add_argument('-l', '--Lmin', default=10, type=int, help='reverseRequest Lmin')
    parser.add_argument('-r', '--Lmax', default=20, type=int, help='reverseRequest Lmax')
    args = parser.parse_args()
    return args


def get_file_content(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        return content


def split_file_content(content, Lmin, Lmax):
    lines = []
    while len(content) > 0:
        sub_length = min(len(content), random.randint(Lmin, Lmax))
        lines.append(content[:sub_length])
        content = content[sub_length:]
    return lines


def get_client_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s


def save_file_content(file_path, contents):
    with open(file_path, 'w') as f:
        for content in reversed(contents):
            f.write(content)


if __name__ == "__main__":
    main()
