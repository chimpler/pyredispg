class RespWriter(object):
    def __init__(self, fd):
        self._fd = fd

    def write_simple_string(self, s):
        self._fd.write('+{s}\r\n'.format(s=s))

    def write_error(self, error):
        self._fd.write('-{s}\r\n'.format(s=error))

    def write_integer(self, i):
        self._fd.write(':{i}\r\n'.format(i=i))

    def write_bulk_string(self, s):
        self._fd.write('${length}\r\n{s}\r\n'.format(length=len(s), s=s))

    def write_null(self):
        self._fd.write('$-1\r\n')

    def write_array(self, array):
        self._fd.write('*{num_resp}\r\n'.format(num_resp=len(array)))
        for e in array:
            self.write(e)

    def write(self, e):
        if e is None:
            self.write_null()
        elif isinstance(e, int):
            self.write_integer(e)
        elif isinstance(e, list):
            self.write_array(e)
        elif e[0] == '-' and '\n' not in e:
            self.write_error(e[1:])
        elif e[0] == '+' and '\n' not in e:
            self.write_simple_string(e[1:])
        else:
            self.write_bulk_string(e)
