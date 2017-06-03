"""
"""
import enum
import struct


class MachineType(enum.IntEnum):
    UNKNOWN = 0x0
    """The contents of this field are assumed to be applicable to any machine type"""
    AM33 = 0x1d3
    """Matsushita AM33"""
    AMD64 = 0x8664
    """x64"""
    ARM = 0x1c0
    """ARM little endian"""
    ARM64 = 0xaa64
    """ARM64 little endian"""
    ARMNT = 0x1c4
    """ARM Thumb - 2  little  endian"""
    EBC = 0xebc
    """EFI byte code"""
    I386 = 0x14c
    """Intel 386 or later   processors and compatible    processors"""
    IA64 = 0x200
    """Intel    Itanium    processor    family"""
    M32R = 0x9041
    """Mitsubishi    M32R    little    endian"""
    MIPS16 = 0x266
    """MIPS16"""
    MIPSFPU = 0x366
    """MIPS    with FPU"""
    MIPSFPU16 = 0x466
    """MIPS16        with FPU"""
    POWERPC = 0x1f0
    """Power        PC        little        endian"""
    POWERPCFP = 0x1f1
    """Power    PC    with floating point support"""
    R4000 = 0x166
    """MIPS    little    endian"""
    RISCV32 = 0x5032
    """RISC - V    32 - bit    address    space"""
    RISCV64 = 0x5064
    """RISC - V    64 - bit    address    space"""
    RISCV128 = 0x5128
    """RISC - V    128 - bit    address    space"""
    SH3 = 0x1a2
    """Hitachi    SH3"""
    SH3DSP = 0x1a3
    """Hitachi    SH3    DSP"""
    SH4 = 0x1a6
    """Hitachi    SH4"""
    SH5 = 0x1a8
    """Hitachi    SH5"""
    THUMB = 0x1c2
    """Thumb"""
    WCEMIPSV2 = 0x169
    """MIPS    little - endian    WCE    v2"""


class FileHeader(struct.Struct):
    """
    Offset	Size	Field
    =====================================
       0	  2	    Machine
       2	  2	    NumberOfSections
       4	  4	    TimeDateStamp
       8	  4	    PointerToSymbolTable
      12	  4	    NumberOfSymbols
      16	  2	    SizeOfOptionalHeader
      18	  2	    Characteristics

    Machine:
        Target machine type.
    NumberOfSections:
        Indicates the size of the section table, which immediately follows the headers.
    TimeDateStamp:
        Indicates when the file was created. The low 32 bits of the number of seconds since 1970-01-01 00:00.
    PointerToSymbolTable:
        The file offset of the COFF symbol table, or zero if no COFF symbol table is present.
    NumberOfSymbols:
        The number of entries in the symbol table.
        This data can be used to locate the string table, which immediately follows the symbol table.
    SizeOfOptionalHeader:
        The size of the optional header, which is required for executable files but not for object files.
    Characteristics:
        The flags that indicate the attributes of the file.
    """

    def __init__(self):
        super().__init__('<HHLLLHH')
        self.machine = MachineType.AMD64
        self.number_of_sections = 0
        self.time_date_stamp = 0
        self.pointer_to_symtab = 0
        self.number_of_symbols = 0
        self.size_of_opt_header = 0
        self.characteristics = 0

    def pack(self):
        return super().pack(self.machine, self.number_of_sections, self.time_date_stamp, self.pointer_to_symtab,
                            self.number_of_symbols, self.size_of_opt_header, self.characteristics)


