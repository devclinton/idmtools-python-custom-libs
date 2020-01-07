import os
from functools import partial
from idmtools.assets import Asset
from idmtools.builders import ExperimentBuilder
from idmtools.core.platform_factory import Platform
from idmtools.managers import ExperimentManager
from idmtools_models.python.python_experiment import PythonExperiment


class setParam:
    def __init__(self, param):
        self.param = param

    def __call__(self, simulation, value):
        return simulation.set_parameter(self.param, value)


experiment = PythonExperiment(name="numba example", model_path=os.path.join("model.py"))
# get the asset id from 01-bootstrap_asset_collection.py
experiment.add_asset(Asset(id=''))


builder = ExperimentBuilder()
builder.add_sweep_definition(setParam("min_x"), range(-2, 0))
builder.add_sweep_definition(setParam("max_x"), range(1, 3))
builder.add_sweep_definition(setParam("min_y"), range(-2, 0))
builder.add_sweep_definition(setParam("max_y"), range(1, 3))
builder.add_sweep_definition(setParam("iters"), range(10, 40, step=10))
experiment.add_builder(builder)

platform = Platform('COMPS')

em = ExperimentManager(experiment=experiment, platform=platform)
em.run()
em.wait_till_done()