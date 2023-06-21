
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = '0.0.0.0'
server_port = 8808

server_socket.bind((server_host, server_port))
server_socket.listen(5)  # Maximum number of queued connections

print('Server listening on {}:{}'.format(server_host, server_port))

# --- Server waiting for connection ---
while True:
    client_socket, client_address = server_socket.accept()

    print('New connection from {}:{}'.format(client_address[0], client_address[1]))

    new_thread = ClientConn(client_socket, client_address)
    new_thread.start()
