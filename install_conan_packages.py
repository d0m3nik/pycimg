import os
import re
import sys
import platform
import subprocess
import struct

is64bit = 8*struct.calcsize('P') == 64

profile_path = os.path.expanduser('~/.conan2/profiles/default')
if not os.path.exists(profile_path):
    print('Creating Conan 2 default profile:', profile_path)
    subprocess.check_call(['conan', 'profile', 'detect', '--force'])

arch = 'x86_64' if is64bit else "x86"

if sys.platform == 'win32':
    compiler = platform.python_compiler()
    compiler_version = ''
    match = re.search(r'MSC v\.([0-9]+)', compiler)
    if match:
        compiler_version = str(int(match.group(1)) // 10)

    args = [
        'conan', 'install', '.',
        '-pr', 'default',
        '-s', 'compiler=msvc',
    ]
    if compiler_version:
        args += ['-s', 'compiler.version=%s' % compiler_version]
    args += [
        '-s', 'compiler.runtime=MT',
        '-s', 'compiler.cppstd=17',
        '-s', 'arch=%s' % arch,
        '-g', 'VirtualBuildEnv',
        '--build=missing'
    ]

    subprocess.check_call(args)
elif sys.platform == "darwin":

    subprocess.check_call([
        'conan', 'install', '.',
        '--build=missing',
        '-g', 'json',
        '-s', 'arch=%s' % arch,
        '-e', 'CFLAGS=-DHAVE_UNISTD_H'
    ])
else:
    subprocess.check_call([
        'conan', 'install', '.',
        '--build=missing',
        '-g', 'json',
        '-s', 'arch=%s' % arch
    ])
