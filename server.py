import asyncio
import socket

clients = []


async def handle_data(reader, writer):

    data = await reader.read(1024)
    client_data = data.decode()

    # Client Data (id, message, username)
    client_data = client_data.split(",")

    client_id = client_data[0]
    message = client_data[1]
    username = client_data[2]

    if message == "RECEIVE":
        client = [writer, client_id, username]
        print(username+" has connected!")
        clients.append(client)

        for cl in clients:
            user = (cl[1]+",USER,"+cl[2]).encode()
            writer.write(user)

        data = "".encode()

    if data.decode() != "":
        print(username+': '+message)
        for client in clients:
            writer = client[0]
            writer.write(data)
            await writer.drain()


async def start_server():
    server = await asyncio.start_server(
        handle_data, '0.0.0.0', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print(f'IP: {ip}')

    async with server:
        await server.serve_forever()


asyncio.run(start_server())
