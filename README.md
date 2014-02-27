pyboxgen
========

Parametric box generation for CNC/Lasercut.

Currently, there is the box.py script. At the end of the script
you can find the parameters:

* b=460 (X-Size of the box)
* t=560 (Y-Size of the box)
* h=70 (Height of the box)
* dis=5 (Thickness of material used for the compartments and bottom)
* das=10 (Thickness of material used for frame)
* df=2 (Cutting bit diameter)
* hs = [140, 280] (Positions of compartments, horizontally)
* vs = [115, 230] (Positions of compartments, vertically)


The script requires the "dxfwrite" library to be installed.
Running the script with python should result in a kasten.dxf
file containing the cutting plan for your box.
