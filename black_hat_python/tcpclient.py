import socket
import ssl

target_host = "www.google.com"
target_port = 443  # HTTPS

# Crear un socket TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))

# Usar SSLContext para envolver el socket
context = ssl.create_default_context()
secure_client = context.wrap_socket(client, server_hostname=target_host)

# Enviar una solicitud HTTPS
request = b"GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n"
secure_client.send(request)

# Recibir y mostrar la respuesta
response = secure_client.recv(4096)
print(response.decode())

# Cerrar la conexión
secure_client.close()
