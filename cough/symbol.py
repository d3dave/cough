import enum
import struct


class SpecialSectionNumber(enum.IntEnum):
    UNDEFINED = 0
    ABSOLUTE = -1
    DEBUG = -2


class StorageClass(enum.IntEnum):
    END_OF_FUNCTION = -1
    NULL = 0
    AUTOMATIC = 1
    EXTERNAL = 2
    STATIC = 3
    REGISTER = 4
    EXTERNAL_DEF = 5
    LABEL = 6
    UNDEFINED_LABEL = 7
    MEMBER_OF_STRUCT = 8
    ARGUMENT = 9
    STRUCT_TAG = 10
    MEMBER_OF_UNION = 11
    UNION_TAG = 12
    TYPE_DEFINITION = 13
    UNDEFINED_STATIC = 14
    ENUM_TAG = 15
    MEMBER_OF_ENUM = 16
    REGISTER_PARAM = 17
    BIT_FIELD = 18
    BLOCK = 100
    FUNCTION = 101
    END_OF_STRUCT = 102
    FILE = 103
    SECTION = 104.
    WEAK_EXTERNAL = 105
    CLR_TOKEN = 107


class BaseType(enum.IntEnum):
    NULL = 0
    VOID = 1
    CHAR = 2
    SHORT = 3
    INT = 4
    LONG = 5
    FLOAT = 6
    DOUBLE = 7
    STRUCT = 8
    UNION = 9
    ENUM = 10
    MOE = 11
    BYTE = 12
    WORD = 13
    UINT = 14
    DWORD = 15


class ComplexType(enum.IntEnum):
    NULL = 0
    POINTER = 1
    FUNCTION = 2
    ARRAY = 3


def mktype(base, comp):
    return (comp << 8) + base


class SymbolRecord:
    record_struct = struct.Struct('<8sLhHBB')

    def __init__(self, name, typ=None, section_number=SpecialSectionNumber.UNDEFINED, storage_class=StorageClass.NULL):
        self.name = name
        self.value = None
        self.section_number = section_number
        self.type = typ or 0
        self.storage_class = storage_class
        self.aux_records = []

    def pack(self):
        packed_aux_records = b''.join(self.aux_records)
        if len(packed_aux_records) % 18 != 0:
            raise ValueError('auxiliary records length must be a multiple of 18')
        return self.record_struct.pack(
            self.name,
            self.value,
            self.section_number,
            self.type,
            self.storage_class,
            len(self.aux_records)
        ) + packed_aux_records
