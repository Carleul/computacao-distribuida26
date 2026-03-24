import asyncio
import struct

# armazenamento em memória
mensagens = {}

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Conectado: {addr}")

    try:
        while True:
            # 🔴 Lê exatamente 3 bytes (HEADER)
            header = await reader.readexactly(3)

            payload_size, operacao = struct.unpack("!HB", header)

            # 🔴 Lê o payload completo (se existir)
            payload = b''
            if payload_size > 0:
                payload = await reader.readexactly(payload_size)

            # 🔵 OPERAÇÃO: ENVIAR
            if operacao == 0x00:
                # formato simples: destinatario|mensagem
                if payload_size == 0:
                    print(f"[{addr}] Mensagem vazia ignorada")
                    continue
                texto = payload.decode('utf-8')
                if '|' not in texto:
                    print(f"[{addr}] Formato inválido recebido")
                    continue
                destinatario, msg = texto.split('|', 1)

                if destinatario not in mensagens:
                    mensagens[destinatario] = []

                mensagens[destinatario].append(msg)

                print(f"[{addr}] armazenou mensagem para {destinatario}")

            # 🔵 OPERAÇÃO: RECUPERAR
            elif operacao == 0x01:
                usuario = payload.decode('utf-8')

                msgs = mensagens.get(usuario, [])

                resposta = '\n'.join(msgs).encode('utf-8')

                if usuario in mensagens:
                    mensagens[usuario] = []

                header_resp = struct.pack("!HB", len(resposta), 0x01)
                writer.write(header_resp + resposta)
                await writer.drain()
                
                print(f"[{addr}] {usuario} recuperou mensagens")
                
            else:
                print(f"[{addr}] Operação desconhecida: {operacao}")

    except asyncio.IncompleteReadError:
        print(f"Cliente desconectou: {addr}")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        writer.close()
        await writer.wait_closed()


async def main():
    server = await asyncio.start_server(
        handle_client,
        '0.0.0.0',
        8888
    )

    addr = server.sockets[0].getsockname()
    print(f"Servidor rodando em {addr}")

    try:
        async with server:
            await server.serve_forever()
    except asyncio.CancelledError:
        print("Servidor sendo finalizado...")

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

try:
    loop.run_until_complete(main())
except KeyboardInterrupt:
    print("\nServidor encerrado manualmente.")
finally:
    loop.close()