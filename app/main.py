import socket  # noqa: F401
import threading

def resp_parser(resp_bytes):
    # print(resp_bytes.split(b'\r\n'))
    command = []
    resp_bytes_split = resp_bytes.split(b'\r\n')
    length = len(resp_bytes_split)
    for i in range(2, length, 2):
        # print(resp_bytes.split(b'\r\n')[i])
        command.append(resp_bytes_split[i].decode())
    return command

def encode_bulk_string(s):
    return b"$" + str(len(s)).encode() + b"\r\n" + s.encode() + b"\r\n"

def handle_connection(connection):
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break

            parsed_data = resp_parser(data)
            # print(parsed_data)
            if parsed_data[0].upper() == "PING":
                connection.sendall(b"+PONG\r\n")
            elif parsed_data[0].upper() == "ECHO":
                connection.sendall(encode_bulk_string(" ".join([x for x in parsed_data[1:]])))
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
