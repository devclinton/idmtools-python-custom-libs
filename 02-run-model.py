import os
from idmtools.assets import Asset, AssetCollection
from idmtools.builders import ExperimentBuilder
from idmtools.core.platform_factory import Platform
from idmtools.managers import ExperimentManager
from idmtools_models.python.python_experiment import PythonExperiment


class setParam:
    def __init__(self, param):
        self.param = param

    def __call__(self, simulation, value):
        return simulation.set_parameter(self.param, value)

ac = AssetCollection()
# Add the libraries to an AssetCollection
ac.add_directory('Libraries')
experiment = PythonExperiment(name="fractals are cool", model_path=os.path.join("model.py"))
# Add asset collection to experiment
experiment.add_assets(ac)

builder = ExperimentBuilder()
builder.add_sweep_definition(setParam("min_x"), range(-2, 0))
builder.add_sweep_definition(setParam("max_x"), range(1, 3))
builder.add_sweep_definition(setParam("min_y"), range(-2, 0))
builder.add_sweep_definition(setParam("max_y"), range(1, 3))
builder.add_sweep_definition(setParam("iters"), range(10, 40, 10))
experiment.add_builder(builder)

platform = Platform('COMPS2')
em = ExperimentManager(experiment=experiment, platform=platform)
em.run()
em.wait_till_done()