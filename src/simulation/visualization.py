"""Vizard recording setup, kept separate from orbital dynamics."""
from Basilisk.utilities import vizSupport


def configure_vizard(sim, task_name, satellites, colors, output_file):
    if not vizSupport.vizFound:
        raise RuntimeError("This Basilisk build has no Vizard interface. Install bsk[all].")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    viz = vizSupport.enableUnityVisualization(
        sim, task_name, satellites, saveFile=str(output_file),
        oscOrbitColorList=colors, trueOrbitColorList=colors,
    )
    viz.settings.orbitLinesOn = 1
    return viz
