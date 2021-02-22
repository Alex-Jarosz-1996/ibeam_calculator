#%% 
## Inputs / Outputs / Comments definition
# Inputs:
# sigma : max allowable stress
# F     : force applied
# t     : thickness of I-beam
# h     : height of I-beam (NOTE: total height of I-beam = h + 2*t)
# w     : width of I-beam
# dist  : distance from force applied, requirement for bending moment
# calculation
# tol   : tolerance -> how much we want the chosen z value (zInt) to be
# over the minimum (we don't want too high as this leads to unnecessary mass)

# Outputs:
# geom   : relationship b/w shear modulus and XSA (i.e. want to maximise)


# Comments:
# (1) This code chunks seeks to find an optimal geometric configuration based
#     on dist

# (2) We want to maximise zInt -> i.e. since sigma = M / Z, since increasing Z
#     means decreasing sigma (which is ideal for our case)

# (3) For the zInt / XSA case, we want to minimize XSA (as small XSA means less mass) 
#     and maximise zInt (refer to (2) for explanation)
#%% 
# Importing the appropriate packages
import numpy as np
print("All modules imported")

# Final version:
#  - successfully converted the .m code into a .py code

## Defining the system inputs
sigma = 100 # Max stress not allowed to exceed (N/mm^2)
F = 100 * 10**3 # Force applied (N)
dist = np.array([100, 1000, 2000, 3000, 4000]) # Distance from force applied (mm)

t = 10 # Thickness of I-beam (mm)

h = np.arange(1, 1001-2*t, step=1) # Height of I-beam (mm)
w = np.arange(1, 1001-2*t, step=1) # width of I-beam (mm)

tol = 2.00 # tolerance for the system (how close we want our desired shear modulus to be to the limit)

# Writing the IBeam function
def IBeam(sigma, F, t, h, w, dist, tol):
    M = F * dist # calculating moment
    zShear = M / sigma # calculating shear modulus based on given conditions

    # pre-allocation of the xsa, ix, y, zInt and geom arrays
    xsa  = np.zeros((h.size, w.size)) # mm^2
    ix   = np.zeros((h.size, w.size)) # mm^3
    y    = np.zeros((h.size, w.size)) # mm
    zInt = np.zeros((h.size, w.size)) # mm^2
    geom = np.zeros((h.size, w.size)) # dimensionless

    # iterating through all combinations of height and width
    for i in range(0, len(h)): # iterating through the height vector
        for j in range(0, len(w)): # iterating through the width vector
            xsa[i, j] = 2*t*w[j] + t*h[i] # calculating XSA for each h/w combination   
            ix[i, j] = (t*h[i]**3)/12 + (w[j]/12) * ((2*t+h[i])**3 - h[i]**3) # calculating ix (i.e. inertia of rotation about the x-axis) for each h/w combination
            y[i] = h[i]/2 + t # calculating y for each h combination 
            zInt[i, j] = ix[i, j] / y[i, j] # calculating zInt for each Ix/y combination

            # check to see if zInt <= zShear or >= tol * zShear since this is not ideal
            if zInt[i, j] <= zShear or zInt[i, j] >= tol * zShear:
                zInt[i, j] = 0 # zInt is set to 0 if this condition is unsatisfied

            geom[i, j] = zInt[i, j] /  xsa[i, j] # Creating the relationship between zInt and XSA

    maxVal = np.amax(geom) # finding the max value of geom
    print("\nThe max value of geom is: ", round(maxVal, 2))

    maxValLoc = np.where(geom == np.amax(geom)) # finding the coordinates of the max value of geom
    # this represents our most optimal inertia-xsa solution
    print("height (h):", int(maxValLoc[0]), "\nwidth (w):", int(maxValLoc[1]), "\ndistance from force applied:", int(dist))

# Calling the I-Beam function

for d in dist:
    IBeam(sigma, F, t, h, w, d, tol) # looping through all distance values to print
