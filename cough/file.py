"""
Overall COFF file structure
"""
import time
import enum
import struct

from .string_table import StringTable


class MachineType(enum.IntEnum):
    UNKNOWN = 0x0
    AM33 = 0x1d3
    AMD64 = 0x8664
    ARM = 0x1c0
    ARM64 = 0xaa64
    ARMNT = 0x1c4
    EBC = 0xebc
    I386 = 0x14c
    IA64 = 0x200
    M32R = 0x9041
    MIPS16 = 0x266
    MIPSFPU = 0x366
    MIPSFPU16 = 0x466
    POWERPC = 0x1f0
    POWERPCFP = 0x1f1
    R4000 = 0x166
    RISCV32 = 0x5032
    RISCV64 = 0x5064
    RISCV128 = 0x5128
    SH3 = 0x1a2
    SH3DSP = 0x1a3
    SH4 = 0x1a6
    SH5 = 0x1a8
    THUMB = 0x1c2
    WCEMIPSV2 = 0x169


class FileHeader:
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
    struct = struct.Struct('<HHLLLHH')

    def __init__(self, machine=MachineType.AMD64):
        self.machine = machine
        self.number_of_sections = 0
        self.time_date_stamp = 0
        self.pointer_to_symtab = 0
        self.number_of_symbols = 0
        self.size_of_opt_header = 0
        self.characteristics = 0

    def pack(self):
        return self.struct.pack(
            self.machine,
            self.number_of_sections,
            self.time_date_stamp,
            self.pointer_to_symtab,
            self.number_of_symbols,
            self.size_of_opt_header,
            self.characteristics
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
        self.file_header.time_date_stamp = int(time.time())
        self.file_header.number_of_sections = len(self.sections)
        self.file_header.number_of_symbols = len(self.symbols)

        self.file_header.pointer_to_symtab = FileHeader.struct.size + len(sections_buffer)
        body_buffer = bytearray()
        body_buffer += self.file_header.pack()
        body_buffer += sections_buffer
        for sym in self.symbols:
            body_buffer += sym.pack()
        body_buffer += self.string_table.pack()
        return bytes(body_buffer)

    def dump_sections(self):
        data_buf = bytearray()
        sections_offsets = []
        reloc_offsets = []
        for sec in self.sections:
            if sec.data:
                sections_offsets.append(len(data_buf))
                data_buf += sec.data
            if sec.relocations:
                reloc_offsets.append(len(data_buf))
                for reloc in sec.relocations:
                    data_buf += reloc.pack()

        sections_buffer_offset = FileHeader.struct.size + 40 * len(self.sections)
        hdrs_and_data_buf = bytearray()
        for i, sec in enumerate(self.sections):
            if sec.data:
                sec.pointer_to_raw_data = sections_buffer_offset + sections_offsets[i]
            if sec.relocations:
                sec.pointer_to_relocations = sections_buffer_offset + reloc_offsets[i]
            hdrs_and_data_buf += sec.get_header()
        hdrs_and_data_buf += data_buf
        return bytes(hdrs_and_data_buf)
