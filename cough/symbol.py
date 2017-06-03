import enum
import struct


class SpecialSectionNumber(enum.IntEnum):
    UNDEFINED = 0
    ABSOLUTE = -1
    DEBUG = -2


class StorageClass(enum.IntEnum):
    END_OF_FUNCTION = -1  # A special symbol that represents the end of function, for debugging purposes.
    NULL = 0  # No assigned storage class.
    AUTOMATIC = 1  # The automatic (stack) variable. The Value field specifies the stack frame offset.
    EXTERNAL = 2  # A value that Microsoft tools use for external symbols. The Value field indicates the size if the section number is IMAGE_SYM_UNDEFINED (0). If the section number is not zero, then the Value field specifies the offset within the section.
    STATIC = 3  # The offset of the symbol within the section. If the Value field is zero, then the symbol represents a section name.
    REGISTER = 4  # A register variable. The Value field specifies the register number.
    EXTERNAL_DEF = 5  # A symbol that is defined externally.
    LABEL = 6  # A code label that is defined within the module. The Value field specifies the offset of the symbol within the section.
    UNDEFINED_LABEL = 7  # A reference to a code label that is not defined.
    MEMBER_OF_STRUCT = 8  # The structure member. The Value field specifies the nth member.
    ARGUMENT = 9  # A formal argument (parameter) of a function. The Value field specifies the nth argument.
    STRUCT_TAG = 10  # The structure tag-name entry.
    MEMBER_OF_UNION = 11  # A union member. The Value field specifies the nth member.
    UNION_TAG = 12  # The Union tag-name entry.
    TYPE_DEFINITION = 13  # A Typedef entry.
    UNDEFINED_STATIC = 14  # A static data declaration.
    ENUM_TAG = 15  # An enumerated type tagname entry.
    MEMBER_OF_ENUM = 16  # A member of an enumeration. The Value field specifies the nth member.
    REGISTER_PARAM = 17  # A register parameter.
    BIT_FIELD = 18  # A bit-field reference. The Value field specifies the nth bit in the bit field.
    BLOCK = 100  # A .bb (beginning of block) or .eb (end of block) record. The Value field is the relocatable address of the code location.
    FUNCTION = 101  # A value that Microsoft tools use for symbol records that define the extent of a function: begin function (.bf), end function (.ef), and lines in function (.lf). For .lf records, the Value field gives the number of source lines in the function. For .ef records, the Value field gives the size of the function code.
    END_OF_STRUCT = 102  # An end-of-structure entry.
    FILE = 103  # A value that Microsoft tools, as well as traditional COFF format, use for the source-file symbol record. The symbol is followed by auxiliary records that name the file.
    SECTION = 104  # A definition of a section (Microsoft tools use STATIC storage class instead).
    WEAK_EXTERNAL = 105  # A weak external. For more information, see section 5.5.3, “Auxiliary Format 3: Weak Externals.”
    CLR_TOKEN = 107  # A CLR token symbol. The name is an ASCII string that consists of the hexadecimal value of the token. For more information, see section 5.5.7, “CLR Token Definition (Object Only).”


class BaseType(enum.IntEnum):
    NULL = 0  # No type information or unknown base type. Microsoft tools use this setting
    VOID = 1  # No valid type; used with void pointers and functions
    CHAR = 2  # A character (signed byte)
    SHORT = 3  # A 2-byte signed integer
    INT = 4  # A natural integer type (normally 4 bytes in Windows)
    LONG = 5  # A 4-byte signed integer
    FLOAT = 6  # A 4-byte floating-point number
    DOUBLE = 7  # An 8-byte floating-point number
    STRUCT = 8  # A structure
    UNION = 9  # A union
    ENUM = 10  # An enumerated type
    MOE = 11  # A member of enumeration (a specific value)
    BYTE = 12  # A byte; unsigned 1-byte integer
    WORD = 13  # A word; unsigned 2-byte integer
    UINT = 14  # An unsigned integer of natural size (normally, 4 bytes)
    DWORD = 15  # An unsigned 4-byte integer


class ComplexType(enum.IntEnum):
    NULL = 0  # No derived type; the symbol is a simple scalar variable.
    POINTER = 1  # The symbol is a pointer to base type.
    FUNCTION = 2  # The symbol is a function that returns a base type.
    ARRAY = 3  # The symbol is an array of base type.


def mktype(base, comp):
    return comp << 8 + base


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
