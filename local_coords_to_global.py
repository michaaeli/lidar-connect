import numpy as np
import math

# Constants
RADIUS_EARTH = 6371000
MINLON = -180
MAXLON = 180


def compute_destination_point(lat, lon, distance, bearing, radius=RADIUS_EARTH):
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

def xy2latlon(x, y, lato, lono):
    """
    Converts local Cartesian coordinates into latitude and longitude.
    
    Args:
        input_args: List of arguments. Can be [x, y, lato, lono] or [cx, lato, lono] or
                    [x, y, lato, lono, 'option'] or [cx, lato, lono, 'option'] where 
                    'option' can be 'sphere' or 'small' for spherical or small angle approximation.
    
    Returns:
        Tuple of (lat, lon).
    """
    
    lat, lon = xy2latlon_one(x, y, lato, lono)

    return lat, lon

def xy2latlon_one(x, y, lato, lono):
    lato, lono = jdeg2rad(lato, lono)
    R = radearth()

    return xy2latlon_sphere(x, y, lato, lono, R)

def xy2latlon_cartesian(x, y, lato, lono, R):
    r1 = R * np.cos(lato)
    lat = y / R + lato
    lon = x / r1 + lono
    return jrad2deg(lat, lon)

def xy2latlon_sphere(x, y, lato, lono, R):
    r = np.sqrt(x**2 + y**2)
    r1 = R - np.sqrt(R**2 - r**2)
    R1 = np.sqrt((R - r1)**2 + y**2)
    gamma = np.arcsin(y / R1)
    phi = lato + gamma
    xo = R1 * np.cos(phi)
    zo = R1 * np.sin(phi)
    yo = np.sqrt(R**2 - xo**2 - zo**2)
    index = np.where(x < 0)
    if index[0].size > 0:
        yo[index] = -yo[index]
    return xyz2latlon(xo, yo, zo)

def xyz2latlon(x, y, z):
    R = np.sqrt(x**2 + y**2 + z**2)
    x = x / R
    y = y / R
    z = z / R
    phi = np.arcsin(z)
    th = np.angle(x + 1j * y)
    return jrad2deg(phi, th)

def radearth():
    return 6371  # Earth's radius in kilometers

def jdeg2rad(*args):
    return [np.deg2rad(arg) for arg in args]

def jrad2deg(*args):
    return [np.rad2deg(arg) for arg in args]