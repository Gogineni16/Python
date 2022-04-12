"""Server Runner and Worker"""
from asyncio import run, start_server
from pathlib import Path

from user import User


async def servercb(reader, writer):
    """Server Callback
    Decides What to do, when to do"""
    user = None

    while True:
        command = await reader.read(1000)
        command = command.decode()

        if command == 'quit':
            break

        args = command.split()
        tmp_user = user
        result = 'Invalid Command'

        if args[0] in ['login', 'register']:
            if len(args) != 3:
                result = 'Invalid Syntax for command'
            else:
                tmp_user = User(args[1], args[2])
                result = tmp_user.login(
                ) if args[0] == 'login' else tmp_user.register()
                if tmp_user.valid:
                    user = tmp_user

        elif args[0] == 'commands':
            result = (Path(__file__).parent / 'help.txt').read_text()

        elif not user:
            result = 'Login to Continue'

        elif args[0] == 'list':
            result = user.ls()

        elif args[0] == 'change_folder':
            if len(args) != 2:
                result = 'Invalid Syntax for command'
            else:
                result = user.cd(args[1])

        elif args[0] == 'read_file':
            if len(args) != 2:
                result = 'Invalid Syntax for command'
            else:
                result = user.cat(args[1])

        elif args[0] == 'write_file':
            if len(args) < 3:
                result = 'Invalid Syntax for command'
            else:
                result = user.file_append(args[1], ' '.join(args[2:]))

        elif args[0] == 'create_folder':
            if len(args) != 2:
                result = 'Invalid Syntax for command'
            else:
                result = user.mkdir(args[1])

        writer.write(result.encode())

    writer.close()


async def server():
    """Server Starter"""
    servr = await start_server(servercb, '127.0.0.1', '8088')
    async with servr:
        await servr.serve_forever()

run(server())
