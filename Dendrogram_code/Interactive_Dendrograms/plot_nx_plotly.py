def plot_nx_plotly(z, plot_connectors = True, highlight_connectors = None, prog = 'dot', inscreen = True, filename = 'name'):
    
    """This plots an interactive dendrogram so that specific treenode and connector_ids can be examined
    
    Parameters
    ----------
    
            z : CatmaidNeuron - the neuron to plot. Downsampling is strongly recommended
    
            plot_connectors : True/False - whether to show the connectors or not.

            Presynapses are Green
            Postsynapses are Blue
    
            highlight_connectors : A list of connector_ids that are of interest (CoIs = connectors of interest).
            e.g. HCs = [Connector_id1, Connector_id2, etc.]
            
            These will be larger than the other connectors and in purple
    
            prog: The plotting engine to be used by Graphviz; dot or neato 
    
            inscreen: Have the rendering in the output cell (for jupyter notebooks) or as a separate
            html file. Note, this is then saved to your downloads as temp-plot.html unless a filename is specified
    
            filename:  A string for the filename
    
    """
    
    
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
    
    node_trace = Scatter(
        x = [],
        y = [],
        text = [],
        mode = 'markers',
        hoverinfo = 'text',
        marker = Marker(showscale = False))
    
    
    for node in g.nodes():
        x,y = pos[node]
        node_trace['x'].append(x)
        node_trace['y'].append(y)
        node_info = 'treenode_id:  '+str(node)
        node_trace['text'].append(node_info)
        
    
    edge_trace = Scatter(
        x = [],
        y = [],
        line = Line(width = 1.0, color = '#000'),
        hoverinfo = 'none',
        mode = 'lines')
    
    for edge in g.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]
    
    #Soma
    
    soma_trace = Scatter(
    x = [],
    y = [],
    text = [],
    mode = 'markers',
    hoverinfo = 'text',
    marker = dict(
        size = 20,
        color = 'rgb(0,0,0)'))
    
    for node in g.nodes():
        if node != z.soma:
            continue
        elif node == z.soma:
            x,y = pos[node]
            soma_trace['x'].append(x)
            soma_trace['y'].append(y)
            soma_info = 'SOMA, treenode_id:  '+str(node)
            soma_trace['text'].append(soma_info)
        else: 
            break
    
    #Connectors: 
    #relation = 0 is outputs (presynapses), relation = 1 is inputs (postsynapses)
    
    if plot_connectors == False:
        
        presynapse_connector_trace = Scatter()
        
        postsynapse_connector_trace = Scatter()
        
    
    elif plot_connectors == True:
        
        presynapse_connectors = z.connectors[z.connectors.relation==0].treenode_id.values
        presynapse_connector_list = presynapse_connectors.tolist()
    
        presynapse_connector_trace = Scatter(
            x=[],
            y=[],
            text=[],
            mode = 'markers',
            hoverinfo = 'text',
            marker = dict(
                size = 10,
                color = 'rgb(0,255,0)'))
    
        postsynapse_connectors = z.connectors[z.connectors.relation==1].treenode_id.values
        postsynapse_connector_list = postsynapse_connectors.tolist()
    
        postsynapse_connector_trace = Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker = dict(
                size = 10,
                color = 'rgb(0,0,255)'))
    
        for node in g.nodes():
            for tn in presynapse_connector_list:
                if node == tn:
                    x,y = pos[node]
                    presynapse_connector_trace['x'].append(x)
                    presynapse_connector_trace['y'].append(y)
                    presynapse_connector_info = 'Presynapse here, Connector_id: {}, treenode id: {}'.format(z.connectors[z.connectors.treenode_id==node].connector_id.values[0],node)
                    presynapse_connector_trace['text'].append(presynapse_connector_info)
    
        for node in g.nodes():
            for tn in postsynapse_connector_list:
                if node == tn:
                    x,y = pos[node]
                    postsynapse_connector_trace['x'].append(x)
                    postsynapse_connector_trace['y'].append(y)
                    postsynapse_connector_info = 'Postsynapse here, Connector_id: {}, treenode id: {}'.format(z.connectors[z.connectors.treenode_id==node].connector_id.values[0],node)
                    postsynapse_connector_trace['text'].append(postsynapse_connector_info)
    
    if highlight_connectors == None:
            
        HC_trace = Scatter()
            
    elif highlight_connectors != None:
            
        HC_treenodes = []
            
        for i in highlight_connectors:
                
            HC_treenodes.append(z.connectors[z.connectors.connector_id == i].treenode_id.values[0])
            
            HC_trace = Scatter(
            x = [],
            y = [],
            text = [],
            mode = 'markers',
            hoverinfo = 'text',
            marker = dict(
                size = 15,
                color = 'rgb(238,0,255)'))
            
        for node in g.nodes():
            for tn in HC_treenodes:
                 if node == tn:
                    x,y = pos[node]
                    HC_trace['x'].append(x)
                    HC_trace['y'].append(y)
                    HC_trace_info = 'CoI: {}, treenode id: {}'.format(z.connectors[z.connectors.treenode_id==node].connector_id.values[0],node)
                    HC_trace['text'].append(HC_trace_info)
                        
    
    print('Creating Plotly Graph')
    
    fig = Figure(data=Data([edge_trace, node_trace, soma_trace, presynapse_connector_trace, postsynapse_connector_trace, HC_trace]),
                layout = Layout(
                title = '{}, with {} rendering.'.format(z.neuron_name, prog),
                titlefont = dict(size = 16),
                showlegend = False,
                hovermode = 'closest',
                margin = dict(b = 20, l = 50, r = 5, t= 40),
                annotations=[ dict(
                    showarrow = False,
                    xref = 'paper', yref = 'paper',
                    x = 0.005, y = -0.002 ) ],
                xaxis = XAxis(showgrid = False, zeroline = False, showticklabels = False),
                yaxis = YAxis(showgrid = False, zeroline = False, showticklabels = False)))
    
    
    if inscreen == True: 
        
        return(iplot(fig))
    
    elif inscreen != True:
    
        return(plot(fig, filename = filename))
