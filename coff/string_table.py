class StringTable:
    """
    Layout:
    +-----------------+
    |  Size of table  |
    +-----------------+
    |     Strings     |
    +-----------------+
    Size is in bytes and contains the 4 bytes required to write it.
    """
    def __init__(self):
        self._strings = []

    @staticmethod
    def _check(value):
        if not isinstance(value, bytes):
            raise ValueError('value must be an encoded string')

    def __len__(self):
        return len(self._strings)

    def __getitem__(self, item):
        return self._strings[item]

    def __setitem__(self, key, value):
        self._check(value)
        self._strings[key] = value

    def __contains__(self, item):
        return item in self._strings

    def __iter__(self):
        return iter(self._strings)

    def append(self, item):
        self._check(item)
        self._strings.append(item)

    def pack(self):
        sizeof_strtab_size = 4
        total_size_in_bytes = sizeof_strtab_size + sum(len(s) + 1 for s in self._strings)
        buffer = bytearray()
        buffer += total_size_in_bytes.to_bytes(sizeof_strtab_size, 'little', signed=False)
        for s in self._strings:
            buffer += s + b'\0'
        return bytes(buffer)
