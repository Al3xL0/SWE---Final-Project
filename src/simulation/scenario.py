"""Compose and execute the simulation; export trajectories for later analysis."""
import csv
from dataclasses import dataclass
from pathlib import Path
from Basilisk.utilities import SimulationBaseClass, macros, simIncludeGravBody

if __package__:
    from .constellation import build_constellation
    from .visualization import configure_vizard
else:
    from constellation import build_constellation
    from visualization import configure_vizard


@dataclass(frozen=True)
class SimulationResult:
    vizard_file: Path
    trajectories_file: Path


def run_simulation(config, output_dir):
    config.validate()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    sim = SimulationBaseClass.SimBaseClass()
    task_name = "orbitDynamics"
    process = sim.CreateNewProcess("dynamics")
    process.addTask(sim.CreateNewTask(task_name, macros.sec2nano(config.step_s)))
    gravity = simIncludeGravBody.gravBodyFactory()
    earth = gravity.createEarth()
    earth.isCentralBody = True
    satellites, colors, recorders = build_constellation(
        sim, task_name, gravity, earth, config.groups
    )
    vizard_file = output_dir / "leo_meo.bin"
    viz = configure_vizard(sim, task_name, satellites, colors, vizard_file)
    sim.InitializeSimulation()
    sim.ConfigureStopTime(macros.sec2nano(config.duration_s))
    sim.ExecuteSimulation()
    trajectories_file = output_dir / "trajectories.csv"
    with trajectories_file.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["satellite", "time_s", "x_m", "y_m", "z_m", "vx_m_s", "vy_m_s", "vz_m_s"])
        for satellite, recorder in zip(satellites, recorders):
            for time, position, velocity in zip(recorder.times(), recorder.r_BN_N, recorder.v_BN_N):
                writer.writerow([satellite.ModelTag, time * macros.NANO2SEC, *position, *velocity])
    # Retain the visualization and gravity objects until execution has finished.
    del viz
    return SimulationResult(vizard_file, trajectories_file)
