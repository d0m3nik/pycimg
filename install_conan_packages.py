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
        # Try to get paths for the expected packages, with fallbacks
        lib_paths = []
        include_paths = []
        
        # Try different possible package references
        packages_to_try = [
            ('libtiff', ['libtiff/4.4.0', 'libtiff/4.6.0']),
            ('libpng', ['libpng/1.6.38', 'libpng/1.6.40']),
            ('libjpeg', ['libjpeg/9e', 'libjpeg/9f'])
        ]
        
        for lib_name, package_refs in packages_to_try:
            path_found = False
            for ref in package_refs:
                try:
                    result = subprocess.run(['conan', 'cache', 'path', '--folder', ref], 
                                          capture_output=True, text=True, check=True)
                    package_path = result.stdout.strip()
                    include_paths.append(os.path.join(package_path, "include"))
                    lib_paths.append(os.path.join(package_path, "lib"))
                    path_found = True
                    break
                except subprocess.CalledProcessError:
                    continue
            
            if not path_found:
                print(f'Warning: Could not find path for {lib_name}')
        
        # Create the JSON structure that setup.py expects
        conanbuildinfo = {
            "dependencies": [
                {
                    "include_paths": include_paths,
                    "lib_paths": lib_paths,
                    "libs": ["tiff", "png", "jpeg"],
                    "defines": []
                }
            ]
        }
        
        with open('conanbuildinfo.json', 'w') as f:
            json.dump(conanbuildinfo, f, indent=2)
        print('Created conanbuildinfo.json')
        print('Contents:', json.dumps(conanbuildinfo, indent=2))
        
    except Exception as e:
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
        print('Contents:', json.dumps(conanbuildinfo, indent=2))

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

# Create conanbuildinfo.json for setup.py after all platform installs
create_conanbuildinfo_json()
