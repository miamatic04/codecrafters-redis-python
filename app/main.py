import socket  # noqa: F401
import threading

def handle_connection(connection):
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            connection.sendall(b"+PONG\r\n")
    except (ConnectionResetError, BrokenPipeError):
        pass
    finally:
        connection.close()

def main():
    print("Logs from your program will appear here!")
    
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        connection, address = server_socket.accept() 

        threading.Thread(target=handle_connection, args=(connection,)).start()

if __name__ == "__main__":
    main()
