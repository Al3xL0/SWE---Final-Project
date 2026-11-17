"""Build independent spacecraft with circular Earth-centred initial orbits."""
from math import radians
from Basilisk.simulation import spacecraft
from Basilisk.utilities import orbitalMotion


def build_constellation(sim, task_name, gravity, earth, groups):
    satellites, colors, recorders = [], [], []
    for group in groups:
        for index in range(group.count):
            satellite = spacecraft.Spacecraft()
            satellite.ModelTag = f"{group.name}-{index + 1:02d}"
            satellite.hub.mHub = 100.0
            satellite.hub.IHubPntBc_B = [[20., 0., 0.], [0., 20., 0.], [0., 0., 20.]]
            gravity.addBodiesTo(satellite)

            elements = orbitalMotion.ClassicElements()
            elements.a = earth.radEquator + group.altitude_m
            elements.e = 0.0
            elements.i = radians(group.inclination_deg)
            # Separate planes and phases make individual spacecraft easy to see.
            elements.Omega = radians(group.raan_offset_deg + 360 * index / group.count)
            elements.omega = 0.0
            elements.f = radians(360 * index / group.count)
            position, velocity = orbitalMotion.elem2rv(earth.mu, elements)
            satellite.hub.r_CN_NInit = position
            satellite.hub.v_CN_NInit = velocity
            sim.AddModelToTask(task_name, satellite)
            recorder = satellite.scStateOutMsg.recorder()
            sim.AddModelToTask(task_name, recorder)
            satellites.append(satellite)
            colors.append(list(group.color))
            recorders.append(recorder)
    return satellites, colors, recorders
