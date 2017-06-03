import enum
import struct


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
            self.flags
        )