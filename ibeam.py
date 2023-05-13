from tabulate import tabulate
import numpy as np

def ibeam(sigma, F, t, dist, tol, height_values, width_values):
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
    dist : float
        The distance from the applied force to the centroid of the beam cross-section.
    tol : float
        The tolerance factor for the maximum allowable stress in the beam.
    height_values : array-like
        An array of possible heights for the beam web.
    width_values : array-like
        An array of possible widths for the beam flanges.

    Returns
    -------
    None
        The function prints the maximum geometric efficiency of the beam and its corresponding height, width, and distance from the applied force in a table format.
    """
    headers = ['Height (h)', 'Width (w)', 'Distance from force applied (m)', 'Geometric efficiency']
    data = []

    for h in height_values:
        row_data = []
        for w in width_values:
            M = F * dist # calculating moment
            zShear = M / sigma # calculating shear modulus based on given conditions

            # calculating XSA for each h/w combination   
            xsa = 2*t*w + t*h 
            
            # calculating ix (i.e. inertia of rotation about the x-axis) for each h/w combination
            ix = (t*h**3)/12 + (w/12) * ((2*t+h)**3 - h**3) 
            
            # calculating y for each h combination 
            y = h/2 + t 

            # calculating zInt for each Ix/y combination
            zInt = ix / y

            # check to see if zInt <= zShear or >= tol * zShear since this is not ideal
            if zInt <= zShear or zInt >= tol * zShear:
                zInt = 0 # zInt is set to 0 if this condition is unsatisfied

            # Creating the relationship between zInt and XSA
            geom = round(zInt /  xsa, 2)

            row_data.append([h, w, dist, geom])

        data.extend(row_data)

    max_row = max(data, key=lambda x: x[3])
    print(tabulate([max_row], headers=headers))
    print("\n")


if __name__ == "__main__":
    
    sigma = 100 # Max stress not allowed to exceed (N/mm^2)
    F = 100 * pow(10, 3) # Force applied (N)
    dist = [100, 1000, 2000, 3000, 4000] # Distance from force applied (mm)

    t = 10 # Thickness of I-beam (mm)

    tol = 2.00 # tolerance for the system (how close we want our desired shear modulus to be to the limit)

    h = np.arange(1, 1001-2*t, step=1) # Height of I-beam (mm)
    w = np.arange(1, 1001-2*t, step=1) # width of I-beam (mm)

    for d in dist:
        ibeam(sigma, F, t, d, tol, h, w)
