import numpy as np
import math

# Constants
RADIUS_EARTH = 6371000
MINLON = -180
MAXLON = 180


def compute_destination_point(lat, lon, distance, bearing, radius=RADIUS_EARTH)->list[float]:
    delta = distance / radius
    theta = np.deg2rad(bearing)

    phi1 = np.deg2rad(lat)
    lambda1 = np.deg2rad(lon)

    phi2 = math.asin(
        math.sin(phi1) * math.cos(delta) +
        math.cos(phi1) * math.sin(delta) * math.cos(theta)
    )

    lambda2 = lambda1 + math.atan2(
        math.sin(theta) * math.sin(delta) * math.cos(phi1),
        math.cos(delta) - math.sin(phi1) * math.sin(phi2)
    )

    longitude = np.rad2deg(lambda2)
    if longitude < MINLON or longitude > MAXLON:
        # normalise to >=-180 and <=180° if value is >MAXLON or <MINLON
        lambda2 = ((lambda2 + 3 * math.pi) % (2 * math.pi)) - math.pi
        longitude = np.rad2deg(lambda2)

    return [np.rad2deg(phi2), longitude]