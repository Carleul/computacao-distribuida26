import socket
import struct

def recuperar(usuario):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 8888))

    payload = usuario.encode('utf-8')

    # header: tamanho + operação 0x01 (RECUPERAR)
    header = struct.pack("!HB", len(payload), 0x01)

    s.sendall(header + payload)

    # 🔴 ler header da resposta
    header_resp = s.recv(3)
    size, op = struct.unpack("!HB", header_resp)

    # 🔴 ler payload completo
    data = b''
    while len(data) < size:
        data += s.recv(1024)

    print("\nMensagens recebidas:")
    print(data.decode('utf-8'))

    s.close()


# entrada do usuário
usuario = input("Seu nome: ")

recuperar(usuario)