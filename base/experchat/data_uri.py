import re
from binascii import Error, a2b_base64

MIMETYPE_REGEX = r'[\w]+\/[\w\-\+\.]+'
_MIMETYPE_RE = re.compile('^{}$'.format(MIMETYPE_REGEX))

CHARSET_REGEX = r'[\w\-\+\.]+'
_CHARSET_RE = re.compile('^{}$'.format(CHARSET_REGEX))

DATA_URI_REGEX = (
    r'data:' +
    r'(?P<mimetype>{})?'.format(MIMETYPE_REGEX) +
    r'(?:\;charset\=(?P<charset>{}))?'.format(CHARSET_REGEX) +
    r'(?P<base64>\;base64)?' +
    r',(?P<data>.*)')
_DATA_URI_RE = re.compile(r'^{}$'.format(DATA_URI_REGEX), re.DOTALL)


class DataURI(str):

    def __new__(cls, *args, **kwargs):
        uri = super(DataURI, cls).__new__(cls, *args, **kwargs)
        uri._parse  # Trigger any ValueErrors on instantiation.
        return uri

    def __repr__(self):
        return 'DataURI(%s)' % (super(DataURI, self).__repr__(),)

    @property
    def mimetype(self):
        return self._parse[0]

    @property
    def charset(self):
        return self._parse[1]

    @property
    def is_base64(self):
        return self._parse[2]

    @property
    def data(self):
        return self._parse[3]

    @property
    def _parse(self):
        match = _DATA_URI_RE.match(self)
        if not match:
            raise ValueError("Not a valid data URI: %r" % self)
        mimetype = match.group('mimetype') or None
        charset = match.group('charset') or None

        if match.group('data'):
            try:
                data = a2b_base64(match.group('data'))
            except Error:
                data = None
        else:
            data = None

        return mimetype, charset, bool(match.group('base64')), data
