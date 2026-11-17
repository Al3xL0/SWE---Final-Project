# LEO + MEO simulation

Seven independent spacecraft propagated by Basilisk around Earth, with a Vizard playback recording: **5 LEO at 550 km** and **2 MEO at 10,000 km**. LEO orbit lines are cyan; MEO orbit lines are orange. The default run spans 12 simulated hours with a 10-second integration/output step, enough to see a complete MEO revolution. This is offline playback: Basilisk generates the motion, and Vizard displays it afterward.

## Run (PowerShell, from the repository root)

```powershell
.\.venv\Scripts\python.exe .\src\simulation\run.py
```

For a short initial check:

```powershell
.\.venv\Scripts\python.exe .\src\simulation\run.py --hours 0.1
```

Optional settings:

```powershell
.\.venv\Scripts\python.exe .\src\simulation\run.py --hours 24 --step 10 --output .\src\simulation\output
```

Use the existing project environment, which already contains Basilisk. If setting up a new environment, install the repository's requirements (`python -m pip install -r requirements.txt`). Vizard is a separate desktop application; installing Basilisk does not install Vizard.

## View the motion in Vizard

1. Run the Python entry point and wait for completion.
2. Start Vizard and choose its recorded simulation/file playback mode.
3. Open `src/simulation/output/leo_meo.bin` (the script prints the absolute path).
4. Select Earth as the camera target and zoom out until the larger MEO orbits fit on screen.
5. Press Play and increase playback speed to see the orbital motion clearly. Spacecraft are named `LEO-01` through `LEO-05` and `MEO-01` through `MEO-02`.

The script does not launch Vizard or require a live network connection. Each new run overwrites the recording and CSV in the chosen output directory; use a different `--output` to preserve a run. If playback opens at a close satellite view, selecting Earth and zooming out is necessary to see the whole constellation.

## Files and extension points

| File | Responsibility |
| --- | --- |
| `config.py` | Immutable scenario settings and orbit groups, with input validation |
| `constellation.py` | Spacecraft creation, gravity attachment, initial orbital elements and state recorders |
| `visualization.py` | Vizard connection, orbit colors and recording configuration |
| `scenario.py` | Simulation process/task setup, execution and trajectory export |
| `run.py` | Command-line options and user-facing entry point |

Change `DEFAULT_GROUPS` in `config.py` to adjust counts, altitude, inclination, colors or RAAN offsets. Add another `OrbitGroup` to extend the constellation without changing the simulation engine. Satellites are evenly distributed in RAAN and initial true anomaly within each group; this is an illustrative layout, not an optimized Walker constellation. Initial orbits are circular. Altitude is measured above Basilisk's Earth equatorial radius, not from Earth's centre.

`output/trajectories.csv` contains satellite name, simulation time in seconds, inertial Cartesian position in metres and velocity in metres per second. This is the interface for future analysis, scheduling and visibility calculations. Output and Python caches are ignored by the local `.gitignore`. Existing `examples/` files are untouched.

## Model scope

The model uses Earth point-mass gravity and independent translational spacecraft dynamics. It does not yet include J2, drag, third bodies, Earth rotation/dated SPICE ephemerides, attitude control, imaging payloads, communication links or scheduling constraints. Earth is centred at the inertial origin. The model demonstrates mixed-altitude orbital propagation and visualization; it does not establish observation coverage or image quality. The step size controls numerical integration and recording; use a smaller step if later adding fast dynamics.

Official references: [Basilisk](https://hanspeterschaub.info/basilisk/) and [Vizard](https://hanspeterschaub.info/basilisk/Vizard/Vizard.html).
