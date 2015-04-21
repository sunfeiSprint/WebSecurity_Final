import codecs

BLOCKSIZE = 1048576 # or some other, desired size in bytes
with codecs.open('phase1.json', "r") as sourceFile:
    with codecs.open('phase1_new.json', "w", "ascii") as targetFile:
        while True:
            contents = sourceFile.read(BLOCKSIZE)
            if not contents:
                break
            targetFile.write(contents)
