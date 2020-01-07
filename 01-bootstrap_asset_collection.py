import subprocess
import sys
import os

from COMPS
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
            acf = AssetCollectionFile(fn, rp, tags={'Executable': None} if os.path.splitext(fn)[1] == '.exe' else None)
            ac.add_asset(acf, os.path.join(dirpath, fn))

    ac.save()
    print('done - created AC ' + str(ac.id))


if __name__ == "__main__":
    if 'nt' in sys.platform:
        full_path = os.path.join(LIB_PATH, 'lib', 'site-packages')
    else:
        full_path = os.path.join(LIB_PATH, 'lib', 'python{}'.format(sys.version[:3]), 'site-packages')
    print("Adding {} to the system path".format(full_path))
    #'/home/clinton/development/work/idmtools-python-custom-libs/Libraries/lib/python3.6/site-packages/numpy'
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    sys.path.insert(1, full_path)
    install_packages_from_requirements('model_requirements.txt', sys.path)
    login()
    create_asset_collection(full_path)
