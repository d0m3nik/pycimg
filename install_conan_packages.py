import sys
import platform
import subprocess

if sys.platform == 'win32':
    compiler = platform.python_compiler()
    compiler_version = ''
    if '1400' in compiler:
        compiler_version = '8'
    elif '1500' in compiler:
        compiler_version = '9'
    elif '1600' in compiler:
        compiler_version = '10'
    elif '1700' in compiler:
        compiler_version = '11'
    elif '1800' in compiler:
        compiler_version = '12'
    elif '1900' in compiler:
        compiler_version = '14'
    subprocess.call(['conan', 'install',  '.', '-s', 'compiler.version=%s' % compiler_version])
