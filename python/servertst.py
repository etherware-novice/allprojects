
import asyncio, socket

async def handle_client(reader, writer):
    request = None
    writer.write(b"You are connected\r\n")
    while (request := (await reader.readline()).decode(errors='ignore')[:-1]) != 'quit':
        print(request)

        
        writer.write(request.encode())
        await writer.drain()
    writer.close()

async def run_server():
    server = await asyncio.start_server(handle_client, '', 23)
    async with server:
        await server.serve_forever()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

print(socket.gethostbyname(socket.gethostname()))
print(get_ip())


asyncio.run(run_server())