import glob
import hashlib
import shutil
import subprocess
import sys
import os
from COMPS import Client
from COMPS.Data import AssetCollection, AssetCollectionFile

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
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


def create_asset_collection(path_to_ac, name, other_tags = None):
    """
    Create python asset collection from folder
    """
    if other_tags is None:
        other_tags = dict()
    path_to_ac = os.path.normpath(path_to_ac)

    if not os.path.exists(path_to_ac) or not os.path.isdir(path_to_ac):
        print('Path \'{0}\' doesn\'t exist or is not a directory'.format(path_to_ac))
        exit()

    tags = other_tags
    tags['python_version'] = sys.version
    tags['os'] = sys.platform
    tags['Name'] = name
    print("Adding files to asset Collection")
    ac = AssetCollection()

    ac.set_tags(tags)

    for (dirpath, dirnames, filenames) in os.walk(path_to_ac):
        for fn in filenames:
            rp = os.path.relpath(dirpath, path_to_ac) if dirpath != path_to_ac else ''
            print('Adding {0}'.format(os.path.join(rp, fn)))
            with open(os.path.join(dirpath, fn), 'rb') as fp:
                acf = AssetCollectionFile(fn, rp, md5_checksum=hashlib.md5(fp.read()).hexdigest())
                print(acf.md5_checksum)
            ac.add_asset(acf, os.path.join(dirpath, fn))
    print('Saving collection')
    ac.save()
    print('done - created AC ' + str(ac.id))

def cleanup_files(full_path):
    files = glob.glob(full_path + '/*.dist-info', recursive=True)
    for file in files:
        if os.path.isdir(file):
            shutil.rmtree(file)
        else:
            os.remove(file)


if __name__ == "__main__":
    #Client.login('https://comps2.idmod.org')
    if sys.platform == "win32":
        full_path = os.path.join(LIB_PATH, 'lib', 'site-packages')
    else:
        full_path = os.path.join(LIB_PATH, 'lib', 'python{}'.format(sys.version[:3]), 'site-packages')
    print("Adding {} to the system path".format(full_path))
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    sys.path.insert(1, full_path)
    install_packages_from_requirements('Assets/model_requirements.txt', sys.path)
    cleanup_files(full_path)
    print('Asset size: {} mb'.format(sum(os.path.getsize(f) for f in os.listdir('.') if os.path.isfile(f))/2**20))
    # ? How do we login when running on comps? Should the idmtools script
    # cache the token somehow? Maybe pass as environment variable?
    #create_asset_collection(full_path, name='fractal assets')
