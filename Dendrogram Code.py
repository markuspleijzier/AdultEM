#Plotting Dendrograms - This assumes some basic knowledge of Pymaid.
#For more information on Pymaid, see http://pymaid.readthedocs.io/en/latest/

#Import required packages

import sys
sys.path.append('/Users/')
import pymaid
import time
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as ps

#A requirement of this code is access to CATMAID.
#This is for API access to the CATMAID servers and to download skeleton information
server = 
http_user = 
http_pw = 
token = 


pymaid.CatmaidInstance( server, http_user, http_pw, token)




#This is an integer number that is unique to your neuron of interest
Neuron_1_skeleton_id_number = 
Neuron_1 = pymaid.get_neuron(Neuron_skeleton_id_number)

Neuron_2_skeleton_id_number = 
Neuron_2 = pymaid.get_neuron(Neuron_2_skeleton_id_number) 

#This function downsamples the neuron - it removes large stretches of skeleton that do not have any branch points.
#When the argument preserve_cn_treenodes = True, this preserves the treenodes where connectors (pre/postsynapses)
#have been placed. Downsampling is used to reduce the computational time, as some 3D reconstructed neurons can become 
#very large. 
Neuron.downsample(1000000, preserve_cn_treenodes = True) 
Neuron_2.downsample(1000000, preserve_cn_treenodes = True)


#Get the connectors between the two neurons of interest
#When True, the directional argument will return the connectors (pre and post synapses)
#from neuron A to neuron B (A-->B; in this case Neuron_1 to Neuron_2). When False, it will return all
#connectors between neuron A to neuron B (A<-->B; in this case, all connectors between Neuron_1 to Neuron_2)

Neuron_1_to_Neuron_2 = pymaid.get_connectors_between(Neuron_1,Neuron_2, directional = True)



def plot_nx(x, plot_connectors=True, highlight_connectors=None, prog='dot'):
    """ This lets you plot neurons as dendrograms using networkx and its bindings
    to graphviz.

    Parameters
    ----------
    x :     				CatmaidNeuron
            				Neuron to plot. Strongly recommend to downsample the neuron!
    plot_connectors :       bool, optional
                            If True, connectors will be plotted
    highlight_connectors :  list of int
                            These connectors (or more precisely, the treenodes they
                            connect to) will be highlighted in green
    prog :                  {'dot','neato','fdp'}
                            Graphviz layout to use. Be aware that neato and fdp are 
                            extremely slow!

    Returns
    -------
    Nothing

    Examples
    --------
    >>> import pymaid
    >>> import matplotlib.pyplot as plt
    >>> rm = pymaid.CatmaidInstance(server,user,password,token)
    >>> # Retrieve neuron
    >>> x = pymaid.get_neuron(16)
    >>> # Downsample to just the essential treenodes (will speed up processing A LOT)
    >>> x.downsample(100000, preserve_cn_treenodes=True)
    >>> plot_nx( x, plot_connectors=True )
    >>> plt.show()
    """

    if not isinstance(x, (pymaid.CatmaidNeuron, pymaid.CatmaidNeuronList)):
        raise ValueError('Need to pass a CatmaidNeuron')
    elif isinstance(x, pymaid.CatmaidNeuronList):
        if len(x) > 1:
            raise ValueError('Need to pass a SINGLE CatmaidNeuron')
        else:
            x = x[0]

    valid_progs = ['fdp','dot','neato']
    if prog not in valid_progs:
        raise ValueError('Unknown program parameter!')

    # Save start time
    start = time.time()

    # Reroot neuron to soma if necessary
    if x.root != x.soma:
        x.reroot(x.soma)

    # This is only relevant if we use the 'neato' layout as it preserves segment lengths
    if 'parent_dist' not in x.nodes:
        x = pymaid.calc_cable(x, return_skdata=True)

    # Generate and populate networkX graph representation of the neuron
    g=nx.DiGraph()
    g.add_nodes_from( x.nodes.treenode_id.values )
    for e in x.nodes[['treenode_id','parent_id','parent_dist']].values:
        #Skip root node
        if e[1]==None:
            continue
        g.add_edge(e[0],e[1],len=e[2])

    # Calculate layout
    print('Calculating node positions...')
    pos = nx.nx_agraph.graphviz_layout(g, prog=prog)
    
    
    # Plot tree with above layout
    print('Plotting tree...')
    nx.draw(g, pos, node_size=0, arrows=False, width = 0.1)

    #Add soma
    plt.scatter([pos[x.soma][0]], [pos[x.soma][1]], s=40, c=(0,0,0), zorder=1 )

    print('Plotting connectors...')
    if plot_connectors:
        plt.scatter(  
                    [ pos[tn][0] for tn in x.connectors[x.connectors.relation==0].treenode_id.values ],
                    [ pos[tn][1] for tn in x.connectors[x.connectors.relation==0].treenode_id.values ],
                    c=(.0,.6,.2),
                    zorder=2,
                    s=0.1)

        plt.scatter(  
                    [ pos[tn][0] for tn in x.connectors[x.connectors.relation==1].treenode_id.values ],
                    [ pos[tn][1] for tn in x.connectors[x.connectors.relation==1].treenode_id.values ],
                    c=(.0,.2,1.0),
                    zorder=2,
                    s=0.1)

    if highlight_connectors != None:
        hl_cn_coords = np.array([ pos[tn] for tn in x.connectors[ x.connectors.connector_id.isin( highlight_connectors ) ].treenode_id ])
        plt.scatter( hl_cn_coords[:,0], hl_cn_coords[:,1], s = 1, c=(0.8,0.0,0.2), zorder = 3 )       


    print('Done in %is' % int( time.time()-start ))
    


#For the diagrams used in Felsenberg et al., 2018, we used the neato algorithm. For more information 
#on neato vs dot vs fdp, see https://www.graphviz.org/

#For large neurons, note that the neato algorithm will rarely produce the same layout - a certain number
#of configurations exist within the plotting space and each iteration of the algorithm restarts the configuration.

plot_nx(Neuron_2, plot_connectors = True, highlight_connectors = Neuron_1_to_Neuron_2, prog = 'neato')
plt.savefig('Neuron_2_with_Neuron_1_connectors.svg') 


