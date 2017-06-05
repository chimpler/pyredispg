import re


class RespReader(object):
    """
    Protocol description at: https://redis.io/topics/protocol
    """

    WORD_SPLIT = re.compile('"([^"]+)"|(\S+)')

    def __init__(self, fd):
        self._fd = fd

    def read_array(self):
        num_instructions = int(self._fd.readline())
        return [self.read() for _ in range(num_instructions)]

    def read_simple_string(self):
        return self._fd.readline().rstrip('\r\n')

    def read_error(self):
        return self._fd.readline().rstrip('\r\n')

    def read_integer(self):
        return int(self._fd.readline())

    def read_bulk_string(self):
        length = int(self._fd.readline())
        blob = self._fd.read(length)
        self._fd.readline()
        return blob

    def read_inline(self, first_char):
        return [a if a else b for a, b in re.findall(self.WORD_SPLIT, first_char + self._fd.readline().rstrip('\r\n'))]

    def read(self):
        resp_type = self._fd.read(1)
        if resp_type == '+':
            return self.read_simple_string()
        elif resp_type == '$':
            return self.read_bulk_string()
        elif resp_type == '-':
            return self.read_error()
        elif resp_type == ':':
            return self.read_integer()
        elif resp_type == '*':
            return self.read_array()
        else:
            return self.read_inline(resp_type)


class RedisReaderException(Exception):
    pass
