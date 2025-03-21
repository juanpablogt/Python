import socket

server_address = ("8.8.8.8", 53)
message = b"\x00"  # Mensaje vacío solo para probar

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(message, server_address)

response, address = client.recvfrom(1024)
print(f"Respuesta: {response} desde {address}")
