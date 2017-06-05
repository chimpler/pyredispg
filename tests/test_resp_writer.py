import StringIO
from contextlib import closing, contextmanager

from pyredispg.resp_writer import RespWriter


class TestRespWriter(object):
    def test_format_simple_string(self):
        with closing(StringIO.StringIO()) as fd:
            RespWriter(fd).write_simple_string('test')
            assert '+test\r\n' == fd.getvalue()

    def test_writer_integer(self):
        with closing(StringIO.StringIO()) as fd:
            RespWriter(fd).write_integer(123)
            assert ':123\r\n' == fd.getvalue()

    def test_write_error(self):
        with closing(StringIO.StringIO()) as fd:
            RespWriter(fd).write_error('Invalid value')
            assert '-Invalid value\r\n' == fd.getvalue()

    def test_write_bulk_string(self):
        with closing(StringIO.StringIO()) as fd:
            RespWriter(fd).write_bulk_string('Hello Big String\nLine2')
            assert '$22\r\nHello Big String\nLine2\r\n' == fd.getvalue()

    def test_write_array(self):
        with closing(StringIO.StringIO()) as fd:
            RespWriter(fd).write_array([
                123,
                None,
                'Hello Big String\nLine2',
                321
            ])
            assert '*4\r\n:123\r\n$-1\r\n$22\r\nHello Big String\nLine2\r\n:321\r\n' == fd.getvalue()
