"""Client Runner and Worker"""
import asyncio


async def clientcb(reader, writer):
    """Client Callback"""
    print('Login / Register to continue.\nYou Can use commands to get help')
    while True:
        cmd = input('Command: ')
        writer.write(cmd.encode())

        if cmd == 'quit':
            break

        result = await reader.read(1000)
        result = result.decode()

        print(result)

    writer.close()


async def client():
    """Client Connection Establisher"""
    reader, writer = await asyncio.open_connection('127.0.0.1', '8088')
    await clientcb(reader, writer)

asyncio.run(client())
