import numpy as np

def IBeam(sigma, F, t, h_values, w_values, dist, tol):
    """
    Calculates the maximum geometric efficiency of an I-beam with the given parameters.

    Parameters
    ----------
    sigma : float
        The maximum allowable stress in the beam material.
    F : float
        The force applied to the beam.
    t : float
        The thickness of the beam flanges and web.
    h_values : array-like
        An array of possible heights for the beam web.
    w_values : array-like
        An array of possible widths for the beam flanges.
    dist : float
        The distance from the applied force to the centroid of the beam cross-section.
    tol : float
        The tolerance factor for the maximum allowable stress in the beam.

    Returns
    -------
    None
        The function prints the maximum geometric efficiency of the beam and its corresponding height, width, and distance from the applied force.
    """
    M = F * dist
    zShear = M / sigma
    
    # Initialize arrays for xsa, ix, y, zInt, and geom
    h_mesh, w_mesh = np.meshgrid(h_values, w_values, indexing='ij')
    xsa = 2 * t * w_mesh + t * h_mesh
    ix = (t * h_mesh**3) / 12 + (w_mesh / 12) * ((2*t+h_mesh)**3 - h_mesh**3)
    y = h_mesh / 2 + t
    zInt = ix / y
    geom = np.where(np.logical_or(zInt <= zShear, zInt >= tol * zShear), 0, zInt / xsa)
    
    # Find max value and its location in geom
    max_val = np.max(geom)
    max_val_indices = np.unravel_index(np.argmax(geom), geom.shape)
    
    # Print results
    print("The max value of geom is:", round(max_val, 2))
    print("height (h):", int(h_values[max_val_indices[0]]))
    print("width (w):", int(w_values[max_val_indices[1]]))
    print("distance from force applied:", int(dist))
    print("\n")


if __name__ == "__main__":
    
    sigma = 100 # Max stress not allowed to exceed (N/mm^2)
    F = 100 * pow(10, 3) # Force applied (N)
    dist = np.array([100, 1000, 2000, 3000, 4000]) # Distance from force applied (mm)

    t = 10 # Thickness of I-beam (mm)

    h = np.arange(1, 1001-2*t, step=1) # Height of I-beam (mm)
    w = np.arange(1, 1001-2*t, step=1) # width of I-beam (mm)

    tol = 2.00 # tolerance for the system (how close we want our desired shear modulus to be to the limit)
    
    for d in dist:
        IBeam(sigma, F, t, h, w, d, tol)
