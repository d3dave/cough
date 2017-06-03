import os
import tempfile
import subprocess

import coff

TESTS_DIR = os.path.dirname(__file__)
BUILD_SCRIPT = os.path.join(TESTS_DIR, 'build.ps1')


def test_coff():
    module = coff.ObjectModule()

    # mov rax, 0; ret
    sec_aaaa = coff.Section(b'aaaa', coff.SectionFlags.MEM_EXECUTE, b'\x48\xC7\xC0\x00\x00\x00\x00\xC3')
    module.sections.append(sec_aaaa)

    sym1 = coff.SymbolRecord()
    sym1.name = b'main'
    sym1.section_number = 1  # aaaa
    sym1.storage_class = coff.StorageClass.EXTERNAL
    sym1.value = 0
    sym1.type = 0
    module.symbols.append(sym1)

    file_buffer = module.get_buffer()
    with tempfile.NamedTemporaryFile(suffix='.obj', delete=False) as file:
        file.write(file_buffer)
    base, _ = os.path.splitext(file.name)
    exe_path = base + '.exe'
    subprocess.run(['PowerShell.exe', BUILD_SCRIPT, file.name, '/out:' + '"' + exe_path + '"'], check=True)
    subprocess.run([exe_path], check=True)
