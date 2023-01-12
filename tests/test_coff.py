import os
import tempfile
import subprocess

import cough

TESTS_DIR = os.path.dirname(__file__)
BUILD_SCRIPT = os.path.join(TESTS_DIR, 'build.ps1')


def test_coff():
    module = cough.ObjectModule()

    # mov rax, 0; ret
    sec_aaaa = cough.Section(b'aaaa', cough.SectionFlags.MEM_EXECUTE, b'\x48\xC7\xC0\x00\x00\x00\x00\xC3')
    module.sections.append(sec_aaaa)

    sym1 = cough.SymbolRecord(b'main', section_number=1, storage_class=cough.StorageClass.EXTERNAL)
    sym1.value = 0  # offset 0
    module.symbols.append(sym1)

    file_buffer = module.get_buffer()
    with tempfile.NamedTemporaryFile(suffix='.obj', delete=False) as file:
        file.write(file_buffer)
    base, _ = os.path.splitext(file.name)
    exe_path = f'{base}.exe'
    subprocess.run(['PowerShell.exe', BUILD_SCRIPT, file.name, '/out:' + '"' + exe_path + '"'], check=True)
    subprocess.run([exe_path], check=True)


def test_reloc():
    module = cough.ObjectModule()

    instructions = [
        b'\x48\x83\xEC\x28',      # sub rsp, 28h
        b'\xB9\x41\x00\x00\x00',  # mov ecx, 41h
        b'\xE8\x00\x00\x00\x00',  # call putchar
        b'\x48\x83\xC4\x28',      # add rsp, 28h
        b'\x29\xC0',              # sub eax, eax
        b'\xC3']                  # ret
    sec_aaaa = cough.Section(b'aaaa', cough.SectionFlags.MEM_EXECUTE, b''.join(instructions))
    sec_aaaa.number_of_relocations = 1
    putchar_reloc = cough.Relocation()
    putchar_reloc.virtual_address = 10
    putchar_reloc.symbol_table_index = 1
    putchar_reloc.type = 0x04  # REL32
    sec_aaaa.relocations.append(putchar_reloc)
    module.sections.append(sec_aaaa)

    sym1 = cough.SymbolRecord(b'main', section_number=1, storage_class=cough.StorageClass.EXTERNAL)
    sym1.value = 0  # offset 0
    module.symbols.append(sym1)

    putchar_sym = cough.SymbolRecord(b'putchar', storage_class=cough.StorageClass.EXTERNAL)
    putchar_sym.value = 0
    module.symbols.append(putchar_sym)

    file_buffer = module.get_buffer()
    with tempfile.NamedTemporaryFile(suffix='.obj', delete=False) as file:
        file.write(file_buffer)
    base, _ = os.path.splitext(file.name)
    exe_path = f'{base}.exe'
    subprocess.run(['PowerShell.exe', BUILD_SCRIPT, file.name, '/out:' + '"' + exe_path + '"'], check=True)
    proc = subprocess.run([exe_path], stdout=subprocess.PIPE, check=True)
    assert proc.stdout == b'A'


def test_uninit_before_init():
    module = cough.ObjectModule()

    sec_uninit = cough.Section(b'uninit', cough.SectionFlags.CNT_UNINITIALIZED_DATA)
    sec_uninit.size_of_raw_data = 0x400
    module.sections.append(sec_uninit)

    sec_init = cough.Section(b'init', 0, b'\xAA\xBB\xCC\xDD')
    module.sections.append(sec_init)

    assert module.get_buffer()
