import StringIO
from contextlib import closing

from pyredispg.resp_reader import RespReader


class TestRespReader(object):

    @staticmethod
    def from_string(s):
        output = StringIO.StringIO()
        output.write(s)
        output.seek(0)
        return output

    def test_parse_simple_string(self):
        with closing(TestRespReader.from_string('test\r\n')) as fd:
            assert 'test' == RespReader(fd).read_simple_string()