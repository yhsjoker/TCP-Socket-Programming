import random
import socket
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
    if pkg is None or len(pkg) == 0 or pkg[0] != 2:
        print('Invalid packet received')
        return

    rev_contents = []
    for seq_no, content in zip(range(1, len(contents) + 1), contents):
        print("第{}块：{}".format(seq_no, content))
        client_socket.send(utils.pack_request(content).encode('UTF-8'))
        pkg = utils.unpack_msg(client_socket.recv(1024).decode('UTF-8'))
        if pkg is None or len(pkg) == 0 or pkg[0] != 4:
            print('Invalid packet received')
            return
        print("翻转后的第{}块：{}".format(seq_no, pkg[1]))
        rev_contents.append(pkg[1])

    save_file_content(args.outfile, rev_contents)


def get_args():
    """
    解析命令行参数。

    Returns:
        argparse.Namespace: 包含所有命令行参数值的命名空间对象。
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', default=config.DEFAULT_IP, type=str, help='IP address (default: 127.0.0.1)')
    parser.add_argument('-p', '--port', default=config.DEFAULT_PORT, type=int, help='port number (default: 12345)')
    parser.add_argument('-if', '--infile', default='test_in.txt', type=str, help='file to send (default: test_in.txt)')
    parser.add_argument('-of', '--outfile', default="test_out.txt", type=str, help='file to save (default: test_out.txt)')
    parser.add_argument('-l', '--Lmin', default=10, type=int, help='reverseRequest Lmin (default: 10)')
    parser.add_argument('-r', '--Lmax', default=20, type=int, help='reverseRequest Lmax (default: 20)')
    args = parser.parse_args()
    return args


def get_file_content(file_path):
    """
    从指定路径读取并返回文件的全部内容。

    Args:
        file_path (str): 要读取的文件的路径。

    Returns:
        str: 文件的内容。
    """
    with open(file_path, 'r') as f:
        content = f.read()
        return content


def split_file_content(content, Lmin, Lmax):
    """
    将给定内容分割成随机长度的子字符串列表。

    Args:
        content (str): 要分割的原始字符串内容。
        Lmin (int): 分割块的最小长度。
        Lmax (int): 分割块的最大长度。

    Returns:
        list: 分割后的字符串列表。
    """
    lines = []
    while len(content) > 0:
        sub_length = min(len(content), random.randint(Lmin, Lmax))
        lines.append(content[:sub_length])
        content = content[sub_length:]
    return lines


def get_client_socket():
    """
    创建并返回一个新的TCP客户端socket。

    Returns:
        socket.socket: 新创建的客户端socket。
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s


def save_file_content(file_path, contents):
    """
    将给定内容列表逆序保存到指定的文件路径。

    Args:
        file_path (str): 要保存内容的文件路径。
        contents (list): 需要保存的内容列表。

    """
    with open(file_path, 'w') as f:
        for content in reversed(contents):
            f.write(content)


if __name__ == "__main__":
    main()
