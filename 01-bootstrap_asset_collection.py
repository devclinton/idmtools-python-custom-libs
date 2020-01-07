import os
from COMPS import Client, AuthManager
from idmtools.assets import Asset
from idmtools.core.platform_factory import Platform
from idmtools.managers import ExperimentManager
from idmtools_models.python.python_experiment import PythonExperiment

experiment = PythonExperiment(name="fractals asset bootstrap", model_path=os.path.join("requirements_to_asset_collection.py"))
experiment.add_asset(Asset('model_requirements.txt'))
platform = Platform('COMPS2')
cl = Client.login(platform.endpoint)
am = AuthManager(platform.endpoint)
with open('token.txt', 'w') as of:
    of.write(am.get_auth_token()[1])
experiment.base_simulation.add_asset(Asset("token.txt"))
em = ExperimentManager(experiment=experiment, platform=platform)
em.run()
em.wait_till_done()