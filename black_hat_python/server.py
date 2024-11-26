import socket
import threading

bind_ip = "0.0.0.0"  # Escucha en todas las interfaces
bind_port = 9999      # Puerto de escucha

# Crear el socket TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket a la IP y puerto
server.bind((bind_ip, bind_port))

# Configurar el servidor para escuchar conexiones entrantes (máximo 5 conexiones en espera)
server.listen(5)
print(f"[*] Listening on {bind_ip}:{bind_port}")

# Esta es la función que manejará la conexión de cada cliente
def handle_client(client_socket):
    # Recibir datos del cliente
    request = client_socket.recv(1024)
    print(f"[*] Received: {request.decode('utf-8')}")  # Decodificar bytes a string (en UTF-8)
    
    # Enviar una respuesta al cliente
    client_socket.send(b"ACK!")  # Enviar ACK como bytes
    
    # Cerrar la conexión con el cliente
    client_socket.close()

# Bucle principal que acepta las conexiones entrantes
while True:
    # Aceptar una nueva conexión
    client, addr = server.accept()
    print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")
    
    # Crear y lanzar un hilo para manejar al cliente
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
