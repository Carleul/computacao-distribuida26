import socket
import struct

def enviar(destinatario, mensagem):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 8888))

    # formato: destinatario|mensagem
    texto = f"{destinatario}|{mensagem}".encode('utf-8')

    # header: tamanho + operação 0x00 (ENVIAR)
    header = struct.pack("!HB", len(texto), 0x00)

    s.sendall(header + texto)
    s.close()


# entrada do usuário
destinatario = input("Destinatário: ")
mensagem = input("Mensagem: ")

enviar(destinatario, mensagem)