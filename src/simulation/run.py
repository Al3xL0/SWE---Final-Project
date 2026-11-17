"""Command line entry point: python src/simulation/run.py."""
import argparse
from pathlib import Path

if __package__:
    from .config import SimulationConfig
else:
    from config import SimulationConfig


def positive_number(value):
    from math import isfinite
    number = float(value)
    if not isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("Expected a finite positive number.")
    return number


def main():
    parser = argparse.ArgumentParser(description="Record 5 LEO and 2 MEO satellites for Vizard.")
    parser.add_argument("--hours", type=positive_number, default=12.0)
    parser.add_argument("--step", type=positive_number, default=10.0, help="Integration/output step in seconds")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "output")
    args = parser.parse_args()
    try:
        if __package__:
            from .scenario import run_simulation
        else:
            from scenario import run_simulation
    except ModuleNotFoundError as error:
        if error.name == "Basilisk":
            parser.exit(1, "Basilisk is missing. Run using the project's .venv Python.\n")
        raise
    config = SimulationConfig(duration_s=args.hours * 3600, step_s=args.step)
    try:
        result = run_simulation(config, args.output)
    except (ValueError, RuntimeError) as error:
        parser.exit(1, f"Simulation failed: {error}\n")
    print(f"Vizard recording: {result.vizard_file}")
    print(f"Trajectory data:  {result.trajectories_file}")
    print("Open the .bin recording in Vizard and press Play. Select Earth and zoom out to see both orbit groups.")


if __name__ == "__main__":
    main()
