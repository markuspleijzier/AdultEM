<h1>Dendrogram Code: 
The plot_nx function:</h2>

This script creates 2D graph representation of 3D reconstructed CATMAID neurons. Using 
pymaid (see https://github.com/schlegelp/pymaid), it recovers treenode and connector 
information of any neuron from CATMAID and renders it as a NetworkX graph/network: 
	
- treenode_ids are treated as 'nodes/vertices'
- edges/links are drawn between parent and daughter treenode_ids
	
As every connector (both presynaptic & postsynaptic) are associated with a specific 
treenode id (both presynaptic & postsynaptic), the plot_nx function also allows one 
visualise which treenodes of a neuron are connected by specific neurons/ specific 
connector ids. This allows one to visualise the placement of synapses from 
specific neurons/ lineages.

<h2>Getting Started</h2>

These notes detail what is required in order to run the Dendrogram Code. 

If this is your first time using this code, please install the following packages using 
pip in the terminal:

**Pymaid (see https://github.com/schlegelp/pymaid)**

    $ pip install git+git://github.com/schlegelp/pymaid@master

**NetworkX (see https://networkx.github.io/documentation/stable/install.html)**

    $ pip install networkx

Installing the graph drawing engines is a little more complicated. To install Graphviz, 
one must first install homebrew: 

**Homebrew ( see https://brew.sh/ )**

    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Simply paste the above into the terminal. 

Then to install Graphviz:

**Graphviz (see http://www.graphviz.org/)**

    $ brew install Graphviz

**PyGraphviz ( see http://pygraphviz.github.io/)** 

To install PyGraphviz, we need to direct pip (this time using pip3) to where Graphviz is located. 
To do this, simply paste this snippet into the terminal: 

    pip3 install --install-option="--include-path=/usr/local/include/" --install-option="--library-path=/usr/local/lib/" pygraphviz
    

Once these are installed, import them into your environment. Graphviz is a dependency of 
NetworkX, so there is no need to import Graphviz/PyGraphviz. 

    >>> import pymaid
   
    >>> import networkx as nx
    
    >>> import matplotlib.pyplot as plt
    
    >>> import time

<h2>Example of Use</h2>

    >>> rm = pymaid.CatmaidInstance(server, user, password, token) 

    >>> #Get the neuron of interest (NOI) - e.g. skid

    >>> x = pymaid.get_neuron( NOI )

    >>> #Downsample to just the essential nodes -- this step is not absolutely required,
    >>> #although it speeds up the processing dramatically. The preserve_cn_treenodes argument
    >>> #preserves the treenodes which are connected to a presynapse/postsynapse. Downsampling a neuron 
    >>> #will have a greater effect on the represenation by the 
    >>> #neato algorithm than dot (see Important Note below)

    >>> x.downsample( 100000 , preserve_cn_treenodes = True )
    
**THE PLOT_NX FUNCTION IS LOCATED IN THE OTHER FILE OF THIS FOLDER**
    
**COPY AND PASTE THE FUNCTION INTO A NEW LINE/CELL OF YOUR PYTHON ENVIRONMENT, THEN RUN:**

    >>> plot_nx( x, plot_connectors = True, highlight_connectors = None, prog = 'dot')

    >>> plt.show()
    
*TIP: When producing dendrograms of multiple neurons, remember to clear the plotting space to avoid all of your
dendrograms being plotted ontop of one another. To do this, use*

    >>> plt.clf()
    
<h2>Example Renderings</h2>

Dendrogram of a VM2 neuron using the dot layout

![](https://github.com/markuspleijzier/AdultEM/blob/master/VM_neuron_dot.png)

Dendrogram of a VM2 neuron using the neato layout

![](https://github.com/markuspleijzier/AdultEM/blob/master/VM_neuron_neato.png)

<h2>Extra Details of plot_nx/ graphviz</h2>

Two possible graphical layout engines used by graphviz in this function are: 
(there is a third available to use on the plot_nx function, called fdp, but we
won't discuss that here). 

1. dot
1. neato


    (1) The **dot** layout draws directed graphs (like phone calls, where person A calling person B 
    is enough to initiate a phone call, but it is not necessary for person B to also call person A 
    at the same time to start talking). For Catmaid neurons, the treenodes most distal (i.e. the 
    tip of the dendrites) are treated as the top of the hierarchy and the soma is at the bottom 
    of the hierarchy. For more information see https://www.graphviz.org/pdf/dotguide.pdf

    (2) The **neato** layout draws undirected graphs (where if person A dates person B, person B also dates person A). 
    The neato layout takes all the nodes and finds the lowest energy configuration of where the nodes should be placed. 
    It does this by placing a 'virtual spring' between each node. The force from this spring is proportional to the **geodesic**
    distance between the nodes. Imagine you have a bunch of connected, individual springs. You squeeze 
    the ball of springs and let go. Each spring will continue to exert (extend) or accept (contract) a force 
    from another spring until the system reaches an equilibrium state. This is a loose analogy as to how the neato 
    algorithm works. As the force is proportional to the distance between notes, this gives neato diagrams an 
    advantage of being able to respect the distance between nodes, giving a more realistic representation of 
    the neuron than the dot layout, which does not consider distance. 
    Finding this low energy configuration takes a long time, therefore it is strongly recommended that one 
    downsamples the NOI before running the neato algorithm (by a factor of 1000000). 
    For more information see http://www.graphviz.org/pdf/neatoguide.pdf 

<h2>**Important Note**</h2>

Downsampling a neuron will have a greater effect on the representation by the neato algorithm than when using the dot algorithm
This is because the dot algorithm does not consider the distance between nodes when plotting; it only plots the neuron hierarchically
from the tip of the dendrites to the soma. The neato algorithm does consider (**geodesic**) distance when plotting, so if one downsamples a neuron
(i.e. removes 'unessential' nodes), then the distance between any remaining nodes becomes more euclidean rather than geodesic. This results in
overestimations and underestimations of the actual distance between certain nodes.

<h2>Acknowledgments</h2>
This code was written by Markus Pleijzier, Drosophila Connectomics WT Team, Department of Zoology, University of Cambridge
and by Philipp Schlegel, Drosophila Connectomics WT Team, Department of Zoology, University of Cambridge & Jefferis Lab, Laboratory of Molecular Biology,
Cambridge. This code was used to generate figures in Felsenberg et al. (2018)
