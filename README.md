cough
=====

A library for building COFF object files.


Tutorial
--------

Start with the ObjectModule class:

    module = ObjectModule()

Now, let's create a '.text' section:

    section = Section(b'.text', SectionFlags.MEM_EXECUTE)

Add a bit of code:

    section.data = b'\x29\xC0\xC3'  # return 0

Good enough, let's add it to our module:

    module.sections.append(section)

To make use of that bit of code, we are going to need an exported symbol:

    main = SymbolRecord(b'main', section_number=1, storage_class=StorageClass.EXTERNAL)

Set the value to the offset in the section:

    main.value = 0

And add it to our module:

    module.symbols.append(main)

That's enough, let's write our module to a file:

    with open('test.obj', 'wb') as obj_file:
        obj_file.write(module.get_buffer())