class SectionFlags(enum.IntFlag):
    TYPE_NO_PAD = 0x00000008  # The section should not be padded to the next boundary. This flag is obsolete and is replaced by ALIGN_1BYTES. This is valid only for object files.
    CNT_CODE = 0x00000020  # The section contains executable code.
    CNT_INITIALIZED_DATA = 0x00000040  # The section contains initialized data.
    CNT_UNINITIALIZED_DATA = 0x00000080  # The section contains uninitialized data.
    LNK_INFO = 0x00000200  # The section contains comments or other information. The .drectve section has this type. This is valid for object files only.
    LNK_REMOVE = 0x00000800  # The section will not become part of the image. This is valid only for object files.
    LNK_COMDAT = 0x00001000  # The section contains COMDAT data. For more information, see section 5.5.6, “COMDAT Sections (Object Only).” This is valid only for object files.
    GPREL = 0x00008000  # The section contains data referenced through the global pointer (GP).
    ALIGN_1BYTES = 0x00100000  # Align data on a 1-byte boundary. Valid only for object files.
    ALIGN_2BYTES = 0x00200000  # Align data on a 2-byte boundary. Valid only for object files.
    ALIGN_4BYTES = 0x00300000  # Align data on a 4-byte boundary. Valid only for object files.
    ALIGN_8BYTES = 0x00400000  # Align data on an 8-byte boundary. Valid only for object files.
    ALIGN_16BYTES = 0x00500000  # Align data on a 16-byte boundary. Valid only for object files.
    ALIGN_32BYTES = 0x00600000  # Align data on a 32-byte boundary. Valid only for object files.
    ALIGN_64BYTES = 0x00700000  # Align data on a 64-byte boundary. Valid only for object files.
    ALIGN_128BYTES = 0x00800000  # Align data on a 128-byte boundary. Valid only for object files.
    ALIGN_256BYTES = 0x00900000  # Align data on a 256-byte boundary. Valid only for object files.
    ALIGN_512BYTES = 0x00A00000  # Align data on a 512-byte boundary. Valid only for object files.
    ALIGN_1024BYTES = 0x00B00000  # Align data on a 1024-byte boundary. Valid only for object files.
    ALIGN_2048BYTES = 0x00C00000  # Align data on a 2048-byte boundary. Valid only for object files.
    ALIGN_4096BYTES = 0x00D00000  # Align data on a 4096-byte boundary. Valid only for object files.
    ALIGN_8192BYTES = 0x00E00000  # Align data on an 8192-byte boundary. Valid only for object files.
    LNK_NRELOC_OVFL = 0x01000000  # The section contains extended relocations.
    MEM_DISCARDABLE = 0x02000000  # The section can be discarded as needed.
    MEM_NOT_CACHED = 0x04000000  # The section cannot be cached.
    MEM_NOT_PAGED = 0x08000000  # The section is not pageable.
    MEM_SHARED = 0x10000000  # The section can be shared in memory.
    MEM_EXECUTE = 0x20000000  # The section can be executed as code.
    MEM_READ = 0x40000000  # The section can be read.
    MEM_WRITE = 0x80000000  # The section can be written to.


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


class SymbolRecord(struct.Struct):
    def __init__(self):
        super().__init__('<8sLHHBB')
        self.name = None
        self.value = None
        self.section_number = None
        self.type = None
        self.storage_class = None
        self.aux_symbols = []

    def pack(self):
        packed_aux_symbols = b''.join(s.pack() for s in self.aux_symbols)
        return super().pack(self.name, self.value, self.section_number, self.type, self.storage_class,
                            len(self.aux_symbols)) + packed_aux_symbols


