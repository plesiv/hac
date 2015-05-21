import os

rootDir = os.path.dirname(os.path.realpath(__file__))
configDir = os.path.join(rootDir, 'config')

files = [ os.path.join(os.path.relpath(dir_, rootDir), fileName) for dir_, _, files in os.walk(configDir) for fileName in files ]
print(files)

