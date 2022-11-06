import sys
import platform
import subprocess
import struct

is64bit = 8*struct.calcsize('P') == 64

arch = 'x86_64' if is64bit else "x86"

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
    elif '191' in compiler:
        compiler_version = '15'
    elif '192' in compiler:
        compiler_version = '16'
    elif '193' in compiler:
        compiler_version = '17'

    subprocess.call(['conan', 'install', '.', '-s', 'compiler.version=%s' % compiler_version, '--build=missing', '-s', 'arch=%s' % arch])
elif sys.platform == "darwin":
    subprocess.call(['conan', 'install', '.', '--build=missing', '-s', 'arch=%s' % arch, '-e', 'CFLAGS=-DHAVE_UNISTD_H'])
else:
    subprocess.call(['conan', 'install', '.', '--build=missing', '-s', 'arch=%s' % arch])
