# I-beam_calculator
This project seeks to find an optimal geometric configuration for an I-beam. It aims to find the optimal height and width for a symmetric I-beam around the x-axis.  
The purpose of this file is to find the theoretical ideal relationship between for an I-beam.

Inputs:
 - sigma : max allowable stress
 - F     : force applied
 - t     : thickness of I-beam
 - h     : height of I-beam (NOTE: total height of I-beam = h + 2*t)
 - w     : width of I-beam
 - dist  : distance from force applied, requirement for bending moment
 - tol   : tolerance -> how much we want the chosen z value (zInt) to be

Outputs:
 - The output displays the recommended geometry at each dist from F
