import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

# 检查11434端口是否被占用
if is_port_in_use(7982):
    print("端口11434已被占用")
else:
    print("端口11434未被占用")