class Section:
    """
    Header struct:
      0	8	Name	An 8-byte, null-padded UTF-8 encoded string. If the string is exactly 8 characters long, there is no terminating null. For longer names, this field contains a slash (/) that is followed by an ASCII representation of a decimal number that is an offset into the string table. Executable images do not use a string table and do not support section names longer than 8 characters. Long names in object files are truncated if they are emitted to an executable file.
      8	4	VirtualSize	The total size of the section when loaded into memory. If this value is greater than SizeOfRawData, the section is zero-padded. This field is valid only for executable images and should be set to zero for object files.
    12	4	VirtualAddress	For executable images, the address of the first byte of the section relative to the image base when the section is loaded into memory. For object files, this field is the address of the first byte before relocation is applied; for simplicity, compilers should set this to zero. Otherwise, it is an arbitrary value that is subtracted from offsets during relocation.
    16	4	SizeOfRawData	The size of the section (for object files) or the size of the initialized data on disk (for image files). For executable images, this must be a multiple of FileAlignment from the optional header. If this is less than VirtualSize, the remainder of the section is zero-filled. Because the SizeOfRawData field is rounded but the VirtualSize field is not, it is possible for SizeOfRawData to be greater than VirtualSize as well. When a section contains only uninitialized data, this field should be zero.
    20	4	PointerToRawData	The file pointer to the first page of the section within the COFF file. For executable images, this must be a multiple of FileAlignment from the optional header. For object files, the value should be aligned on a 4-byte boundary for best performance. When a section contains only uninitialized data, this field should be zero.
    24	4	PointerToRelocations	The file pointer to the beginning of relocation entries for the section. This is set to zero for executable images or if there are no relocations.
    28	4	PointerToLinenumbers	The file pointer to the beginning of line-number entries for the section. This is set to zero if there are no COFF line numbers. This value should be zero for an image because COFF debugging information is deprecated.
    32	2	NumberOfRelocations	The number of relocation entries for the section. This is set to zero for executable images.
    34	2	NumberOfLinenumbers	The number of line-number entries for the section. This value should be zero for an image because COFF debugging information is deprecated.
    36	4	Characteristics	The flags that describe the characteristics of the section. For more information, see section 4.1, “Section Flags.”
    """
    header_struct = struct.Struct('<8sLLLLLLHHL')

    def __init__(self, name, flags=None, data=None):
        self.name = name
        self.flags = flags or 0
        self.data = data
        self.virtual_size = 0
        self.virtual_address = 0
        self.size_of_raw_data = len(data) if data else 0
        self.pointer_to_raw_data = 0
        self.pointer_to_relocations = 0
        self.pointer_to_linenumbers = 0
        self.number_of_relocations = 0
        self.number_of_linenumbers = 0

    def get_header(self):
        return self.header_struct.pack(
            self.name,
            self.virtual_size,
            self.virtual_address,
            self.size_of_raw_data,
            self.pointer_to_raw_data,
            self.pointer_to_relocations,
            self.pointer_to_linenumbers,
            self.number_of_relocations,
            self.number_of_linenumbers,
            self.flags,
        )


class ObjectModule:
    """
    Layout:
    +-----------------+
    |     Header      |
    +-----------------+
    | Section headers |
    +-----------------+
    |    Sections     |
    +-----------------+
    |  Symbol table   |
    +-----------------+
    |  String table   |
    +-----------------+
    """

    def __init__(self):
        self.file_header = FileHeader()
        self.sections = []
        self.symbols = []
        self.string_table = StringTable()

    def get_buffer(self):
        sections_buffer = self.dump_sections()
        self.file_header.pointer_to_symtab = self.file_header.size + len(sections_buffer)
        self.file_header.number_of_symbols = len(self.symbols)
        self.file_header.number_of_sections = len(self.sections)

        body_buffer = bytearray()
        body_buffer += self.file_header.pack()
        body_buffer += sections_buffer
        for sym in self.symbols:
            body_buffer += sym.pack()
        body_buffer += self.string_table.pack()
        return bytes(body_buffer)

    def dump_sections(self):
        data_buf = bytearray()
        offsets = []
        for sec in self.sections:
            if sec.data:
                offsets.append(len(data_buf))
                data_buf += sec.data

        sections_offset = self.file_header.size + 40 * len(self.sections)
        hdrs_and_data_buf = bytearray()
        for i, sec in enumerate(self.sections):
            if sec.data:
                sec.pointer_to_raw_data = sections_offset + offsets[i]
            hdrs_and_data_buf += sec.get_header()
        hdrs_and_data_buf += data_buf
        return bytes(hdrs_and_data_buf)
