import json
import os

import sys
import time

from pyredispg.exceptions import RedisException
from pyredispg.postgres_dao import KeyValue


class RedisWrapper(object):
    COMMAND_FILE = 'command.json'

    def __init__(self, dao, redis_info):
        with open(os.path.join(sys.path[0], self.COMMAND_FILE)) as fd:
            self._command = json.loads(fd.read())
        self._redis_info = redis_info
        self._dao = dao
        self._db = 0

    def command(self):
        return self._command

    def delete(self, key):
        return self._dao.delete(self._db, key)

    def echo(self, value):
        return value

    def exists(self, key):
        return 1 if self._dao.exists(self._db, key) else 0

    def flushall(self):
        self._dao.delete_all_dbs()
        return '+OK'

    def flushdb(self):
        self._dao.delete_db(self._db)
        return '+OK'

    def get(self, key):
        return self._dao.get(self._db, key)

    def type(self, key):
        t = self._dao.type_str(self._db, key)
        return '+' + (t if t else 'none')

    def keys(self, pattern):
        return self._dao.get_keys(self._db, pattern)

    def dbsize(self):
        return self._dao.dbsize()

    def select(self, db):
        def check_db():
            try:
                n = int(db)
                if 0 <= n and n <= 15:
                    return n
                else:
                    return None
            except ValueError:
                return None

        n = check_db(db)
        if n is None:
            raise RedisException('invalid DB index')
        else:
            self._db = n
            return '+OK'

    def hexists(self, key, hkey):
        # convert boolean to 0 or 1
        return int(self._dao.hexists(self._db, key, hkey))

    def hdel(self, key, hkey):
        # convert boolean to 0 or 1
        return int(self._dao.hdel(self._db, key, hkey))

    def hget(self, key, hkey):
        return self._dao.hget(self._db, key, hkey)

    def hmget(self, key, *hkeys):
        return self._dao.hmget(self._db, key, hkeys)

    def hset(self, key, hkey, value):
        return self._dao.hset(self._db, key, hkey, value)

    def hmset(self, key, *hkey_values):
        key_vals = [KeyValue(hkey_values[i * 2], hkey_values[i * 2 + 1]) for i in range(len(hkey_values) / 2)]
        return self._dao.hmset(self._db, key, key_vals)

    def hlen(self, key, hkey):
        return self._dao.hlen(self._db, key, hkey)

    def hgetall(self, key):
        return [e for kv in self._dao.hgetall(self._db, key) for e in kv]

    def hkeys(self, key):
        return self._dao.hkeys(self._db, key)

    def hvals(self, key):
        return self._dao.hvals(self._db, key)

    def hlen(self, key):
        return self._dao.hlen(self._db, key)

    def info(self):
        return '\n\n'.join([
            '# {title}\n{section}'.format(
                title=title,
                section='\n'.join(
                   '{k}:{v}'.format(k=k, v=v) for k, v in kvdict.items()
                )
            ) for title, kvdict in self._redis_info.get_info().items()
        ]) + '\n'

    def ping(self, value='PONG'):
        return value

    def sadd(self, key, *values):
        return self._dao.sadd(self._db, key, values)

    def set(self, key, value, ex=None, mx=None, overwrite=True):
        self._dao.set(self._db, key, value, ex, mx, overwrite)
        return '+OK'

    def scard(self, key):
        return self._dao.scard(self._db, key)

    def smembers(self, key):
        return self._dao.smembers(self._db, key)

    def time(self):
        t = time.time()
        seconds = int(t)
        millis = int((t - seconds) * 1000000)
        return [
            str(seconds),
            str(millis)
        ]
