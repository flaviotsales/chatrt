import threading
import socket
import ssl
import getpass

hostname = 'timechat.aptans.cloud'
hostname = 'localhost'

def main():
  context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
  context.load_verify_locations('certs/ca-cert.pem')
  # Cria um objeto de soquete para o cliente
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
      # Tenta se conectar ao servidor na porta 7777
      sclient = context.wrap_socket(client, server_hostname=hostname)

      sclient.connect((hostname, 7777))
      
  except Exception as e:
      print(e)
      # Se não conseguir se conectar, exibe uma mensagem e encerra o programa
      return print('\nNão foi possível se conectar ao servidor!\n')


  # Solicita ao usuário inserir um nome de usuário
  username = input('Usuário> ')
  senha = getpass.getpass('Senha> ')
  print('\nConectado')

  sclient.send(username.encode('utf-8'))
  sclient.send(senha.encode('utf-8'))


  # Cria duas threads para lidar com a recepção e envio de mensagens simultaneamente
  thread1 = threading.Thread(target=receiveMessages, args=[sclient])
  thread2 = threading.Thread(target=sendMessages, args=[sclient])


  # Inicia as threads
  thread1.start()
  thread2.start()


def receiveMessages(client):
  # Loop para receber mensagens do servidor
  while True:
      try:
          # Recebe uma mensagem codificada em UTF-8 e a decodifica
          msg = client.recv(2048).decode('utf-8')

          if msg == '':
             client.close()
             return
          
          # Exibe a mensagem recebida
          print(f'\b{msg}\n>', end='')
      except:
          # Se houver um erro ao receber mensagens, exibe uma mensagem e encerra a conexão
          print('\nNão foi possível permanecer conectado no servidor!')
          print('Pressione <Enter> Para continuar...')
          client.close()
          break


def sendMessages(client):
  # Loop para enviar mensagens para o servidor
  while True:
      try:
          # Solicita ao usuário inserir uma mensagem
          msg = input('>')

          # Envia a mensagem formatada com o nome de usuário ao servidor
          client.send(f'{msg}'.encode('utf-8'))
      except:
          # Se houver um erro ao enviar mensagens, encerra a thread
          return


# Chama a função main para iniciar o cliente
main()