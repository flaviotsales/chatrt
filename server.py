import threading
import socket
import ssl

usuarios = {
    'flavio': 'secret123',
    'fontes': 'secret456'
}

# Lista de clientes conectados ao servidor
clients = []

# Função para lidar com as mensagens de um cliente
def handle_client(client):
    username = bytes.decode(client.recv(2048))
    senha = bytes.decode(client.recv(2048))

    senha_correta = username in usuarios and usuarios[username] == senha
    if not senha_correta:
        client.send('Usuário ou senha incorreta'.encode('utf-8'))
        client.shutdown(socket.SHUT_RDWR)
        client.close()
        remove_client(client)
        return

    while True:
        try:
            msg = client.recv(2048)
            if msg != '':
                broadcast(f'<{username}>: {msg}'.encode('utf-8'), client)
        except:
            remove_client(client)
            break

# Função para transmitir mensagens para todos os clientes
def broadcast(msg, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(msg)
            except:
                remove_client(client)

# Função para remover um cliente da lista
def remove_client(client):
    clients.remove(client)

# Função principal
def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('certs/ca-cert.pem', 'certs/ca-key.pem')
    context.verify_mode = ssl.CERT_NONE

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

        print("Iniciou o servidor de bate-papo")

        try:
            server.bind(("0.0.0.0", 7777))  # Aceitar conexões de qualquer endereço
            server.listen()

            with context.wrap_socket(server, server_side=True) as sserver:
                while True:
                    try:
                        client, addr = sserver.accept()
                        clients.append(client)
                        print(f'Cliente conectado com sucesso. IP: {addr}')

                        # Inicia uma nova thread para lidar com as mensagens do cliente
                        thread = threading.Thread(target=handle_client, args=(client,))
                        thread.start()
                    except Exception as e:
                        print(f'Erro ao aceitar conexão: {e}')       

        except Exception as e:
            return print(f'\nNão foi possível iniciar o servidor! Erro: {e}\n')

# Executa o programa
if __name__ == "__main__":
    main()