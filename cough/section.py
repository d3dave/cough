import enum
import struct


class SectionFlags(enum.IntFlag):
    CNT_CODE = 0x00000020
    CNT_INITIALIZED_DATA = 0x00000040
    CNT_UNINITIALIZED_DATA = 0x00000080
    LNK_INFO = 0x00000200
    LNK_REMOVE = 0x00000800
    LNK_COMDAT = 0x00001000
    GPREL = 0x00008000
    ALIGN_1BYTES = 0x00100000
    ALIGN_2BYTES = 0x00200000
    ALIGN_4BYTES = 0x00300000
    ALIGN_8BYTES = 0x00400000
    ALIGN_16BYTES = 0x00500000
    ALIGN_32BYTES = 0x00600000
    ALIGN_64BYTES = 0x00700000
    ALIGN_128BYTES = 0x00800000
    ALIGN_256BYTES = 0x00900000
    ALIGN_512BYTES = 0x00A00000
    ALIGN_1024BYTES = 0x00B00000
    ALIGN_2048BYTES = 0x00C00000
    ALIGN_4096BYTES = 0x00D00000
    ALIGN_8192BYTES = 0x00E00000
    LNK_NRELOC_OVFL = 0x01000000
    MEM_DISCARDABLE = 0x02000000
    MEM_NOT_CACHED = 0x04000000
    MEM_NOT_PAGED = 0x08000000
    MEM_SHARED = 0x10000000
    MEM_EXECUTE = 0x20000000
    MEM_READ = 0x40000000
    MEM_WRITE = 0x80000000


class Section:
    """
    Header struct:

    Offset	Size	Field
    =====================================
       0	  8	    Name
       8	  4	    VirtualSize
      12	  4	    VirtualAddress
      16	  4	    SizeOfRawData
      20	  4	    PointerToRawData
      24	  4	    PointerToRelocations
      28	  4	    PointerToLinenumbers
      32	  2	    NumberOfRelocations
      34	  2	    NumberOfLinenumbers
      36	  4	    Characteristics

    Name:
        An 8-byte, null-padded UTF-8 encoded string. If the string is exactly 8 characters long, there is no
        terminating null. For longer names, this field contains a slash (/) that is followed by an ASCII
        representation of a decimal number that is an offset into the string table. Long names in object files are
        truncated if they are emitted to an executable file.
    VirtualSize:
        The total size of the section when loaded into memory. Should be set to zero.
    VirtualAddress:
        The address of the first byte of the section relative to the image base when the section is loaded into memory.
        This field is the address of the first byte before relocation is applied; for simplicity, compilers should set
        this to zero. Otherwise, it is an arbitrary value that is subtracted from offsets during relocation.
    SizeOfRawData:
        The size of the section. If this is less than VirtualSize, the remainder of the section is zero-filled. Because
        the SizeOfRawData field is rounded but the VirtualSize field is not, it is possible for SizeOfRawData to be
        greater than VirtualSize as well. When a section contains only uninitialized data, this field should be zero.
    PointerToRawData:
        The file pointer to the first page of the section within the COFF file. The value should be aligned on a 4-byte
        boundary for best performance. When a section contains only uninitialized data, this field should be zero.
    PointerToRelocations:
        The file pointer to the beginning of relocation entries for the section. This is set to zero if there are no
        relocations.
    PointerToLinenumbers:
        The file pointer to the beginning of line-number entries for the section. This is set to zero if there are no
        COFF line numbers.
    NumberOfRelocations:
        The number of relocation entries for the section.
    NumberOfLinenumbers:
        The number of line-number entries for the section.
    Characteristics:
        The flags that describe the characteristics of the section.
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
            self.flags
        )
