import glob
import hashlib
import re
import shutil
import subprocess
import sys
import os
import traceback
from pprint import pprint

CURRENT_DIRECTORY = os.getcwd()
LIB_PATH = os.path.join(CURRENT_DIRECTORY, 'Libraries')


def install_packages_from_requirements(requirements_file='requirements.txt', python_paths=None):
    """
    Install our packages to a local directory
    """
    if python_paths is None:
        env = dict()
    else:
        if type(python_paths) is not list:
            python_paths = [python_paths]
        #env = dict(PYTHONPATH=os.pathsep.join(python_paths))
        env = dict(os.environ)
        env['PYTHONPATH'] = os.pathsep.join(python_paths)
    print("Running pip install -r {} to tmp directory".format(requirements_file))
    subprocess.check_call([sys.executable, "-m", "pip", 'install',  '--prefix', LIB_PATH, "-r", requirements_file],
                          env=env)

if __name__ == "__main__":
    if sys.platform == "win32":
        full_path = os.path.join(LIB_PATH, 'lib', 'site-packages')
    else:
        full_path = os.path.join(LIB_PATH, 'lib', 'python{}'.format(sys.version[:3]), 'site-packages')
    print("Adding {} to the system path".format(full_path))
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    sys.path.insert(1, full_path)
    tb = None
    try:
        install_packages_from_requirements('Assets/model_requirements.txt', sys.path)
        print('Asset size: {} mb'.format(sum(os.path.getsize(f) for f in os.listdir('.') if os.path.isfile(f))/2**20))
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
    finally:
        if tb:
            sys.exit(-1)
