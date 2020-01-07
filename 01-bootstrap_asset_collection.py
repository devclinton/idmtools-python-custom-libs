import os
from idmtools.assets import Asset
from idmtools.core.platform_factory import Platform
from idmtools.managers import ExperimentManager
from idmtools_models.python.python_experiment import PythonExperiment

experiment = PythonExperiment(name="fractals asset bootstrap", model_path=os.path.join("requirements_to_asset_collection.py"))
experiment.add_asset(Asset('model_requirements.txt'))
platform = Platform('COMPS2')

experiment.add_asset(Asset(""))
em = ExperimentManager(experiment=experiment, platform=platform)
em.run()
em.wait_till_done()