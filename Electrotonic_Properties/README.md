<h1>Electrotonic Properties Dataframe Function</h1>

The goal of this function is to provide a dataframe with parameters to
begin modelling steady-state electrical properties of neurons. There are a number of assumptions,
noted explicitly here, required to take a CATMAID neuron and begin modelling its electrical properties. 

**It is highly recommended that you read Signal Propagation in Drosophila Central Neurons, Gouwens & Wilson (2009)
before using this code, as the equations and thinking used in this function are derived from this paper.**

***Pymaid (see https://github.com/schlegelp/pyMaid) is a dependency of this code***

<h2>A CATMAID neuron as a series of cylinders</h2>

To model the electrical properties of CATMAID neurons, we first take the neuron and divide it into segments.
This returns a list of lists; where each sub-list contains treenode_ids that are contained within a particular segment
The way that pymaid returns these segments is similar to the way a neuron is segmented in the review widget of CATMAID.
The start and end nodes of each segment are placed into separate lists. The geodesic distance between the segment's start
node and end node is then calculated using pymaid's dist_between function.

Using pymaid's guess_radius function, a copy of the neuron of interest (NOI) is returned where the radius of each treenode
is approximated. This is approximated by taking a treenode_id and finding the euclidian distance from this treenode to its connector.
For treenodes that do not have a connector, their radii remain at -0.01. For each segment, the radius associated with the start node
is used for the entire segment.

If we have the geodesic length of each segment and the radius associated with the start node of each segment, then we can
model each segment as a cylinder. The function then calculates the surface area and the cross sectional area (at the start node)
of each segment.

<h2>Electrical properties</h2>

The function has three free variables:

  1. Rm: Membrane Resistance, as kΩcm^2
  1. Cm: Membrane Capacitance, as µFcm^-2
  1. Ri: Intracellular Resistivity, as Ωcm
    
The default values for Rm, Cm and Ri are 20.8, 0.8 and 266.1 respectively. These values were taken from 
Gouwens & Wilson (2009) Table 1, Cell 3.

**The applicability of these values to non-PNs is an open question.**

<h2>Electrical properties of segments</h2>

*The following is taken from Gouwens & Wilson (2009)*

For each segment, its electrical properties are assumed to depend only on its geometry.
These properties are also assumed to be passive and uniform throughout the cell. 

Each segment has three geometry-dependent variables used for modelling:

  1. A pathway for intracellular current flow, modelled as a resistor (ri)
  1. A pathway for current flow across the membrane, modeled as a resistor (rm) and capacitor (cm)
 
rm and cm operate in parallel.
 
The equations to calculate ri, rm & cm are: 

  1. ri = Ri * (l / A)
  1. rm = Rm / a
  1. cm = Cm * a 
    
Where l = length of a segment, a = surface area & A = cross sectional area.

The function calculated ri, rm and cm and returns a dataframe containing all of the details 
mentioned here

<h2>Acknowledgements</h2>

This code was written by Markus Pleijzier, Drosophila Connectomics WT Team, Department of Zoology, University of Cambridge.




 
 



