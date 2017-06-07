from gevent import socket
from gevent.server import StreamServer
from pyhocon import ConfigFactory

from pyredispg.exceptions import RedisWrongTypeException, RedisException
from pyredispg.postgres_dao import PostgresDao
from pyredispg.redis_info import RedisInfo
from pyredispg.redis_wrapper import RedisWrapper
from pyredispg.resp_reader import RespReader
from pyredispg.resp_writer import RespWriter


class Server(object):
    def __init__(self):
        self._server = StreamServer(('', 1234), self.handle_client)
        self._config = ConfigFactory.parse_file('config.hocon')
        self._dao = PostgresDao(self._config['postgres'])
        self._redis_info = RedisInfo()

    def handle_client(self, sock, address):
        ClientConnection(sock, self._config, self._dao, self._redis_info).run()

    def run(self):
        self._server.serve_forever()


class ClientConnection(object):
    COMMAND_MAPPING = {
        'del': 'delete'
    }

    def __init__(self, sock, config, dao, redis_info):
        self._config = config
        self._dao = dao
        self._sock = sock
        self._fp = sock.makefile()
        self._resp_reader = RespReader(self._fp)
        self._resp_writer = RespWriter(self._fp)
        self._redis = RedisWrapper(self._dao, redis_info)

    def _parse_command(self, instructions):
        command = self.COMMAND_MAPPING.get(instructions[0], instructions[0])
        method = getattr(self._redis, command.lower(), None)
        if method is None:
            return "-ERR unknown command '%s'" % command
        try:
            return method(*instructions[1:])
        except RedisWrongTypeException as e:
            return '-WRONGTYPE ' + e.message
        except RedisException as e:
            return '-ERR ' + e.message
        except TypeError:
            return "-ERR wrong number of arguments for '%s' command" % command

    def __del__(self):
        self._sock.shutdown(socket.SHUT_WR)
        self._sock.close()

    def run(self):
        while True:
            instructions = self._resp_reader.read()
            if not instructions or instructions[0].lower() == 'quit':
                break

            result = self._parse_command(instructions)
            self._resp_writer.write(result)
            self._fp.flush()

if __name__ == '__main__':
    Server().run()
