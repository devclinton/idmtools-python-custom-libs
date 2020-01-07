import os
from COMPS import Client, AuthManager
from idmtools.assets import Asset
from idmtools.core.platform_factory import Platform
from idmtools.managers import ExperimentManager
from idmtools_models.python.python_experiment import PythonExperiment

# This provisions a script runs a pip install on a requirements.txt file to a temp direcorty on COMPS and then creates
# an asset collection from the output. This helps avoid target the COMPS python binary that is currently available and
# also avoid the need for the user to upload a large set of files to COMPS

experiment = PythonExperiment(name="fractals asset bootstrap", model_path=os.path.join("requirements_to_asset_collection.py"))
experiment.add_asset(Asset('model_requirements.txt'))
platform = Platform('COMPS2')
am = AuthManager(platform.endpoint)
with open('token.txt', 'w') as of:
    of.write(am.get_auth_token()[1])
experiment.base_simulation.add_asset(Asset("token.txt"))
em = ExperimentManager(experiment=experiment, platform=platform)
em.run()
em.wait_till_done()