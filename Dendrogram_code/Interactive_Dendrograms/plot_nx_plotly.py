import pymaid
import time
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as ps

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from scipy import stats
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)

import plotly as py
from plotly.graph_objs import *
import plotly.graph_objs as go

import collections
from itertools import chain

import powerlaw
import colormap
from colormap import rgb2hex



def plotly_plot_nx(z, plot_connectors = True, highlight_connectors = None, in_volume = None, prog = 'dot', inscreen = True, filename = None):
    
    
    if not isinstance(z,(pymaid.CatmaidNeuron, pymaid.CatmaidNeuronList)):
        raise ValueError('Need to pass a CatmaidNeuron')
    elif isinstance(z, pymaid.CatmaidNeuronList):
        if len(z) >1:
            raise ValueError('Need to pass a SINGLE CatmaidNeuron')
        else:
            z = z[0]
    
    valid_progs = ['neato','dot']
    if prog not in valid_progs:
        raise ValueError('Unknown program parameter!')
    
    #save start time
    
    start = time.time()
    
    #reroot neuron to soma if necessary
    
    if z.root != z.soma:
        z.reroot(z.soma)

    #Necessary for neato layouts for preservation of segment lengths
    
    if 'parent_dist' not in z.nodes:
        z = pymaid.calc_cable(z, return_skdata = True)
        
    #Generation of networkx diagram
    
    g = nx.DiGraph()
    g.add_nodes_from(z.nodes.treenode_id.values)
    for e in z.nodes[['treenode_id','parent_id','parent_dist']].values:
        #skipping root node
        if e[1] == None:
            continue
        g.add_edge(e[0],e[1],len = e[2])
        
        
    #Calculate Layout
    print ('Calculating node positions...')
    pos = nx.nx_agraph.graphviz_layout(g, prog = prog)
    print ('Finished calculating node positions...')
    
    print('Now converting for plotly...')
    
    #Convering networkx nodes for plotly
    #NODES
    
    x = []
    y = []
    node_info = []
    
    for n in g.nodes():
        x_, y_ = pos[n]
        
        x.append(x_)
        y.append(y_)
        node_info.append("Treenode_id: {}".format(n))
        
    node_trace = go.Scatter(x = x, y = y, mode = 'markers', text = node_info,
                            hoverinfo = 'text', marker = go.scatter.Marker(showscale=False))

    #EDGES
    
    xe = []
    ye = []
    
    for e in g.edges():
        
        x0, y0 = pos[e[0]]
        x1, y1 = pos[e[1]]
        
        xe += [x0, x1, None]
        ye += [y0, y1, None]
        
    edge_trace = go.Scatter(x = xe, y = ye, 
                            line = go.scatter.Line(width = 1.0, color = '#000'), 
                            hoverinfo = 'none', mode = 'lines')
    
    #SOMA
    
    xs = []
    ys = []
    
    for n in g.nodes():
        if n != z.soma:
            continue
        elif n == z.soma:
            
            x__, y__ = pos[n]
            xs.append(x__)
            ys.append(y__)
            
        else:
            
            break
            
    soma_trace = go.Scatter(x = xs, y = ys,
                            mode = 'markers',
                            hoverinfo = 'text',
                            marker = dict(size = 20, color = 'rgb(0,0,0)'),
                            text = 'Soma, treenode_id:{}'.format(z.soma))
    
    #CONNECTORS:
    #RELATION  = 0 ARE PRESYNAPSES, RELATION = 1 ARE POSTSYNAPSES
    
    if plot_connectors == False:
        
        presynapse_connector_trace = go.Scatter()
        
        postsynapse_connector_trace = go.Scatter()
        
    elif plot_connectors == True:
        

        presynapse_connector_list = list(z.connectors[z.connectors.relation==0].treenode_id.values)
        
        x_pre = []
        y_pre = []
        presynapse_connector_info = []
    
        for node in g.nodes():
            for tn in presynapse_connector_list:
            
                if node == tn:
                
                    x,y = pos[node]
                
                    x_pre.append(x)
                    y_pre.append(y)
                    presynapse_connector_info.append("Presynapse, connector_id: {}".format(tn))
    
        presynapse_connector_trace = go.Scatter(x = x_pre, y = y_pre, 
                                            text = presynapse_connector_info, mode = 'markers', hoverinfo = 'text',
                                            marker = dict(size = 10, color = 'rgb(0,255,0)'))
    
        postsynapse_connectors_list = list(z.connectors[z.connectors.relation==1].treenode_id.values)
    
        x_post = []
        y_post = []
        postsynapse_connector_info = []
    
        for node in g.nodes():
            for tn in postsynapse_connectors_list:
            
                if node == tn:
                
                    x,y = pos[node]
                
                    x_post.append(x)
                    y_post.append(y)
                
                    postsynapse_connector_info.append("Postsynapse, connector id: {}".format(tn))
                
        postsynapse_connector_trace = go.Scatter(x = x_post, y = y_post, 
                                             text = postsynapse_connector_info, mode = 'markers', hoverinfo = 'text', 
                                             marker = dict(size = 10, color = 'rgb(0,0,255)'))


    if highlight_connectors == None:
        
        HC_trace = go.Scatter()
        
    elif highlight_connectors != None: 
        
        HC_nodes = []
        
        for i in highlight_connectors:
            
            HC_nodes.append(z.connectors[z.connectors.connector_id == i].treenode_id.values[0])
            
            HC_x = []
            HC_y = []
            
            HC_info = []
            
            for node in g.nodes():
                
                for tn in HC_treenodes:
                    
                    if node == tn:
                        
                        x,y = pos[node]
                        
                        HC_x.append(x)
                        HC_y.append(y) 
                        
                        HC_info.append("Connector of Interest, connector_id: {}, treenode_id: {}".format(z.connectors[z.connectors.treenode_id == node].connector_id.values[0],node))
                        
            HC_trace = go.Scatter(x = HC_x, y = HC_y, 
                                  text = HC_info, mode = 'markers', hoverinfo = 'text', 
                                  marker = dict(size = 15, color = 'rgb(238,0,255)'))
            
                        
    
    
    ##Highlight the nodes that are in a particular volume
    
    
    if in_volume == None:
        
        in_volume_trace = go.Scatter()
        
    elif in_volume != None:
        
        #Volume of interest
        
        res = pymaid.in_volume(z.nodes, volume = in_volume, mode = "IN")
        z.nodes['IN_VOLUME'] = res
        
        x_VOI = []
        y_VOI = []
        
        VOI_info = []
        
        for nodes in g.nodes():
            
            for tn in list(z.nodes[z.nodes.IN_VOLUME == True].treenode_id.values):
                
                if nodes == tn:
                    
                    x,y = pos[tn]
                    
                    x_VOI.append(x)
                    y_VOI.append(y)
                    
                    VOI_info.append("Treenode {} is in {} volume".format(tn, in_volume))
                    
        in_volume_trace = go.Scatter(x = x_VOI, y = y_VOI, 
                                     text = VOI_info, mode = 'markers', hoverinfo = 'text', 
                                     marker = dict(size = 5, color = 'rgb(35,119,0)'))        

    
    print("Creating Plotly Graph")
    
    fig = go.Figure(data = [edge_trace, node_trace, soma_trace, 
                                 presynapse_connector_trace, postsynapse_connector_trace, HC_trace, in_volume_trace], 
                    layout = go.Layout(title = "Plotly graph of {} with {} layout".format(z.neuron_name, prog), 
                                       titlefont = dict(size = 16), 
                                       showlegend = False, 
                                       hovermode = 'closest', margin = dict(b = 20, l = 50, r = 5, t = 40), annotations= [dict(showarrow = False, xref = 'paper', yref = 'paper', x = 0.005, y = -0.002)],
                                       xaxis = go.layout.XAxis(showgrid = False, zeroline = False, showticklabels = False),
                                       yaxis = go.layout.YAxis(showgrid = False, zeroline = False, showticklabels = False)))
    
    if inscreen == True:
        
        return(iplot(fig))
    
    else:
        
        return(plot(fig, filename = filename))
    