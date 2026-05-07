import os
import re
import sys
import platform
import subprocess
import struct
import json

is64bit = 8*struct.calcsize('P') == 64

profile_path = os.path.expanduser('~/.conan2/profiles/default')
if not os.path.exists(profile_path):
    print('Creating Conan 2 default profile:', profile_path)
    subprocess.check_call(['conan', 'profile', 'detect', '--force'])

arch = 'x86_64' if is64bit else "x86"

def create_conanbuildinfo_json():
    """Create conanbuildinfo.json compatible with setup.py expectations"""
    try:
        # Get dependency information from Conan cache
        result = subprocess.run(['conan', 'cache', 'path', '--folder', 'libtiff/4.4.0'], 
                              capture_output=True, text=True, check=True)
        libtiff_path = result.stdout.strip()
        
        result = subprocess.run(['conan', 'cache', 'path', '--folder', 'libpng/1.6.38'], 
                              capture_output=True, text=True, check=True)
        libpng_path = result.stdout.strip()
        
        result = subprocess.run(['conan', 'cache', 'path', '--folder', 'libjpeg/9e'], 
                              capture_output=True, text=True, check=True)
        libjpeg_path = result.stdout.strip()
        
        # Create the JSON structure that setup.py expects
        conanbuildinfo = {
            "dependencies": [
                {
                    "include_paths": [
                        os.path.join(libtiff_path, "include"),
                        os.path.join(libpng_path, "include"), 
                        os.path.join(libjpeg_path, "include")
                    ],
                    "lib_paths": [
                        os.path.join(libtiff_path, "lib"),
                        os.path.join(libpng_path, "lib"),
                        os.path.join(libjpeg_path, "lib")
                    ],
                    "libs": ["tiff", "png", "jpeg"],
                    "defines": []
                }
            ]
        }
        
        with open('conanbuildinfo.json', 'w') as f:
            json.dump(conanbuildinfo, f, indent=2)
        print('Created conanbuildinfo.json')
        
    except subprocess.CalledProcessError as e:
        print(f'Warning: Could not create conanbuildinfo.json: {e}')
        # Create a minimal fallback
        conanbuildinfo = {
            "dependencies": [
                {
                    "include_paths": [],
                    "lib_paths": [],
                    "libs": ["tiff", "png", "jpeg"],
                    "defines": []
                }
            ]
        }
        with open('conanbuildinfo.json', 'w') as f:
            json.dump(conanbuildinfo, f, indent=2)
        print('Created minimal conanbuildinfo.json')

if sys.platform == 'win32':
    compiler = platform.python_compiler()
    compiler_version = ''
    match = re.search(r'MSC v\.([0-9]+)', compiler)
    if match:
        msc_ver = int(match.group(1))
        # Map MSC version to Conan MSVC version (193 = 17, 192 = 16, 191 = 15, 190 = 14)
        compiler_version = str(msc_ver // 10)

    print('Python compiler:', compiler)
    print('Using MSVC version:', compiler_version)

    args = [
        'conan', 'install', '.',
        '-s', 'compiler=msvc',
        '-s', 'compiler.version=%s' % compiler_version,
        '-s', 'compiler.runtime=static',
        '-s', 'compiler.cppstd=17',
        '-s', 'arch=%s' % arch,
        '-g', 'VirtualBuildEnv',
        '--build=missing'
    ]

    subprocess.check_call(args)
elif sys.platform == "darwin":

    subprocess.check_call([
        'conan', 'install', '.',
        '-pr', 'default',
        '--build=missing',
        '-g', 'VirtualBuildEnv',
        '-s', 'arch=%s' % arch,
        '-e', 'CFLAGS=-DHAVE_UNISTD_H'
    ])
else:
    subprocess.check_call([
        'conan', 'install', '.',
        '-pr', 'default',
        '--build=missing',
        '-g', 'VirtualBuildEnv',
        '-s', 'arch=%s' % arch
    ])
