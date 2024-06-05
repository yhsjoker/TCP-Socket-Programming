# TCP Socket Programming

这个项目展示了如何通过TCP协议实现客户端和服务器间的文本反转通信。客户端从指定文件读取内容，按照配置的最小和最大长度随机分块后发送到服务器，服务器将接收到的文本块反转后返回给客户端。

## 项目文件结构

- `config.py`：定义了网络配置和协议相关的常量。
- `reverse_tcp_client.py`：实现了TCP客户端的逻辑。
- `reverse_tcp_server.py`：实现了TCP服务器的逻辑，支持多线程处理客户端请求。
- `utils.py`：包含了消息打包和解包的工具函数，用于客户端和服务器间的报文处理。

## 运行环境

- Python 3.12
- 无需额外安装库，使用Python标准库即可。

## 安装步骤

1. 克隆仓库：

   ```bash
   git clone git@github.com:yhsjoker/TCP-Socket-Programming.git
   cd TCP-Socket-Programming
   ```

## 运行应用程序

1. 启动UDP服务器：

   ```bash
   python reverse_tcp_server.py
   ```

2. 运行UDP客户端：

   ```bash
   python reverse_tcp_client.py -i <server_ip> -p <server_port> -if <input_file> -of <output_file> -l <min_length> -r <max_length>
   ```

可以使用 `python reverse_tcp_client.py --help` 查看具体参数。