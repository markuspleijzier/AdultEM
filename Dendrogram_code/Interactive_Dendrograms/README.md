# Interactive Dendrogram: plot_nx_plotly: 

This script is built upon the previous Dendrogram code (see https://github.com/CATMAID-FAFB/catmaid-tools/tree/master/Python/Dendrogram_Code) 
which renders 2D graphical representations of 3D reconstructed CATMAID neurons. However, a major caveat of these static dendrograms
is that one cannot extract treenode or connector information from these graphical representations.

The code presented here addresses this problem, providing an interactive version of dendrograms such that specific
treenode_id and connector_id information can be extracted from the renderings. This enables a user to extract more information
from dendrograms in order to subject the neurons of interest (NOIs) for further analyses; e.g. which branches are
particularly interesting due to the inputs they receive there. 

This code takes the NetworkX & Graphviz renderings of CATMAID neurons and uses plotly (see https://plot.ly/python/) as a backend
to provide the interactive visualisation.


## Getting Started

This README.md assumes that the reader has already installed all of the necessary packages for rendering a dendrogram
as detailed in https://github.com/CATMAID-FAFB/catmaid-tools/tree/master/Python/Dendrogram_Code 

As mentioned, this interactive version of dendrograms use plotly as a backend.

**Plotly (see https://plot.ly/python/getting-started/)**

To install plotly simply run this snippet in the terminal 

		$ pip install plotly
		
Instead of using the online version of plotly, we will focus on the offline version - *Continue reading*


## Setting up plotly offline & Importing required packages

First, set up the offline version by running the following code in your python environment/shell:


		>>> import plotly as py
		
		>>> from plotly.graph_objs import *
		
		>>> from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
		
		>>> from mpl_toolkits.mplot3d import Axes3D
		
		>>> init_notebook_mode(connected = True)
		
		
Now import the packages required to render the static dendrograms

		>>> import pymaid 
		
		>>> import networkx as nx
		
		>>> import matplotlib.pyplot as plt
		
		>>> import time
			
		
## Example Usage

		>>> rm = pymaid.CatmaidInstance(server, user, password, token) 
		
		>>> # Get the neuron of interest (NOI) - e.g. skid 
		
		>>> z = pymaid.get_neuron(NOI)
		
		>>> # Downsample the neuron to the essential nodes & preserve the connector nodes
		
		>>> z.downsample(100000, preserve_cn_treenodes = True)
		
**THE PLOT_NX_PLOTLY FUNCTION IS LOCATED IN THE OTHER FILE WITHIN THIS FOLDER.**
**TOP OF THE PAGE, plot_nx_plotly.py.**

**SIMPLY COPY AND PASTE THE FUNCTION INTO YOUR PYTHON ENVIRONMENT (LINE/CELL) AND RUN IT**
		
		>>> plot_nx_plotly(z, prog = 'dot', plot_connectors = True, highlight_connectors = none, inscreen = True)
		
## Acknowledgements

This code was written by Markus Pleijzier, Drosophila Connectomics WT UK Team, Department of Zoology, University of Cambridge.

